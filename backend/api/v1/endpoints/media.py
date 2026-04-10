import uuid
import os
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from backend.api import deps
from backend import models

router = APIRouter()

# Simple storage path - in production this would be S3 or similar
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Standard media upload endpoint for mobile apps.
    Saves to local 'uploads' directory and returns the public URL path.
    """
    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Only JPEG, PNG and WEBP are allowed")
    
    # Generate unique filename
    extension = os.path.splitext(file.filename)[1].lower()
    if not extension:
        if file.content_type == "image/jpeg": extension = ".jpg"
        elif file.content_type == "image/png": extension = ".png"
        elif file.content_type == "image/webp": extension = ".webp"
    
    filename = f"{uuid.uuid4()}{extension}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    # Write file
    try:
        content = await file.read()
        with open(file_path, "wb") as buffer:
            buffer.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
        
    return {"url": f"/static/uploads/{filename}", "filename": filename}
 Elias
