import cohere
import os

from dotenv import load_dotenv

load_dotenv()

cohere_api_key = os.getenv('cohere_api_key')

co = cohere.ClientV2(api_key=cohere_api_key)  

def rerank_responses(api_key, query, docs, model="rerank-v3.5", top_n=3):
    """
    Use the Cohere rerank API to rank documents based on relevance to a query.

    Args:
        api_key (str): Cohere API key.
        query (str): Query string to rank the documents against.
        docs (list): List of documents to rank.
        model (str): Cohere rerank model name. Default is 'rerank-v3.5'.
        top_n (int): Number of top results to return.

    Returns:
        list: List of dictionaries containing ranked results with index, document, and relevance score.
    """
    # Initialize the Cohere client
    co = cohere.ClientV2(api_key=api_key)

    # Call the rerank API
    response = co.rerank(model=model, query=query, documents=docs, top_n=top_n)

    # Extract and return results
    reranked_results = [
        {
            "index": result.index,
            "document": docs[result.index],
            "score": result.relevance_score,
        }
        for result in response.results
    ]

    return reranked_results

    



