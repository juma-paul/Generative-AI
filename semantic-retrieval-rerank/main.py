import os
import weaviate
from dotenv import load_dotenv 
from weaviate.classes.init import Auth 
from weaviate.config import AdditionalConfig

from utils.search import dense_retrieval, keyword_search
from utils.rerank import rerank_responses
from utils.print_utils import print_result, print_reranked_results

def main():

    """Main entry point for the project."""

    # Load environment variables
    load_dotenv()

    # Weaviate connection configuration
    wcd_url = os.getenv('weaviate_api_url') 
    wcd_api_key = os.getenv('weaviate_api_key') 
    openai_api_key = os.getenv('openai_api_key')
    cohere_api_key = os.getenv('cohere_api_key')

    # Set timeout for Weaviate
    timeout_config = {"http": 360}

    # Connect to Weaviate
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=wcd_url,
        auth_credentials=Auth.api_key(wcd_api_key),
        headers={
            'X-OpenAI-Api-key': openai_api_key,
            'X-Cohere-Api-Key': cohere_api_key
        },
        skip_init_checks=True,
        additional_config=AdditionalConfig(timeout=timeout_config)
    )

    print(f"Connected to Weaviate? {client.is_ready()}")

    try:
        # Perform Dense Retrieval Test
        query = input("Enter a question for Dense Retrieval: ")
        dense_results = dense_retrieval(query, client)
        print_result(dense_results, "Dense Retrieval Results")

        if dense_results:
            # Extract answers for reranking
            dense_rerank_texts = [r.get("answer", "").strip() for r in dense_results if r.get("answer")]

            # Call the rerank function
            reranked_dense_results = rerank_responses(api_key=cohere_api_key, query=query, docs=dense_rerank_texts)

            # Print the reranked results
            print_reranked_results(reranked_dense_results, "Reranked Dense Retrieval")

        # Perform Keyword Search Test
        query_keyword = input("\nEnter a question for Keyword Search: ")
        keyword_results = keyword_search(query_keyword, client)
        print_result(keyword_results, "Keyword Search Results")

        if keyword_results:
            # Extract answers for reranking
            keyword_rerank_texts = [r.get("answer", "").strip() for r in keyword_results if r.get("answer")]

            # Call the rerank function
            reranked_keyword_results = rerank_responses(api_key=cohere_api_key, query=query_keyword, docs=keyword_rerank_texts)

            # Print the reranked results
            print_reranked_results(reranked_keyword_results, "Reranked Keyword Search")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Ensure the client connection is closed
        client.close()

if __name__ == "__main__":
    main()

