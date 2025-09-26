"""
Configuration settings for SwissAI Gantt Planner API
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    """Application settings."""
    
    # API Configuration
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8001"))
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "info")
    
    # Public AI Configuration
    PUBLIC_AI_API_KEY: Optional[str] = os.getenv("PUBLIC_AI_API_KEY")
    PUBLIC_AI_API_URL: str = os.getenv("PUBLIC_AI_API_URL", "https://api.publicai.co/v1/chat/completions")
    PUBLIC_AI_MODEL: str = os.getenv("PUBLIC_AI_MODEL", "swiss-ai/apertus-8b-instruct")
    
    # API Configuration
    API_TITLE: str = "SwissAI Gantt Planner API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "Convert business plan descriptions into structured Gantt charts"
    
    # Request Configuration
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "4000"))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.0"))
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "60"))
    
    @classmethod
    def validate(cls):
        """Validate required settings."""
        if not cls.PUBLIC_AI_API_KEY:
            raise ValueError("PUBLIC_AI_API_KEY is required")


# Global settings instance
settings = Settings()