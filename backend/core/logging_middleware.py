import time
import uuid
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("backend")
logging.basicConfig(level=logging.INFO)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Generate or capture correlation ID
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        
        # Attach to request state for access in endpoints/services if needed
        request.state.request_id = request_id
        
        start_time = time.time()
        
        try:
            response = await call_next(request)
        except Exception as e:
            process_time = time.time() - start_time
            logger.error(
                f"RID: {request_id} | "
                f"Method: {request.method} Path: {request.url.path} | "
                f"ERROR: {str(e)} | Duration: {process_time:.4f}s"
            )
            raise e
            
        process_time = time.time() - start_time
        
        # Log summary
        logger.info(
            f"RID: {request_id} | "
            f"Method: {request.method} Path: {request.url.path} | "
            f"Status: {response.status_code} | Duration: {process_time:.4f}s"
        )
        
        # Add headers for client-side correlation
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = str(process_time)
        return response
