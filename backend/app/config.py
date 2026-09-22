import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    PROJECT_NAME: str = "Perfect Saturday Planner"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api"
    
    # Environment & Secrets
    GROQ_API_KEY: Optional[str] = None
    DATABASE_URL: str = "sqlite:///./saturday_planner.db"
    FRONTEND_URL: str = "http://localhost:5173"
    GROQ_MODEL: str = "openai/gpt-oss-120b"
    
    # Flags
    DEBUG: bool = True
    USE_PGVECTOR: bool = False

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
