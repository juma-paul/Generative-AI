def dense_retrieval(query, client, collection_name="MarcusAurelius"):
    """Perform dense retrieval using Weaviate"""
    try:
        # Use the new collection-based query method
        collection = client.collections.get(collection_name)
        response = collection.query.near_text(
            query=query,
            limit=3
        )
        
        # Convert the results to a list of dictionaries
        return [
            {
                "question": result.properties.get('question', ''),
                "answer": result.properties.get('answer', ''),
                "category": result.properties.get('category', '')
            }
            for result in response.objects
        ]
    
    except Exception as e:
        print(f"Error in dense_retrieval: {e}")
        return []

def keyword_search(query, client, collection_name="MarcusAurelius", properties=None, num_results=3):
    """Perform keyword search using Weaviate's BM25"""
    try:
        # Use the new collection-based query method
        collection = client.collections.get(collection_name)
        response = collection.query.bm25(
            query=query,
            limit=num_results
        )
        
        # Convert the results to a list of dictionaries
        return [
            {
                "question": result.properties.get('question', ''),
                "answer": result.properties.get('answer', ''),
                "category": result.properties.get('category', '')
            }
            for result in response.objects
        ]
    
    except Exception as e:
        print(f"Error in keyword_search: {e}")
        return []