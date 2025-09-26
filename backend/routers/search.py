import time
from fastapi import APIRouter, HTTPException, Depends
from models.schemas import *
from services.query_router import QueryRouter
from dependencies import get_query_router

router = APIRouter(prefix="/search", tags=["search"])

@router.post("/intelligent", response_model=IntelligentSearchResponse)
async def intelligent_search(
    request: IntelligentSearchRequest,
    query_router: QueryRouter = Depends(get_query_router)
):
    """
    Intelligent search endpoint that automatically determines whether to use
    RAG, web search, direct LLM response, or a hybrid approach.
    """
    start_time = time.time()
    total_tokens = 0
    
    try:
        # Reset token counter for this request
        query_router.llm_service.reset_token_counter()
        
        # Step 1: Analyze the query
        analysis = await query_router.analyze_query(request.query)
        
        # Step 2: Override strategy if requested
        if request.force_strategy:
            analysis.strategy = request.force_strategy
            analysis.confidence = 10.0
            analysis.reasoning = f"Strategy forced to {request.force_strategy.value}"
        
        # Step 3: Execute search
        results, actual_strategy = await query_router.execute_search(request.query, analysis)
        
        # Step 4: Generate final response
        answer, response_tokens = await query_router.generate_final_response(
            request.query, results, actual_strategy, analysis
        )
        
        execution_time = time.time() - start_time
        
        # Get total tokens used
        total_tokens = query_router.llm_service.get_total_tokens_used()
        
        return IntelligentSearchResponse(
            query=request.query,
            strategy_used=actual_strategy,
            confidence=analysis.confidence,
            answer=answer,
            sources=results,
            analysis=analysis,
            execution_time=execution_time,
            tokens_used=total_tokens
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@router.post("/analyze-query", response_model=QueryAnalysis)
async def analyze_query_only(
    query: str,
    query_router: QueryRouter = Depends(get_query_router)
):
    """
    Analyze a query without executing the search - useful for debugging
    """
    try:
        analysis = await query_router.analyze_query(query)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.get("/strategies")
async def get_available_strategies():
    """Get list of available search strategies"""
    return {
        "strategies": [strategy.value for strategy in SearchStrategy],
        "descriptions": {
            "RAG": "Search through uploaded documents and internal knowledge base",
            "WEB": "Search the internet for current information",
            "DIRECT": "Answer using the model's training knowledge only",
            "HYBRID": "Combine both RAG and web search results"
        }
    }

@router.get("/stats")
async def get_stats(query_router: QueryRouter = Depends(get_query_router)):
    """Get usage statistics"""
    return {
        "total_tokens_used": query_router.llm_service.get_total_tokens_used(),
        "model": query_router.llm_service.model
    }