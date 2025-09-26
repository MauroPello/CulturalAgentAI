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
    
    # Swiss AI Platform Configuration
    SWISS_AI_PLATFORM_API_KEY: Optional[str] = os.getenv("SWISS_AI_PLATFORM_API_KEY")
    SWISS_AI_PLATFORM_API_URL: str = os.getenv("SWISS_AI_PLATFORM_API_URL", "https://api.swisscom.com/layer/swiss-ai-weeks/apertus-70b/v1")
    SWISS_AI_MODEL: str = os.getenv("SWISS_AI_MODEL", "swiss-ai/Apertus-70B")
    
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
        if not cls.SWISS_AI_PLATFORM_API_KEY:
            raise ValueError("SWISS_AI_PLATFORM_API_KEY is required")


# Global settings instance
settings = Settings()