import chromadb
from chromadb.config import Settings

class VectorStore:
    def __init__(self, config):
        self.client = chromadb.Client(Settings(
            persist_directory=config.VECTOR_DB_PATH
        ))
        self.collection = self.client.get_or_create_collection("documents")
    
    def add_documents(self, documents, embeddings):
        self.collection.add(
            documents=[doc.page_content for doc in documents],
            embeddings=embeddings,
            ids=[f"doc_{i}" for i in range(len(documents))]
        )
    
    def similarity_search(self, query_embedding, k=3):
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )
        return results