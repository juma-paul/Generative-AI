import os
import re
import ssl
import certifi
import urllib.request
from typing import List
from collections import deque
from html.parser import HTMLParser
from urllib.parse import urlparse

import numpy as np
import pandas as pd
import tiktoken
import openai
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv('openai_api_key')

# Initialize OpenAI client
client = openai.OpenAI(api_key=API_KEY)

# Constants
HTTP_URL_PATTERN = r'^http[s]*://.+'
DOMAIN = 'bine.co.zm'
FULL_URL = 'https://bine.co.zm/'
MAX_TOKENS = 1800

# SSL Verification function
def get_url_content(url):
    context = ssl.create_default_context(cafile=certifi.where())
    with urllib.request.urlopen(url, context=context) as response:
        return response.read()

# Crawler classes and functions
class HyperlinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hyperlinks = []

    def handle_starttag(self, tag: str, attrs: str):
        attrs = dict(attrs)
        if tag == 'a' and 'href' in attrs:
            self.hyperlinks.append(attrs['href'])

def get_hyperlinks(url: str) -> List[str]:
    try:
        with urllib.request.urlopen(url) as response:
            if not response.info().get('Content-Type').startswith('text/html'):
                return []
            html = response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching URL {url}: {e}")
        return []
    parser = HyperlinkParser()
    parser.feed(html)
    return parser.hyperlinks

def get_domain_hyperlinks(local_domain: str, url: str) -> List[str]:
    clean_links = []
    for link in set(get_hyperlinks(url)):
        clean_link = None
        if re.search(HTTP_URL_PATTERN, link):
            url_obj = urlparse(link)
            if url_obj.netloc == local_domain:
                clean_link = link
        else:
            if link.startswith('/'):
                link = link[1:]
            elif link.startswith('#') or link.startswith('mailto:'):
                continue
            clean_link = f'https://{local_domain}/{link}'
        if clean_link is not None:
            if clean_link.endswith('/'):
                clean_link = clean_link[:-1]
            clean_links.append(clean_link)
    return list(set(clean_links))

def crawl(url: str) -> str:
    local_domain = urlparse(url).netloc
    queue = deque([url])
    seen = set([url])

    raw_dir = f'text/{local_domain}/'
    os.makedirs(raw_dir, exist_ok=True)

    while queue:
        url = queue.pop()
        print(f"Crawling: {url}")

        try:
            page_content = requests.get(url).text
            soup = BeautifulSoup(page_content, 'html.parser')
            text = soup.get_text()

            # Save raw text
            file_path = os.path.join(raw_dir, url[8:].replace("/", "_") + ".txt")
            with open(file_path, 'w', encoding='UTF-8') as f:
                f.write(text)

            if 'You need to enable JavaScript to run this app.' in text:
                print(f"Unable to parse page {url} due to JavaScript being required")
                continue
        except Exception as e:
            print(f"Error crawling {url}: {e}")
            continue

        # Process domain hyperlinks
        for link in get_domain_hyperlinks(local_domain, url):
            if link not in seen:
                queue.append(link)
                seen.add(link)

# Data processing functions
def remove_newlines(serie):
    serie = serie.str.replace(r'[\n\\n]+', ' ', regex=True)
    return serie.str.replace('  ', ' ')

def split_into_many(text, max_tokens=MAX_TOKENS):
    tokenizer = tiktoken.get_encoding('cl100k_base')
    sentences = text.split('. ')
    n_tokens = [len(tokenizer.encode(' ' + sentence)) for sentence in sentences]
    chunks, tokens_so_far, chunk = [], 0, []
    for sentence, token in zip(sentences, n_tokens):
        if tokens_so_far + token > max_tokens:
            chunks.append('. '.join(chunk) + '.')
            chunk = []
            tokens_so_far = 0
        if token > max_tokens:
            continue
        chunk.append(sentence)
        tokens_so_far += token + 1
    return chunks

# Embedding and similarity functions
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def distances_from_embeddings(query_embedding, embeddings):
    return [1 - cosine_similarity(query_embedding, embedding) for embedding in embeddings]

def create_context(question, df, max_len=1800, size='ada'):
    question_embeddings = client.embeddings.create(input=question, model='text-embedding-ada-002').data[0].embedding
    df['distances'] = distances_from_embeddings(question_embeddings, df['embeddings'].values)
    returns, cur_len = [], 0
    for _, row in df.sort_values('distances', ascending=True).iterrows():
        cur_len += row['n_tokens'] + 4
        if cur_len > max_len:
            break
        returns.append(row['text'])
    return '\n\n###\n\n'.join(returns)

def answer_question(df, question='What are the main services?', model='gpt-3.5-turbo', max_tokens=150):
    context = create_context(question, df)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {'role': 'system', 'content': "Answer the question based on the context below."},
            {'role': 'user', 'content': f'Context: {context}\n\nQuestion: {question}\nAnswer:'}
        ],
        temperature=0,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content

def load_data():
    processed_dir = 'processed'
    embeddings_file = os.path.join(processed_dir, 'embeddings.csv')
    
    if not os.path.exists(embeddings_file):
        print("Embeddings file not found. Running data processing and embedding generation...")
        process_data_and_generate_embeddings()
    
    df = pd.read_csv(embeddings_file)
    df['embeddings'] = df['embeddings'].apply(eval)
    return df

def process_data_and_generate_embeddings():
    # Create necessary directories
    os.makedirs('text', exist_ok=True)
    os.makedirs('processed', exist_ok=True)

    # Crawl the website
    crawl(FULL_URL)

    # Process and prepare data
    texts = []
    for file in os.listdir(f'text/{DOMAIN}/'):
        with open(f'text/{DOMAIN}/{file}', 'r', encoding='UTF-8') as f:
            text = f.read()
            texts.append((file, text))

    df = pd.DataFrame(texts, columns=['fname', 'text'])
    df['text'] = remove_newlines(df['text'])
    df.to_csv('processed/scraped.csv')

    # Tokenize and split long texts
    tokenizer = tiktoken.get_encoding('cl100k_base')
    data = pd.read_csv('processed/scraped.csv')
    data['n_tokens'] = data['text'].apply(lambda x: len(tokenizer.encode(x)))

    shortened = []
    for row in data.itertuples():
        if row.text is not None:
            if row.n_tokens > MAX_TOKENS:
                shortened += split_into_many(row.text)
            else:
                shortened.append(row.text)

    df = pd.DataFrame(shortened, columns=['text'])
    df['n_tokens'] = df['text'].apply(lambda x: len(tokenizer.encode(x)))

    # Generate embeddings
    df['embeddings'] = df['text'].apply(lambda x: client.embeddings.create(input=x, model='text-embedding-ada-002').data[0].embedding)
    df.to_csv('processed/embeddings.csv')

    print("Data processing and embedding generation completed.")

# Main execution
def main():
    try:
        # Test SSL verification
        content = get_url_content(FULL_URL)
        print("Successfully accessed the website")
    except Exception as e:
        print(f"Error accessing the website: {e}")

    # Load data (this will process and generate embeddings if necessary)
    load_data()

if __name__ == '__main__':
    main()