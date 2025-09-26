"""
SwissAI Gantt Planner FastAPI Application
Self-contained API service for Gantt planning using Public AI
"""

import os
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .models import GanttRequest, APIGanttResponse
from .planner import SwissAIGanttPlanner, create_planner


# FastAPI App Setup
app = FastAPI(
    title="SwissAI Gantt Planner API",
    description="Convert business plan descriptions into structured Gantt chart JSON using Swiss-AI Apertus model",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_planner() -> SwissAIGanttPlanner:
    """Dependency to get planner instance."""
    try:
        return create_planner()
    except ValueError as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Configuration error: {str(e)}"
        )


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "service": "SwissAI Gantt Planner API",
        "version": "1.0.0",
        "description": "Convert business descriptions to structured Gantt plans",
        "endpoints": {
            "/": "API information",
            "/health": "Health check",
            "/convert": "POST - Convert business description to Gantt plan",
            "/docs": "Interactive API documentation",
            "/redoc": "ReDoc documentation"
        },
        "model": "swiss-ai/apertus-8b-instruct",
        "provider": "publicai.co"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        # Try to create planner to verify configuration
        planner = get_planner()
        config_status = "healthy"
    except Exception as e:
        config_status = f"configuration error: {str(e)}"
    
    return {
        "status": "healthy" if config_status == "healthy" else "degraded",
        "service": "SwissAI Gantt Planner",
        "model": "swiss-ai/apertus-8b-instruct",
        "api_provider": "publicai.co",
        "configuration": config_status,
        "timestamp": datetime.now().isoformat()
    }


@app.post("/convert", response_model=APIGanttResponse)
async def convert_to_gantt(
    request: GanttRequest, 
    planner: SwissAIGanttPlanner = Depends(get_planner)
):
    """
    Convert a business plan description to a structured Gantt chart JSON.
    
    - **description**: Text describing the business plan or project
    - **project_name**: Optional project name to use in the output
    """
    start_time = datetime.now()
    
    try:
        # Validate input
        if not request.description.strip():
            raise HTTPException(status_code=400, detail="Description cannot be empty")
        
        # Generate Gantt plan
        gantt_data = planner.generate_gantt_plan(
            description=request.description, 
            project_name=request.project_name
        )
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return APIGanttResponse(
            success=True,
            gantt_plan=gantt_data,
            processing_time_seconds=processing_time,
            timestamp=datetime.now()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        processing_time = (datetime.now() - start_time).total_seconds()
        return APIGanttResponse(
            success=False,
            error=str(e),
            processing_time_seconds=processing_time,
            timestamp=datetime.now()
        )


@app.exception_handler(500)
async def internal_server_error_handler(request, exc):
    """Handle internal server errors."""
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "detail": str(exc) if app.debug else "An unexpected error occurred",
            "timestamp": datetime.now().isoformat()
        }
    )


# Health check for external monitoring
@app.get("/ping")
async def ping():
    """Simple ping endpoint for monitoring."""
    return {"status": "ok", "timestamp": datetime.now().isoformat()}


if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting SwissAI Gantt Planner API...")
    print("📊 Model: swiss-ai/apertus-8b-instruct")
    print("🌐 Server will be available at: http://localhost:8001")
    print("📖 API Documentation: http://localhost:8001/docs")
    print("❤️  Health Check: http://localhost:8001/health")
    print("\n" + "="*50)
    
    uvicorn.run(
        "api.gantt.app:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )