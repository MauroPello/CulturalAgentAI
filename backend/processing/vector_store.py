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

    def get_processed_documents(self) -> List[Dict]:
        """
        Returns a list of unique documents that have been processed and stored.
        Returns metadata for each unique filename.
        """
        try:
            # Get all items from the collection (without embeddings to save memory)
            results = self.collection.get(include=['metadatas'])
            
            if not results or not results.get('metadatas'):
                return []
            
            # Group by filename to get unique documents
            unique_docs = {}
            for metadata in results['metadatas']:
                filename = metadata.get('filename')
                file_id = metadata.get('file_id')
                
                if filename and filename not in unique_docs:
                    unique_docs[filename] = {
                        'filename': filename,
                        'file_id': file_id,
                        'file_type': self._get_file_extension(filename),
                        'chunk_count': 0
                    }
                
                if filename:
                    unique_docs[filename]['chunk_count'] += 1
            
            return list(unique_docs.values())
        except Exception as e:
            print(f"Error getting processed documents: {e}")
            return []
    
    def _get_file_extension(self, filename: str) -> str:
        """Extract file extension from filename."""
        if '.' in filename:
            return '.' + filename.split('.')[-1].lower()
        return ''

    def delete_document_by_filename(self, filename: str) -> bool:
        """
        Delete all chunks of a document by filename.
        Returns True if document was found and deleted, False otherwise.
        """
        try:
            # Get all items to find the ones with the matching filename
            results = self.collection.get(include=['metadatas'])
            
            if not results or not results.get('metadatas'):
                return False
            
            # Find IDs of chunks belonging to this filename
            ids_to_delete = []
            for i, metadata in enumerate(results['metadatas']):
                if metadata.get('filename') == filename:
                    ids_to_delete.append(results['ids'][i])
            
            if ids_to_delete:
                self.collection.delete(ids=ids_to_delete)
                print(f"Deleted {len(ids_to_delete)} chunks for document: {filename}")
                return True
            else:
                print(f"No document found with filename: {filename}")
                return False
                
        except Exception as e:
            print(f"Error deleting document {filename}: {e}")
            return False

    def clear_all_documents(self) -> bool:
        """
        Delete all documents from the vector store.
        Returns True if successful, False otherwise.
        """
        try:
            # Get all items
            results = self.collection.get(include=['metadatas'])
            
            if not results or not results.get('ids'):
                print("No documents to delete")
                return True
            
            # Delete all items
            self.collection.delete(ids=results['ids'])
            print(f"Deleted all {len(results['ids'])} chunks from vector store")
            return True
            
        except Exception as e:
            print(f"Error clearing all documents: {e}")
            return False

vector_store_instance = VectorStore()
