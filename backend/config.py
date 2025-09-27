import os
from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import Optional

class Settings(BaseSettings):
    # API Keys - Required
    public_ai_key: str
    google_search_api_key: str
    google_search_engine_id: str  
    swiss_ai_platform_api_key: str
    
    # LLM settings
    llm_model: str = "swiss-ai/apertus-8b-instruct"  # MANDATORY: Must use apertus
    llm_temperature: float = 0.1
    llm_max_tokens: int = 1000
    
    # Service settings
    max_rag_results: int = 5
    max_web_results: int = 5
    router_confidence_threshold: float = 7.0
    
    # Server configuration
    server_host: str = "localhost"
    server_port: int = 8000
    debug_mode: bool = False
    
    # Database settings
    chroma_persist_directory: str = "./chroma_db"
    
    @field_validator('llm_temperature')
    @classmethod
    def validate_temperature(cls, v):
        if not 0.0 <= v <= 2.0:
            raise ValueError('Temperature must be between 0.0 and 2.0')
        return v
    
    @field_validator('llm_max_tokens')
    @classmethod
    def validate_max_tokens(cls, v):
        if v < 1 or v > 8192:
            raise ValueError('Max tokens must be between 1 and 8192')
        return v
    
    @field_validator('router_confidence_threshold')
    @classmethod
    def validate_confidence_threshold(cls, v):
        if not 0.0 <= v <= 10.0:
            raise ValueError('Confidence threshold must be between 0.0 and 10.0')
        return v
    
    @field_validator('max_rag_results', 'max_web_results')
    @classmethod
    def validate_max_results(cls, v):
        if v < 1 or v > 20:
            raise ValueError('Max results must be between 1 and 20')
        return v
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": False
    }
    
    def validate_required_keys(self):
        """Validate that all required API keys are set and not empty"""
        required_keys = [
            'public_ai_key',
            'google_search_api_key', 
            'google_search_engine_id',
            'swiss_ai_platform_api_key'
        ]
        
        missing_keys = []
        empty_keys = []
        
        for key in required_keys:
            value = getattr(self, key, None)
            if value is None:
                missing_keys.append(key.upper())
            elif not value.strip():
                empty_keys.append(key.upper())
        
        if missing_keys:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_keys)}")
        
        if empty_keys:
            raise ValueError(f"Empty required environment variables: {', '.join(empty_keys)}")

# Initialize settings with validation
try:
    settings = Settings()
    settings.validate_required_keys()
except Exception as e:
    print(f"❌ Configuration Error: {e}")
    print("Please check your .env file and ensure all required environment variables are set.")
    raise