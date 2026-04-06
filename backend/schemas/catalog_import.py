from pydantic import BaseModel, Field
from typing import Optional, List, Any
from enum import Enum

class ImportAction(str, Enum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    CONFLICT = "CONFLICT"
    ERROR = "ERROR"

class ImportPreviewRow(BaseModel):
    row_number: int
    action: ImportAction
    sku: Optional[str] = None
    name: str
    existing_id: Optional[int] = None
    existing_name: Optional[str] = None
    changes: Optional[List[str]] = []
    error: Optional[str] = None
    
    # Store raw data for commit
    raw_data: Optional[dict] = None

class ImportPreview(BaseModel):
    batch_id: str
    filename: str
    total_rows: int
    created_count: int
    updated_count: int
    conflict_count: int
    error_count: int
    preview_rows: List[ImportPreviewRow]

class ImportCommitRequest(BaseModel):
    batch_id: str
    update_stock: bool = False
    actor_id: int
