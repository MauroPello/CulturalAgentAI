import httpx
from typing import List
from models.schemas import SearchResult
from bs4 import BeautifulSoup
import asyncio

class WebSearchService:
    def __init__(self, api_key: str, engine_id: str):
        self.api_key = api_key
        self.engine_id = engine_id
    
    async def _scrape_page_content(self, url: str, client: httpx.AsyncClient) -> str:
        """Asynchronously scrapes the text content from a single URL."""
        try:
            response = await client.get(url, follow_redirects=True, timeout=10.0)
            response.raise_for_status()
            
            # Use BeautifulSoup to parse HTML and extract text
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script_or_style in soup(['script', 'style']):
                script_or_style.decompose()
            
            # Get text and clean it up
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = "\n".join(chunk for chunk in chunks if chunk)
            
            # Limit content to a reasonable length to avoid excessive token usage
            return text[:4000]
        except Exception as e:
            print(f"Warning: Failed to scrape {url}. Reason: {str(e)}")
            return "" # Return empty string on failure

    async def search(self, query: str, num_results: int = 3) -> List[SearchResult]:
        """Search the web, then scrape the top results for content."""
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'key': self.api_key,
            'cx': self.engine_id,
            'q': query,
            'num': min(num_results, 10)
        }
        
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                # Step 1: Get search results from Google API
                api_response = await client.get(url, params=params)
                api_response.raise_for_status()
                search_data = api_response.json()

                initial_results = search_data.get('items', [])
                if not initial_results:
                    return []

                # Step 2: Asynchronously scrape content for each result
                scraping_tasks = [
                    self._scrape_page_content(item.get('link', ''), client) 
                    for item in initial_results
                ]
                scraped_contents = await asyncio.gather(*scraping_tasks)

                # Step 3: Combine search results with scraped content
                final_results = []
                for item, scraped_content in zip(initial_results, scraped_contents):
                    # Use the scraped content if available, otherwise fall back to the snippet
                    content = scraped_content if scraped_content else item.get('snippet', '')
                    
                    final_results.append(SearchResult(
                        source="web",
                        title=item.get('title', ''),
                        content=content,
                        url=item.get('link', ''),
                        relevance_score=None
                    ))
            
            return final_results
        except httpx.HTTPError as e:
            raise Exception(f"Web search API error: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected web search error: {str(e)}")
