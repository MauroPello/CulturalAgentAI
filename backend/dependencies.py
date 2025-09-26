from functools import lru_cache
from fastapi import Depends
from config import settings
from services.llm_services import LLMService
from services.rag_service import RAGService
from services.web_search_service import WebSearchService
from services.query_router import QueryRouter

@lru_cache()
def get_llm_service():
    return LLMService(
        api_key=settings.public_ai_key,
        model=settings.llm_model
    )

@lru_cache()
def get_rag_service():
    return RAGService()

@lru_cache()  
def get_web_search_service():
    return WebSearchService(
        api_key=settings.google_search_api_key,
        engine_id=settings.google_search_engine_id
    )

def get_query_router(
    llm_service: LLMService = Depends(get_llm_service),
    rag_service: RAGService = Depends(get_rag_service),
    web_search_service: WebSearchService = Depends(get_web_search_service)
) -> QueryRouter:
    """
    Dependency injector for the QueryRouter.
    Initializes and returns a QueryRouter instance with all its required services.
    """
    return QueryRouter(
        llm_service=llm_service,
        rag_service=rag_service,
        web_search_service=web_search_service,
        confidence_threshold=settings.router_confidence_threshold
    )