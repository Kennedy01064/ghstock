from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class SystemSettingBase(BaseModel):
    lockdown_enabled: bool = False
    institutional_name: str = "Stock Management System"
    institutional_logo_url: Optional[str] = None

class SystemSettingUpdate(BaseModel):
    lockdown_enabled: Optional[bool] = None
    institutional_name: Optional[str] = None
    institutional_logo_url: Optional[str] = None

class SystemSetting(SystemSettingBase):
    id: int
    last_updated: datetime
    model_config = ConfigDict(from_attributes=True)

class PublicSystemStatus(BaseModel):
    lockdown_enabled: bool = False
    message: str = ""
    institutional_name: str = "Stock Management System"
    institutional_logo_url: Optional[str] = None

class OrderSubmissionDeadlineBase(BaseModel):
    order_submission_deadline_at: Optional[datetime] = None
    order_submission_deadline_note: Optional[str] = None

class OrderSubmissionDeadlineUpdate(OrderSubmissionDeadlineBase):
    pass

class OrderSubmissionDeadlineSetting(OrderSubmissionDeadlineBase):
    last_updated: datetime
    model_config = ConfigDict(from_attributes=True)

class AuditLogBase(BaseModel):
    action: str
    resource_type: Optional[str] = None
    resource_id: Optional[str] = None
    details: Optional[str] = None

class AuditLog(AuditLogBase):
    id: int
    timestamp: datetime
    user_id: Optional[int]
    ip_address: Optional[str] = None
    
    # Simple user info in logs
    username: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class AuditLogWithUser(AuditLog):
    user: Optional["User"] = None


from .user import User

AuditLogWithUser.model_rebuild()
