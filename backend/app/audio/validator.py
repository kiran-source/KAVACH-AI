import os
import re
from fastapi import HTTPException, UploadFile
from app.core.config import settings

ALLOWED_EXTENSIONS = {".wav", ".mp3", ".m4a", ".flac", ".ogg", ".webm"}
ALLOWED_MIME_TYPES = {
    "audio/wav", "audio/x-wav", "audio/wave",
    "audio/mpeg", "audio/mp3",
    "audio/mp4", "audio/m4a", "audio/x-m4a",
    "audio/flac", "audio/x-flac",
    "audio/ogg", "audio/vorbis", "application/ogg",
    "audio/webm", "video/webm"
}

def sanitize_filename(filename: str) -> str:
    """Strip dangerous characters and prevent path traversal."""
    if not filename:
        return "unnamed_audio"
    base = os.path.basename(filename)
    sanitized = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', base)
    sanitized = re.sub(r'\.{2,}', '.', sanitized)
    return sanitized or "unnamed_audio"

def validate_audio_file(file: UploadFile, file_size: int) -> str:
    """Validate file extension and size constraints."""
    ext = os.path.splitext(file.filename)[1].lower() if file.filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported audio format '{ext}'. Supported formats: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
        )
    
    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    if file_size > max_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"File size exceeds maximum allowed limit of {settings.MAX_UPLOAD_SIZE_MB}MB."
        )
        
    return ext

