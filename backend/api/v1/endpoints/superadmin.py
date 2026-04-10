from datetime import datetime, timezone
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session, joinedload

from backend import models, schemas
from backend.api import deps

router = APIRouter()


def _request_ip(request: Request | None) -> str | None:
    if request is None or request.client is None:
        return None
    return request.client.host


def _log_superadmin_action(
    db: Session,
    *,
    actor: models.User,
    action: str,
    resource_type: str,
    resource_id: str | None,
    details: str,
    request: Request | None = None,
) -> None:
    db.add(
        models.AuditLog(
            user_id=actor.id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
            ip_address=_request_ip(request),
        )
    )
    db.commit()


@router.get("/settings", response_model=schemas.admin.SystemSetting)
def read_settings(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superadmin),
) -> Any:
    return deps.get_system_setting(db)


@router.put("/settings", response_model=schemas.admin.SystemSetting)
def update_settings(
    *,
    request: Request,
    db: Session = Depends(deps.get_db),
    settings_in: schemas.admin.SystemSettingUpdate,
    current_user: models.User = Depends(deps.get_current_active_superadmin),
) -> Any:
    settings_row = deps.get_system_setting(db)
    changed_fields: list[str] = []

    if settings_in.lockdown_enabled is not None and settings_in.lockdown_enabled != settings_row.lockdown_enabled:
        settings_row.lockdown_enabled = settings_in.lockdown_enabled
        changed_fields.append(f"lockdown_enabled={settings_row.lockdown_enabled}")

    if settings_in.institutional_name is not None and settings_in.institutional_name != settings_row.institutional_name:
        settings_row.institutional_name = settings_in.institutional_name.strip() or settings_row.institutional_name
        changed_fields.append("institutional_name")

    if settings_in.institutional_logo_url is not None and settings_in.institutional_logo_url != settings_row.institutional_logo_url:
        settings_row.institutional_logo_url = settings_in.institutional_logo_url.strip() or None
        changed_fields.append("institutional_logo_url")

    if changed_fields:
        settings_row.last_updated = datetime.now(timezone.utc)

    db.add(settings_row)
    db.commit()
    db.refresh(settings_row)

    if changed_fields:
        _log_superadmin_action(
            db,
            actor=current_user,
            action="system.settings.updated",
            resource_type="system_setting",
            resource_id=str(settings_row.id),
            details=", ".join(changed_fields),
            request=request,
        )

    return settings_row


@router.get("/audit-logs", response_model=List[schemas.admin.AuditLog])
def read_audit_logs(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superadmin),
    limit: int = Query(50, ge=1, le=200),
    action: Optional[str] = None,
    search: Optional[str] = None,
) -> Any:
    query = db.query(models.AuditLog).options(
        joinedload(models.AuditLog.user)
    )

    if action:
        query = query.filter(models.AuditLog.action == action)

    if search:
        term = f"%{search.strip()}%"
        query = query.filter(
            (models.AuditLog.action.ilike(term))
            | (models.AuditLog.resource_type.ilike(term))
            | (models.AuditLog.resource_id.ilike(term))
            | (models.AuditLog.details.ilike(term))
        )

    logs = query.order_by(models.AuditLog.timestamp.desc()).limit(limit).all()
    return [
        {
            "id": log.id,
            "timestamp": log.timestamp,
            "user_id": log.user_id,
            "username": log.user.username if log.user else None,
            "action": log.action,
            "resource_type": log.resource_type,
            "resource_id": log.resource_id,
            "details": log.details,
            "ip_address": log.ip_address,
        }
        for log in logs
    ]
