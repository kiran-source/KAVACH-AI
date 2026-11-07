# Kavach AI - Backend Configuration
import os
import sys
from pathlib import Path
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

# Canonical environment path: always resolves to <repo>/backend/.env
CONFIG_DIR = Path(__file__).resolve().parent
BACKEND_DIR = CONFIG_DIR.parent.parent
CANONICAL_ENV_PATH = (BACKEND_DIR / ".env").resolve()
FALLBACK_ROOT_ENV_PATH = (BACKEND_DIR.parent / ".env").resolve()

# Determine which env file exists
RESOLVED_ENV_FILE = str(CANONICAL_ENV_PATH) if CANONICAL_ENV_PATH.exists() else str(FALLBACK_ROOT_ENV_PATH)

class Settings(BaseSettings):
    PROJECT_NAME: str = "KAVACH AI"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./kavach.db")
    GNANI_API_KEY: str = os.getenv("GNANI_API_KEY", "")
    GNANI_PRISMA_ENDPOINT: str = os.getenv("GNANI_PRISMA_ENDPOINT", "https://api.vachana.ai/stt/v3")
    GNANI_TIMBRE_ENDPOINT: str = os.getenv("GNANI_TIMBRE_ENDPOINT", "https://api.vachana.ai/api/v1/tts/inference")
    DEMO_MODE: bool = os.getenv("DEMO_MODE", "false").lower() == "true"
    MAX_UPLOAD_SIZE_MB: int = int(os.getenv("MAX_UPLOAD_SIZE_MB", "25"))
    RETENTION_DAYS: int = int(os.getenv("RETENTION_DAYS", "7"))
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8000"))
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ]

    def get_allowed_origins(self) -> List[str]:
        env_origins = os.getenv("ALLOWED_ORIGINS")
        if env_origins:
            return [o.strip() for o in env_origins.split(",") if o.strip()]
        return self.ALLOWED_ORIGINS

    model_config = SettingsConfigDict(
        env_file=RESOLVED_ENV_FILE,
        extra="ignore"
    )

    def is_api_key_configured(self) -> bool:
        """Returns True if a real, non-placeholder API key is set."""
        k = (self.GNANI_API_KEY or "").strip()
        return bool(k and k not in ["mock_key", "mock_gnani_api_key_for_testing", "YOUR_ACTUAL_API_KEY"])

    def validate_runtime_mode(self) -> None:
        """
        Validates that if Real API Mode (DEMO_MODE=false) is configured,
        a real API key is present. Does not allow silently starting in demo mode.
        Skipped during automated pytest runs to allow mocked tests.
        """
        if (
            "pytest" in sys.modules or 
            os.getenv("PYTEST_CURRENT_TEST") or 
            os.getenv("TESTING", "").lower() == "true" or
            any("pytest" in str(arg).lower() for arg in sys.argv)
        ):
            return
        if not self.DEMO_MODE and not self.is_api_key_configured():
            raise RuntimeError(
                "CRITICAL CONFIGURATION ERROR: DEMO_MODE is set to 'false' (Real API Mode), "
                f"but no valid GNANI_API_KEY was found in canonical configuration '{CANONICAL_ENV_PATH}'. "
                "The application will not silently fall back to mock data when real mode is requested. "
                "To fix: Provide a valid GNANI_API_KEY in backend/.env, or set DEMO_MODE=true for local simulation."
            )

settings = Settings()
