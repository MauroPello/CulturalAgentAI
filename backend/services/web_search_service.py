import httpx
from typing import List
from models.schemas import SearchResult

class WebSearchService:
    def __init__(self, api_key: str, engine_id: str):
        self.api_key = api_key
        self.engine_id = engine_id
    
    async def search(self, query: str, num_results: int = 5) -> List[SearchResult]:
        """Search the web using Google Custom Search API"""
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'key': self.api_key,
            'cx': self.engine_id,
            'q': query,
            'num': min(num_results, 10)  # Google API limit
        }
        
        try:
            # Use httpx for async HTTP requests
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
            
            results = []
            for item in data.get('items', []):
                results.append(SearchResult(
                    source="web",
                    title=item.get('title', ''),
                    content=item.get('snippet', ''),
                    url=item.get('link', ''),
                    relevance_score=None  # Google doesn't provide scores
                ))
            
            return results
        except httpx.HTTPError as e:
            raise Exception(f"Web search error: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected web search error: {str(e)}")