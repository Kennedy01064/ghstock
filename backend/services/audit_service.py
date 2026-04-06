import json
import logging
from datetime import datetime
from typing import Any, Optional
from fastapi import Request
from backend.core.config import settings

# Dedicated logger for audit events
audit_logger = logging.getLogger("audit")
audit_logger.setLevel(logging.INFO)

# Optional: Add a FileHandler for persistent audit logs if needed
# handler = logging.FileHandler("audit.log")
# audit_logger.addHandler(handler)

class AuditService:
    @staticmethod
    def log_event(
        operation: str,
        actor_id: Optional[int] = None,
        actor_name: Optional[str] = None,
        request_id: Optional[str] = None,
        payload: Optional[dict[str, Any]] = None,
        status: str = "success",
        details: Optional[str] = None,
    ):
        """
        Logs a high-risk mutation event in a structured format.
        """
        if not settings.AUDIT_LOG_ENABLED:
            return

        event = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "actor_id": actor_id,
            "actor_name": actor_name,
            "request_id": request_id,
            "status": status,
            "payload": payload or {},
            "details": details,
        }
        
        # Log as structured JSON for easy ingestion by log aggregators
        audit_logger.info(json.dumps(event))

    @staticmethod
    def log_mutation(
        request: Request,
        operation: str,
        actor: Any,  # Expected to be models.User
        payload: Optional[dict[str, Any]] = None,
        status: str = "success",
        details: Optional[str] = None,
    ):
        """
        Helper to log a mutation using a FastAPI Request object.
        """
        request_id = getattr(request.state, "request_id", "unknown")
        actor_id = getattr(actor, "id", None)
        actor_name = getattr(actor, "username", "unknown")
        
        AuditService.log_event(
            operation=operation,
            actor_id=actor_id,
            actor_name=actor_name,
            request_id=request_id,
            payload=payload,
            status=status,
            details=details,
        )

audit_service = AuditService()
