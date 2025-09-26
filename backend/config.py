from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API Keys
    public_ai_key: str
    google_search_api_key: str
    google_search_engine_id: str
    swiss_ai_platform_api_key: str  
    
    # LLM settings
    llm_model: str = "swiss-ai/apertus-8b-instruct"
    llm_temperature: float = 0.1
    llm_max_tokens: int = 1000
    
    # Service settings
    max_rag_results: int = 5
    max_web_results: int = 5
    router_confidence_threshold: float = 7.0
    
    class Config:
        env_file = ".env"

settings = Settings()