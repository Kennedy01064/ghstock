from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from backend.api.v1.api import api_router
from backend.core.config import settings
from backend.core.logging_middleware import LoggingMiddleware
from backend.core import exceptions

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
)

# Exception handlers
app.add_exception_handler(SQLAlchemyError, exceptions.sqlalchemy_exception_handler)
app.add_exception_handler(Exception, exceptions.generic_exception_handler)

# Middleware
app.add_middleware(LoggingMiddleware)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to Stock API v2.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

