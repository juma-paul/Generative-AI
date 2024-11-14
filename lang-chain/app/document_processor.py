from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
import os

class DocumentProcessor:
    def __init__(self, config):
        self.config = config
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP
        )
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=config.OPENAI_API_KEY
        )
    
    def load_document(self, file_path):
        _, ext = os.path.splitext(file_path)
        if ext.lower() == '.pdf':
            loader = PyPDFLoader(file_path)
        else:
            loader = TextLoader(file_path)
        return loader.load()
    
    def process_document(self, document):
        chunks = self.text_splitter.split_documents(document)
        return chunks
    
    def generate_embeddings(self, chunks):
        return self.embeddings.embed_documents([chunk.page_content for chunk in chunks])