from pydantic import BaseModel
from typing import List, Optional, Dict
from enum import Enum

class ChatMessage(BaseModel):
    role: str  # "user", "assistant", or "system"
    content: str

class ChatCompletionRequest(BaseModel):
    messages: List[ChatMessage]
    temperature: Optional[float] = 0.1
    max_tokens: Optional[int] = 512

class SearchStrategy(str, Enum):
    RAG = "RAG"
    WEB = "WEB"
    DIRECT = "DIRECT"
    HYBRID = "HYBRID"

class QueryAnalysis(BaseModel):
    strategy: SearchStrategy
    confidence: float
    backup_strategy: Optional[SearchStrategy] = None
    reasoning: str
    key_factors: List[str]
    temporal_indicators: List[str] = []
    internal_references: List[str] = []

class SearchResult(BaseModel):
    source: str  # "rag", "web", "direct"
    title: Optional[str] = None
    content: str
    url: Optional[str] = None
    relevance_score: Optional[float] = None

class IntelligentSearchRequest(BaseModel):
    query: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    force_strategy: Optional[SearchStrategy] = None

class IntelligentSearchResponse(BaseModel):
    query: str
    strategy_used: SearchStrategy
    confidence: float
    answer: str
    sources: List[SearchResult]
    analysis: QueryAnalysis
    execution_time: float
    tokens_used: int