import uuid
import os
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from supabase import create_client, Client
from backend.api import deps
from backend import models
from backend.core.config import settings

router = APIRouter()

# Initialize Supabase client if credentials are provided
supabase_client: Client = None
if settings.SUPABASE_URL and settings.SUPABASE_SERVICE_KEY:
    try:
        supabase_client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)
        print("✅ Supabase Storage client initialized successfully")
    except Exception as e:
        print(f"⚠️ Failed to initialize Supabase client: {str(e)}")
        supabase_client = None

# Fallback local directory (for development or if Supabase is not configured)
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Media upload endpoint.
    Prioritizes Supabase Storage for production persistence.
    Falls back to local 'uploads' directory if Supabase is not configured.
    """
    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "image/webp", "image/gif"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Only JPEG, PNG, WEBP and GIF are allowed")
    
    # Generate unique filename
    extension = os.path.splitext(file.filename)[1].lower()
    if not extension:
        mapping = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp", "image/gif": ".gif"}
        extension = mapping.get(file.content_type, ".bin")
    
    filename = f"{uuid.uuid4()}{extension}"
    
    # Attempt Supabase Upload
    if supabase_client:
        try:
            content = await file.read()
            # Upload to Supabase
            response = supabase_client.storage.from_(settings.SUPABASE_BUCKET).upload(
                path=filename,
                file=content,
                file_options={"content-type": file.content_type, "upsert": "false"}
            )
            
            # Construct public URL
            # Note: Assumes the bucket is set to PUBLIC in Supabase
            # Format: https://[project-id].supabase.co/storage/v1/object/public/[bucket]/[filename]
            public_url = f"{settings.SUPABASE_URL}/storage/v1/object/public/{settings.SUPABASE_BUCKET}/{filename}"
            
            return {
                "url": public_url,
                "filename": filename,
                "storage": "supabase"
            }
        except Exception as e:
            # Fallback to local if Supabase fails (optional, but safer for now)
            print(f"Supabase upload failed, falling back to local: {str(e)}")
            await file.seek(0) # Reset file pointer for local read

    # Local Filesystem Fallback
    file_path = os.path.join(UPLOAD_DIR, filename)
    try:
        content = await file.read()
        with open(file_path, "wb") as buffer:
            buffer.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
        
    return {
        "url": f"/static/uploads/{filename}", 
        "filename": filename,
        "storage": "local"
    }
