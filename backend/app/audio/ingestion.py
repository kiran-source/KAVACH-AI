import os
import uuid
import shutil
from fastapi import UploadFile, HTTPException, status
from app.core.config import settings
from app.core.logging import logger

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {".wav", ".mp3", ".m4a", ".flac", ".ogg"}

async def save_uploaded_audio(file: UploadFile) -> dict:
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file format {file_ext}. Allowed formats: {list(ALLOWED_EXTENSIONS)}"
        )
    
    audio_id = str(uuid.uuid4())
    stored_filename = f"{audio_id}{file_ext}"
    stored_path = os.path.join(UPLOAD_DIR, stored_filename)
    
    try:
        content = await file.read()
        file_size = len(content)
        
        max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
        if file_size > max_bytes:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File size exceeds maximum allowed limit of {settings.MAX_UPLOAD_SIZE_MB}MB"
            )
            
        with open(stored_path, "wb") as buffer:
            buffer.write(content)
            
        logger.info(f"Saved audio file {file.filename} as {stored_path} ({file_size} bytes)")
        
        # Estimate duration roughly if soundfile/librosa available or fallback
        duration = 15.0 # default estimated duration in seconds for mock/demo
        try:
            import soundfile as sf
            info = sf.info(stored_path)
            duration = info.duration
        except Exception as e:
            logger.warning(f"Could not extract exact duration via soundfile: {e}")
            
        return {
            "id": audio_id,
            "original_filename": file.filename,
            "stored_path": stored_path,
            "file_size": file_size,
            "duration": duration,
            "format": file_ext.lstrip(".")
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error saving uploaded audio: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process audio upload: {str(e)}"
        )
