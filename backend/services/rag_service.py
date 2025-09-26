from typing import List, Optional
from models.schemas import SearchResult
from processing.embedder import embed_chunks
from processing.vector_store import vector_store_instance

class RAGService:
    def __init__(self):
        self.vector_store = vector_store_instance
    
    async def search(self, query: str, top_k: int = 5) -> List[SearchResult]:
        """Search through RAG documents"""
        try:
            # Embed the query using your existing embedder
            query_embedding = embed_chunks([query])[0]
            
            # Query your existing vector store
            results = self.vector_store.query(
                query_embedding=query_embedding,
                n_results=top_k
            )
            
            # Convert to SearchResult format
            search_results = []
            if results and results.get('documents') and results['documents'][0]:
                documents = results['documents'][0]
                metadatas = results.get('metadatas', [[{}] * len(documents)])[0]
                distances = results.get('distances', [[0] * len(documents)])[0]
                
                for i, (doc, metadata, distance) in enumerate(zip(documents, metadatas, distances)):
                    # Convert distance to similarity score (lower distance = higher similarity)
                    similarity_score = max(0, 1 - distance) if distance is not None else 0.5
                    
                    search_results.append(SearchResult(
                        source="rag",
                        title=metadata.get('filename', f'Document {i+1}'),
                        content=doc,
                        url=None,  # RAG documents don't have URLs
                        relevance_score=similarity_score
                    ))
            
            return search_results
            
        except Exception as e:
            print(f"RAG search error: {str(e)}")
            return []
    
    async def quick_search(self, query: str) -> Optional[float]:
        """Quick similarity check without full retrieval"""
        try:
            # Do a quick search with just 1 result to get similarity
            query_embedding = embed_chunks([query])[0]
            results = self.vector_store.query(
                query_embedding=query_embedding,
                n_results=1
            )
            
            if results and results.get('distances') and results['distances'][0]:
                distance = results['distances'][0][0]
                # Convert distance to similarity score
                similarity = max(0, 1 - distance) if distance is not None else 0
                return similarity
            
            return 0.0
            
        except Exception as e:
            print(f"Quick search error: {str(e)}")
            return None