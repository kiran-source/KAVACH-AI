import os
import re
from typing import Tuple
from fastapi import HTTPException, UploadFile
from app.core.config import settings

ALLOWED_EXTENSIONS = {".wav", ".mp3", ".m4a", ".flac", ".ogg", ".webm"}

MAGIC_SIGNATURES = {
    ".wav": [b"RIFF"],
    ".mp3": [b"ID3", b"\xff\xfb", b"\xff\xf3", b"\xff\xf2", b"\xff\xe3"],
    ".flac": [b"fLaC"],
    ".ogg": [b"OggS"],
    ".webm": [b"\x1a\x45\xdf\xa3"]
}

def sanitize_filename(filename: str) -> str:
    """Strip dangerous characters, null bytes, and prevent path traversal."""
    if not filename:
        return "unnamed_audio"
    # Remove null bytes and control characters
    cleaned = filename.replace("\x00", "").strip()
    base = os.path.basename(cleaned)
    sanitized = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', base)
    sanitized = re.sub(r'\.{2,}', '.', sanitized)
    return sanitized or "unnamed_audio"

def validate_audio_magic_bytes(header_bytes: bytes, ext: str) -> bool:
    """Verifies that the initial bytes match known audio file signatures."""
    if not header_bytes or len(header_bytes) < 4:
        return False
        
    ext = ext.lower()
    
    # Specific M4A check: offset 4 contains 'ftyp'
    if ext == ".m4a":
        return len(header_bytes) >= 8 and header_bytes[4:8] == b"ftyp"

    # Specific WAV check: RIFF header + WAVE format indicator
    if ext == ".wav":
        if header_bytes.startswith(b"RIFF") and len(header_bytes) >= 12:
            return header_bytes[8:12] == b"WAVE"
        return header_bytes.startswith(b"RIFF")

    if ext in MAGIC_SIGNATURES:
        signatures = MAGIC_SIGNATURES[ext]
        for sig in signatures:
            if header_bytes.startswith(sig):
                return True
        return False

    return True

async def read_and_validate_stream(file: UploadFile, max_bytes: int) -> Tuple[bytes, str]:
    """
    Safely streams uploaded file in 64KB chunks to prevent RAM exhaustion.
    Validates magic bytes on initial chunk and raises HTTP 413 immediately
    if payload exceeds maximum permitted size.
    """
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported audio format '{ext}'. Supported formats: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
        )

    chunk_size = 64 * 1024 # 64 KB
    total_bytes = 0
    buffer = bytearray()
    first_chunk = True

    while True:
        chunk = await file.read(chunk_size)
        if not chunk:
            break
            
        total_bytes += len(chunk)
        if total_bytes > max_bytes:
            raise HTTPException(
                status_code=413,
                detail=f"Payload exceeds maximum allowed size of {settings.MAX_UPLOAD_SIZE_MB}MB. Upload aborted to prevent memory exhaustion."
            )
            
        if first_chunk:
            first_chunk = False
            # Check magic bytes for security verification
            if not validate_audio_magic_bytes(chunk[:16], ext):
                raise HTTPException(
                    status_code=400,
                    detail=f"File content header does not match expected audio format signature for '{ext}'."
                )

        buffer.extend(chunk)

    if total_bytes == 0:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty (0 bytes)."
        )

    return bytes(buffer), ext
