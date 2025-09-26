import chromadb
from typing import List, Dict

# Setup a persistent client. Data will be stored in the 'chroma_db' directory.
client = chromadb.PersistentClient(path="chroma_db")

# The collection is where you'll store the vectors.
# You can think of it like a table in a SQL database.
# We'll use a default name, but you could make this customer-specific.
COLLECTION_NAME = "company_documents"
collection = client.get_or_create_collection(name=COLLECTION_NAME)

def add_documents_to_store(chunks: List[str], embeddings: List[List[float]], metadata: List[Dict]):
    """
    Adds chunks, their embeddings, and metadata to the ChromaDB collection.
    Generates unique IDs for each chunk.
    """
    if not chunks:
        return

    # ChromaDB requires unique IDs for each document. We can generate them.
    # Here, we'll use the metadata's file_id and the chunk index.
    ids = [f"{meta['file_id']}-chunk{i}" for i, meta in enumerate(metadata)]

    collection.add(
        embeddings=embeddings,
        documents=chunks,
        metadatas=metadata,
        ids=ids
    )

def get_document_count() -> int:
    """Returns the total number of documents in the collection."""
    return collection.count()