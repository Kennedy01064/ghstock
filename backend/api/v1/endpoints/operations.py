from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from backend import models, schemas
from backend.api import deps

router = APIRouter()


def _request_ip(request: Request | None) -> str | None:
    if request is None or request.client is None:
        return None
    return request.client.host


def _normalize_deadline(value: datetime | None) -> datetime | None:
    if value is None:
        return None
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


@router.get("/order-deadline", response_model=schemas.admin.OrderSubmissionDeadlineSetting)
def read_order_deadline(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_management),
) -> Any:
    settings_row = deps.get_system_setting(db)
    return {
        "order_submission_deadline_at": _normalize_deadline(
            settings_row.order_submission_deadline_at
        ),
        "order_submission_deadline_note": settings_row.order_submission_deadline_note,
        "last_updated": _normalize_deadline(settings_row.last_updated),
    }


@router.put("/order-deadline", response_model=schemas.admin.OrderSubmissionDeadlineSetting)
def update_order_deadline(
    *,
    request: Request,
    db: Session = Depends(deps.get_db),
    settings_in: schemas.admin.OrderSubmissionDeadlineUpdate,
    current_user: models.User = Depends(deps.get_current_active_management),
) -> Any:
    settings_row = deps.get_system_setting(db)
    deadline_was_set = settings_row.order_submission_deadline_at is not None

    if (
        settings_in.order_submission_deadline_note
        and "order_submission_deadline_at" not in settings_in.model_fields_set
        and settings_row.order_submission_deadline_at is None
    ):
        raise HTTPException(
            status_code=400,
            detail="Debe definir una fecha limite antes de registrar una nota.",
        )

    if "order_submission_deadline_at" in settings_in.model_fields_set:
        settings_row.order_submission_deadline_at = _normalize_deadline(
            settings_in.order_submission_deadline_at
        )
        if settings_in.order_submission_deadline_at is None:
            settings_row.order_submission_deadline_note = None

    if "order_submission_deadline_note" in settings_in.model_fields_set:
        normalized_note = (settings_in.order_submission_deadline_note or "").strip()
        if normalized_note and settings_row.order_submission_deadline_at is None:
            raise HTTPException(
                status_code=400,
                detail="La nota solo puede guardarse si existe una fecha limite activa.",
            )
        settings_row.order_submission_deadline_note = normalized_note or None

    settings_row.last_updated = datetime.now(timezone.utc)
    db.add(settings_row)
    db.commit()
    db.refresh(settings_row)

    action = (
        "operations.order_deadline.cleared"
        if deadline_was_set and settings_row.order_submission_deadline_at is None
        else "operations.order_deadline.updated"
    )
    details = (
        "Fecha limite eliminada"
        if settings_row.order_submission_deadline_at is None
        else f"deadline={_normalize_deadline(settings_row.order_submission_deadline_at).isoformat()}, note={settings_row.order_submission_deadline_note or 'Sin nota'}"
    )

    db.add(
        models.AuditLog(
            user_id=current_user.id,
            action=action,
            resource_type="system_setting",
            resource_id=str(settings_row.id),
            details=details,
            ip_address=_request_ip(request),
        )
    )
    db.commit()

    return {
        "order_submission_deadline_at": _normalize_deadline(
            settings_row.order_submission_deadline_at
        ),
        "order_submission_deadline_note": settings_row.order_submission_deadline_note,
        "last_updated": _normalize_deadline(settings_row.last_updated),
    }
