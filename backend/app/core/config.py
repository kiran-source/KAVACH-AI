# Kavach AI - Backend Configuration
import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "KAVACH AI"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./kavach.db")
    GNANI_API_KEY: str = os.getenv("GNANI_API_KEY", "")
    GNANI_PRISMA_ENDPOINT: str = os.getenv("GNANI_PRISMA_ENDPOINT", "https://api.gnani.ai/v1/speech-to-text")
    GNANI_TIMBRE_ENDPOINT: str = os.getenv("GNANI_TIMBRE_ENDPOINT", "https://api.gnani.ai/v1/text-to-speech")
    DEMO_MODE: bool = os.getenv("DEMO_MODE", "true").lower() == "true"
    MAX_UPLOAD_SIZE_MB: int = int(os.getenv("MAX_UPLOAD_SIZE_MB", "25"))
    RETENTION_DAYS: int = int(os.getenv("RETENTION_DAYS", "7"))
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()
