import os
import wave
import uuid
from typing import Dict, Any, Optional
import soundfile as sf
from app.core.logging import logger
from app.audio.validator import sanitize_filename

UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../uploads"))
os.makedirs(UPLOAD_DIR, exist_ok=True)

def extract_audio_metadata(file_path: str) -> Dict[str, Any]:
    """
    Extracts duration, sample rate, channels, and format from audio file.
    Uses soundfile first, falling back to wave or audioread.
    """
    metadata = {
        "duration": 0.0,
        "sample_rate": 0,
        "channels": 1,
        "format": os.path.splitext(file_path)[1].lower().replace(".", ""),
        "file_size": os.path.getsize(file_path) if os.path.exists(file_path) else 0
    }
    
    # Try soundfile
    try:
        info = sf.info(file_path)
        metadata["duration"] = round(float(info.duration), 2)
        metadata["sample_rate"] = int(info.samplerate)
        metadata["channels"] = int(info.channels)
        metadata["format"] = str(info.format).lower()
        return metadata
    except Exception as e:
        logger.debug(f"SoundFile could not parse {file_path}: {e}")

    # Try standard wave module
    try:
        with wave.open(file_path, 'rb') as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            metadata["duration"] = round(frames / float(rate), 2) if rate > 0 else 0.0
            metadata["sample_rate"] = rate
            metadata["channels"] = wf.getnchannels()
            metadata["format"] = "wav"
            return metadata
    except Exception as e:
        logger.debug(f"Wave could not parse {file_path}: {e}")

    # Try audioread
    try:
        import audioread
        with audioread.audio_open(file_path) as a:
            metadata["duration"] = round(float(a.duration), 2)
            metadata["sample_rate"] = int(a.samplerate)
            metadata["channels"] = int(a.channels)
            return metadata
    except Exception as e:
        logger.warning(f"Audioread fallback could not parse {file_path}: {e}")

    # Fallback estimated duration based on typical bitrate if header parsing fails
    metadata["duration"] = max(1.0, round(metadata["file_size"] / 16000.0, 2))
    return metadata

def save_upload_file(file_content: bytes, original_filename: str) -> Dict[str, Any]:
    """
    Saves uploaded audio file safely with a unique UUID.
    Returns audio ID, stored path, and extracted metadata.
    """
    audio_id = str(uuid.uuid4())
    safe_name = sanitize_filename(original_filename)
    ext = os.path.splitext(safe_name)[1].lower() or ".wav"
    target_filename = f"{audio_id}{ext}"
    target_path = os.path.join(UPLOAD_DIR, target_filename)

    with open(target_path, "wb") as f:
        f.write(file_content)

    meta = extract_audio_metadata(target_path)
    return {
        "audio_id": audio_id,
        "original_filename": safe_name,
        "stored_path": target_path,
        "file_size": meta["file_size"],
        "duration": meta["duration"],
        "sample_rate": meta["sample_rate"],
        "channels": meta["channels"],
        "format": meta["format"]
    }

def delete_audio_file(file_path: str) -> bool:
    """Safely delete audio file."""
    try:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
            return True
    except Exception as e:
        logger.error(f"Error deleting audio file {file_path}: {e}")
    return False

