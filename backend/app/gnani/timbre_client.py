import os
import io
import math
import struct
import wave
import uuid
import time
import base64
import requests
from typing import Dict, Any, Optional
from fastapi import HTTPException
from app.core.config import settings
from app.core.logging import logger

WARNING_AUDIO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../uploads/warnings"))
os.makedirs(WARNING_AUDIO_DIR, exist_ok=True)

class GnaniTimbreClient:
    """
    Client for Gnani Timbre V2.5 Text-to-Speech API on Vachana platform.
    Official Endpoint: POST https://api.vachana.ai/api/v1/tts/inference
    Authentication: X-API-Key-ID: <API_KEY>
    """
    def __init__(self):
        self.api_key = settings.GNANI_API_KEY
        self.endpoint = settings.GNANI_TIMBRE_ENDPOINT
        self.timeout = 25.0

    def generate_speech(self, text: str, language: str = "en") -> Dict[str, Any]:
        """
        Synthesizes warning audio. Returns metadata including audio file path, audio bytes, and status.
        In Real API Mode (DEMO_MODE=false): Calls official Gnani Timbre V2.5 endpoint with strict validation.
        In Demo Mode (DEMO_MODE=true): Uses local fallback speech synthesis.
        """
        logger.info(f"Generating voice warning via Timbre (lang={language}, text_len={len(text)})")
        
        is_mock_key = not self.api_key or self.api_key in [
            "mock_key", "mock_gnani_api_key_for_testing", "YOUR_ACTUAL_API_KEY", ""
        ]
        
        # Real API Mode
        if not settings.DEMO_MODE and not is_mock_key:
            lang_map = {
                "hi": "hi-IN",
                "te": "te-IN",
                "en": "en-IN",
                "hi-in": "hi-IN",
                "te-in": "te-IN",
                "en-in": "en-IN"
            }
            lang_code = lang_map.get(language.lower(), "en-IN")

            headers = {
                "X-API-Key-ID": self.api_key,
                "Content-Type": "application/json",
                "User-Agent": "Kavach-AI/1.0"
            }

            payload = {
                "text": text,
                "voice": "Nalini",
                "model": "timbre-v2.5",
                "language": lang_code,
                "speed": 1,
                "audio_config": {
                    "encoding": "linear_pcm",
                    "container": "wav",
                    "num_channels": 1,
                    "sample_rate": 48000,
                    "sample_width": 2
                }
            }

            try:
                resp = requests.post(self.endpoint, headers=headers, json=payload, timeout=self.timeout)
                if resp.status_code == 200:
                    content_type = resp.headers.get("content-type", "").lower()
                    audio_bytes = None

                    # Check if response is raw binary WAV
                    if resp.content.startswith(b"RIFF"):
                        audio_bytes = resp.content
                    elif "audio" in content_type:
                        audio_bytes = resp.content
                    else:
                        # Attempt parsing JSON response with base64 audio
                        try:
                            resp_json = resp.json()
                            b64_data = (
                                resp_json.get("audio") or 
                                resp_json.get("audio_content") or 
                                (resp_json.get("data") and resp_json["data"].get("audio"))
                            )
                            if b64_data:
                                audio_bytes = base64.b64decode(b64_data)
                            elif resp.content:
                                audio_bytes = resp.content
                        except Exception:
                            audio_bytes = resp.content

                    # Validate audio integrity: Must be valid WAV with RIFF header and non-trivial size
                    if not audio_bytes or len(audio_bytes) < 44:
                        logger.error(f"Timbre returned empty or truncated audio ({len(audio_bytes) if audio_bytes else 0} bytes)")
                        raise HTTPException(
                            status_code=502,
                            detail="Gnani Timbre API returned an empty or truncated audio stream."
                        )
                    
                    if not audio_bytes.startswith(b"RIFF"):
                        logger.error("Timbre returned invalid audio header (not RIFF/WAVE)")
                        raise HTTPException(
                            status_code=502,
                            detail="Gnani Timbre API returned invalid audio data (missing RIFF/WAVE header)."
                        )

                    filename = f"warning_timbre_{uuid.uuid4().hex[:8]}.wav"
                    file_path = os.path.join(WARNING_AUDIO_DIR, filename)
                    with open(file_path, "wb") as f:
                        f.write(audio_bytes)
                    logger.info(f"Successfully generated speech using Gnani Timbre V2.5 ({len(audio_bytes)} bytes)")
                    return {
                        "filename": filename,
                        "file_path": file_path,
                        "audio_bytes": audio_bytes,
                        "provider": "gnani_timbre_v2.5",
                        "is_fallback": False,
                        "language": lang_code,
                        "status": "success"
                    }
                elif resp.status_code in [401, 403]:
                    err_msg = f"Gnani Timbre authentication failed (HTTP {resp.status_code}): Invalid or unauthorized API key."
                    logger.error(err_msg)
                    raise HTTPException(status_code=resp.status_code, detail=err_msg)
                else:
                    err_msg = f"Gnani Timbre API returned HTTP {resp.status_code}: {resp.text[:200]}"
                    logger.error(err_msg)
                    raise HTTPException(status_code=502, detail=err_msg)
            except HTTPException:
                raise
            except requests.exceptions.RequestException as e:
                err_msg = f"Network connection error to Gnani Timbre endpoint: {str(e)}"
                logger.error(err_msg)
                raise HTTPException(status_code=503, detail=err_msg)

        # Demo Mode: Generate local playable speech via SAPI5 or alert wave
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
                    "provider": "local_sapi_tts_fallback (Demo Mode)",
                    "is_fallback": True,
                    "language": language,
                    "status": "success"
                }
        except Exception as e:
            logger.warning(f"pyttsx3 engine failed to render audio file: {e}. Generating alert audio signal.")

        # Fallback: Generate an emergency cybersecurity audio alert signal in valid WAV format
        sample_rate = 16000
        duration_sec = 2.0
        num_samples = int(sample_rate * duration_sec)
        
        with wave.open(file_path, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            
            for i in range(num_samples):
                t = float(i) / sample_rate
                # 440 Hz alert pulse modulated at 4 Hz
                freq = 440.0 if (int(t * 4) % 2 == 0) else 554.37
                val = 0.5 * math.sin(2.0 * math.pi * freq * t)
                sample = int(val * 32767.0)
                wf.writeframesraw(struct.pack('<h', sample))

        with open(file_path, "rb") as f:
            audio_bytes = f.read()

        logger.info(f"Emergency alert tone generated: {file_path} ({len(audio_bytes)} bytes)")
        return {
            "filename": filename,
            "file_path": file_path,
            "audio_bytes": audio_bytes,
            "provider": "security_tone_fallback (Demo Mode)",
            "is_fallback": True,
            "language": language,
            "status": "success"
        }
