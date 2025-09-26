import chromadb
from typing import List, Dict

DB_PATH = "chroma_db"
COLLECTION_NAME = "company_documents"

class VectorStore:
    """A wrapper class for ChromaDB to manage document storage and retrieval."""
    
    def __init__(self, path: str = DB_PATH, collection_name: str = COLLECTION_NAME):
        """
        Initializes the VectorStore.
        
        Args:
            path: The directory to store the ChromaDB data.
            collection_name: The name of the collection to use.
        """
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def add_documents(self, chunks: List[str], embeddings: List[List[float]], metadatas: List[Dict]):
        """
        Adds documents, their embeddings, and metadata to the collection.
        """
        if not chunks:
            return

        ids = [f"{meta['file_id']}-chunk{i}" for i, meta in enumerate(metadatas)]

        self.collection.add(
            embeddings=embeddings,
            documents=chunks,
            metadatas=metadatas,
            ids=ids
        )

    def query(self, query_embedding: List[float], n_results: int = 5) -> Dict:
        """
        Queries the collection for the most similar documents.
        """
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

    def get_count(self) -> int:
        """Returns the total number of documents in the collection."""
        return self.collection.count()

vector_store_instance = VectorStore()
