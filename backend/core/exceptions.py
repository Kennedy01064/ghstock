from fastapi import Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger("backend")

async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    logger.exception(exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Database error occurred", "type": "SQLAlchemyError"}
    )

from backend.domain.errors import (
    DomainError, ResourceNotFoundError, 
    InsufficientStockError, DomainConflictError, 
    UnauthorizedError
)

async def domain_exception_handler(request: Request, exc: DomainError):
    logger.warning(f"Domain error: {exc.message}")
    
    status_code = status.HTTP_400_BAD_REQUEST
    if isinstance(exc, ResourceNotFoundError):
        status_code = status.HTTP_404_NOT_FOUND
    elif isinstance(exc, InsufficientStockError):
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    elif isinstance(exc, DomainConflictError):
        status_code = status.HTTP_409_CONFLICT
    elif isinstance(exc, UnauthorizedError):
        status_code = status.HTTP_403_FORBIDDEN

    return JSONResponse(
        status_code=status_code,
        content={"detail": exc.message, "type": type(exc).__name__}
    )

async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception(exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected error occurred", "type": str(type(exc).__name__)}
    )
