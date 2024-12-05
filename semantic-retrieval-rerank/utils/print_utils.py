def print_result(result, title="Results"):
    """ Print results with formatted output """
    print(f"\n--- {title} ---")
    for i, item in enumerate(result, 1):
        print(f"Result {i}:")
        for key, value in item.items():
            print(f"{key.capitalize()}: {value}")
        print()

def print_reranked_results(reranked_results, header="Reranked Results"):
    """
    Print reranked results with relevance scores.

    Args:
        reranked_results (list): List of reranked results with details.
        header (str): Header to display above results.
    """
    print(f"\n--- {header} ---")
    if not reranked_results:
        print("No reranked results found.")
        return

    for i, result in enumerate(reranked_results):
        print(f"Reranked Result {i + 1}:")
        print(f"  Document: {result['document']}")
        print(f"  Relevance Score: {result['score']:.4f}")
        print()

    # Display the top-ranked document
    print("\nTop Ranked Document:")
    top_result = reranked_results[0]
    print(f"  Document: {top_result['document']}")
    print(f"  Relevance Score: {top_result['score']:.4f}")



