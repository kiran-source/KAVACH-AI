import os
import io
import math
import struct
import wave
import uuid
import time
import requests
from typing import Dict, Any, Optional
from app.core.config import settings
from app.core.logging import logger

WARNING_AUDIO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../uploads/warnings"))
os.makedirs(WARNING_AUDIO_DIR, exist_ok=True)

class GnaniTimbreClient:
    """
    Client for Gnani Timbre v2.5 Text-to-Speech API.
    Provides speech synthesis for safety warnings in English, Telugu, and Hindi.
    Includes offline TTS fallback using pyttsx3 and valid WAV tone synthesis.
    """
    def __init__(self):
        self.api_key = settings.GNANI_API_KEY
        self.endpoint = settings.GNANI_TIMBRE_ENDPOINT
        self.timeout = 25.0

    def generate_speech(self, text: str, language: str = "en") -> Dict[str, Any]:
        """
        Synthesizes warning audio. Returns metadata including audio file path, audio bytes, and status.
        """
        logger.info(f"Generating voice warning via Timbre (lang={language}, text_len={len(text)})")
        
        is_mock_key = not self.api_key or self.api_key in ["mock_key", "mock_gnani_api_key_for_testing", ""]
        
        # Live Gnani Timbre API call if configured
        if not settings.DEMO_MODE and not is_mock_key:
            try:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "User-Agent": "Kavach-AI/1.0"
                }
                payload = {
                    "text": text,
                    "language": language,
                    "voice": "safety_alert",
                    "audio_format": "wav"
                }
                resp = requests.post(self.endpoint, headers=headers, json=payload, timeout=self.timeout)
                if resp.status_code == 200 and len(resp.content) > 100:
                    filename = f"warning_{uuid.uuid4().hex[:8]}.wav"
                    file_path = os.path.join(WARNING_AUDIO_DIR, filename)
                    with open(file_path, "wb") as f:
                        f.write(resp.content)
                    return {
                        "filename": filename,
                        "file_path": file_path,
                        "audio_bytes": resp.content,
                        "provider": "gnani_timbre_v2.5",
                        "is_fallback": False,
                        "language": language
                    }
                else:
                    logger.warning(f"Gnani Timbre API returned {resp.status_code}. Using local TTS fallback.")
            except Exception as e:
                logger.error(f"Gnani Timbre API connection failed: {e}. Using local TTS fallback.")

        # Local Fallback generation: synthesize genuine spoken speech via pyttsx3 or tone WAV
        return self._generate_local_fallback_audio(text, language)

    def _generate_local_fallback_audio(self, text: str, language: str) -> Dict[str, Any]:
        """Generates real local playable speech audio on Windows using pyttsx3 or clear alert sound wave."""
        filename = f"warning_fallback_{uuid.uuid4().hex[:8]}.wav"
        file_path = os.path.join(WARNING_AUDIO_DIR, filename)
        
        # Attempt offline speech synthesis with pyttsx3
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)
            engine.setProperty('volume', 1.0)
            engine.save_to_file(text, file_path)
            engine.runAndWait()
            
            if os.path.exists(file_path) and os.path.getsize(file_path) > 100:
                with open(file_path, "rb") as f:
                    audio_bytes = f.read()
                logger.info(f"Local TTS fallback generated successfully: {file_path}")
                return {
                    "filename": filename,
                    "file_path": file_path,
                    "audio_bytes": audio_bytes,
                    "provider": "local_sapi_tts_fallback",
                    "is_fallback": True,
                    "language": language
                }
        except Exception as e:
            logger.warning(f"pyttsx3 engine failed to render audio file: {e}. Generating alert audio signal.")

        # Fallback: Generate an emergency cybersecurity audio alert signal in valid WAV format
        sample_rate = 16000
        duration = 2.0
        num_samples = int(duration * sample_rate)
        
        buf = io.BytesIO()
        with wave.open(buf, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            for i in range(num_samples):
                # Two-tone cyber siren (880Hz alternating with 587Hz)
                freq = 880.0 if (i // 4000) % 2 == 0 else 587.0
                t = float(i) / sample_rate
                envelope = min(1.0, i / 800) * min(1.0, (num_samples - i) / 800)
                val = int(32767.0 * 0.4 * envelope * math.sin(2.0 * math.pi * freq * t))
                wf.writeframesraw(struct.pack('<h', val))
                
        audio_bytes = buf.getvalue()
        with open(file_path, "wb") as f:
            f.write(audio_bytes)

        return {
            "filename": filename,
            "file_path": file_path,
            "audio_bytes": audio_bytes,
            "provider": "security_tone_fallback",
            "is_fallback": True,
            "language": language
        }

