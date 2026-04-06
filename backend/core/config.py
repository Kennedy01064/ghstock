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
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-for-dev")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    SQLALCHEMY_DATABASE_URL: str = os.getenv("DATABASE_URL", DEFAULT_SQLITE_URL)
    REDIS_URL: str = os.getenv("REDIS_URL", DEFAULT_REDIS_URL)


    BACKEND_CORS_ORIGINS: list = ["*"]

settings = Settings()
