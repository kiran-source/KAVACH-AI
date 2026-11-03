# Kavach AI - Backend Configuration

import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "KAVACH AI"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./kavach.db")
    GNANI_API_KEY: str = os.getenv("GNANI_API_KEY", "mock_key")
    GNANI_PRISMA_ENDPOINT: str = os.getenv("GNANI_PRISMA_ENDPOINT", "https://api.gnani.ai/v1/speech-to-text")
    GNANI_TIMBRE_ENDPOINT: str = os.getenv("GNANI_TIMBRE_ENDPOINT", "https://api.gnani.ai/v1/text-to-speech")
    DEMO_MODE: bool = os.getenv("DEMO_MODE", "true").lower() == "true"
    MAX_UPLOAD_SIZE_MB: int = int(os.getenv("MAX_UPLOAD_SIZE_MB", "25"))
    RETENTION_DAYS: int = int(os.getenv("RETENTION_DAYS", "7"))
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
