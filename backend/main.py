from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from backend.api.v1.api import api_router
from backend.core.config import settings
from backend.core.logging_middleware import LoggingMiddleware
from backend.core import exceptions
from backend.db.runtime_schema import ensure_runtime_schema

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
)

# Exception handlers
from backend.domain.errors import DomainError
app.add_exception_handler(DomainError, exceptions.domain_exception_handler)
app.add_exception_handler(SQLAlchemyError, exceptions.sqlalchemy_exception_handler)
app.add_exception_handler(Exception, exceptions.generic_exception_handler)

# Middleware
app.add_middleware(LoggingMiddleware)

# Set all CORS enabled origins
if settings.cors_origins_list:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix="/api/v1")
app.mount("/static/uploads", StaticFiles(directory="uploads"), name="static_uploads")


@app.on_event("startup")
def startup_event():
    ensure_runtime_schema()


@app.get("/")
def read_root():
    return {"message": "Welcome to Stock API v2.0"}

@app.get("/health")
def health_check():
    from supabase import create_client, Client
    # Initialize Supabase client if credentials are provided
    supabase_client: Client = None
    supabase_error: str = None
    if settings.SUPABASE_URL and settings.SUPABASE_SERVICE_KEY:
        try:
            supabase_client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)
            print("✅ Supabase Storage client initialized successfully")
        except Exception as e:
            supabase_error = str(e)
            print(f"⚠️ Failed to initialize Supabase client: {supabase_error}")
            supabase_client = None
    return {
        "status": "healthy",
        "supabase_configured": supabase_client is not None,
        "supabase_error": supabase_error,
        "url_len": len(settings.SUPABASE_URL),
        "key_len": len(settings.SUPABASE_SERVICE_KEY),
        "bucket": settings.SUPABASE_BUCKET,
        "environment": settings.ENVIRONMENT,
        "version_tag": "v2.0.debug.strip_applied_1223"
    }
