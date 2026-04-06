import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[2]
DEFAULT_SQLITE_URL = f"sqlite:///{(BASE_DIR / 'stock_local.db').as_posix()}"
DEFAULT_REDIS_URL = "redis://localhost:6379/0"

class Settings(BaseSettings):
    PROJECT_NAME: str = "Stock API"
    PROJECT_VERSION: str = "1.0.0"
    
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "local")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-for-dev")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    SQLALCHEMY_DATABASE_URL: str = os.getenv("DATABASE_URL", DEFAULT_SQLITE_URL)
    REDIS_URL: str = os.getenv("REDIS_URL", DEFAULT_REDIS_URL)

    # Security & Observability
    AUDIT_LOG_ENABLED: bool = os.getenv("AUDIT_LOG_ENABLED", "true").lower() == "true"
    
    # CORS
    BACKEND_CORS_ORIGINS: str = os.getenv(
        "BACKEND_CORS_ORIGINS",
        "http://localhost:5173,http://localhost:8000,http://127.0.0.1:5173" if os.getenv("ENVIRONMENT", "local") == "local" else ""
    )

    @property
    def cors_origins_list(self) -> list[str]:
        if not self.BACKEND_CORS_ORIGINS:
            return []
        if self.BACKEND_CORS_ORIGINS == "*":
            return ["*"]
        return [origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(",") if origin.strip()]

    def validate_production(self):
        if self.ENVIRONMENT == "production" and self.SECRET_KEY == "your-secret-key-for-dev":
            raise ValueError("SECURITY ALERT: SECRET_KEY must be set in production environment!")

settings = Settings()
settings.validate_production()
