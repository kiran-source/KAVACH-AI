from typing import Dict, Any, List
from app.gnani.prisma_client import GnaniPrismaClient
from app.gnani.timbre_client import GnaniTimbreClient

prisma_client = GnaniPrismaClient()
timbre_client = GnaniTimbreClient()

def process_transcription(audio_path: str, language: str = "auto") -> Dict[str, Any]:
    """Transcribe audio using Gnani Prisma v2.5 STT."""
    return prisma_client.transcribe(audio_path, language)

def generate_warning_audio(text: str, language: str = "en") -> Dict[str, Any]:
    """Synthesize voice safety warning using Gnani Timbre v2.5 TTS with local fallback."""
    return timbre_client.generate_speech(text, language)
