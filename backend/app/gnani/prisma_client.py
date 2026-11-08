import os
import time
import uuid
import requests
from typing import Dict, Any, List
from fastapi import HTTPException
from app.core.config import settings
from app.core.logging import logger

class GnaniPrismaClient:
    """
    Client for Gnani Prisma V3.0 Speech-to-Text API on Vachana platform.
    Official Endpoint: POST https://api.vachana.ai/stt/v3
    Authentication: X-API-Key-ID: <API_KEY>
    """
    def __init__(self):
        self.api_key = settings.GNANI_API_KEY
        self.endpoint = settings.GNANI_PRISMA_ENDPOINT
        self.max_retries = 1
        self.base_timeout = 30.0

    def transcribe(self, audio_path: str, language: str = "auto") -> Dict[str, Any]:
        """
        Transcribes audio using Gnani Prisma V3.0 STT.
        In Real API Mode (DEMO_MODE=false): Makes genuine authenticated requests.
        In Demo Mode (DEMO_MODE=true or placeholder key): Uses explicitly labeled simulated transcripts.
        """
        logger.info(f"Submitting audio {os.path.basename(audio_path)} to Gnani Prisma STT (hint={language})")
        
        # Check if running in demo mode or unconfigured API key
        is_mock_key = not self.api_key or self.api_key in [
            "mock_key", "mock_gnani_api_key_for_testing", "YOUR_ACTUAL_API_KEY", ""
        ]
        
        if settings.DEMO_MODE or is_mock_key:
            logger.info("Demo Mode or unconfigured API credentials. Generating simulated Prisma V3.0 transcript.")
            return self._generate_simulated_transcript(audio_path, language, is_mock=True)

        # Real API Mode: Must use official Gnani Vachana V3.0 endpoint and header
        headers = {
            "X-API-Key-ID": self.api_key,
            "User-Agent": "Kavach-AI/1.0"
        }

        # Language code mapping for Vachana STT V3
        lang_map = {
            "auto": "indic-auto",
            "indic-auto": "indic-auto",
            "hi": "hi-IN",
            "te": "te-IN",
            "en": "en-IN",
            "ta": "ta-IN",
            "kn": "kn-IN"
        }
        language_code = lang_map.get(language.lower(), "indic-auto")

        data = {
            "model": "prisma-v3.0",
            "language_code": language_code
        }

        ext = os.path.splitext(audio_path)[1].lower()
        mime_map = {
            ".wav": "audio/wav",
            ".mp3": "audio/mpeg",
            ".m4a": "audio/mp4",
            ".flac": "audio/flac",
            ".ogg": "audio/ogg",
            ".webm": "audio/webm"
        }
        content_type = mime_map.get(ext, "audio/wav")

        last_error = None
        for attempt in range(self.max_retries + 1):
            try:
                with open(audio_path, "rb") as f:
                    files = {
                        "audio_file": (os.path.basename(audio_path), f, content_type)
                    }
                    response = requests.post(
                        self.endpoint,
                        headers=headers,
                        files=files,
                        data=data,
                        timeout=self.base_timeout
                    )

                if response.status_code == 200:
                    resp_json = response.json()
                    logger.info("Successfully received genuine Gnani Prisma V3.0 STT response.")
                    return self._normalize_prisma_response(resp_json, language_code)
                elif response.status_code in [401, 403]:
                    err_msg = f"Gnani Prisma authentication failed (HTTP {response.status_code}): Invalid or unauthorized API key."
                    logger.error(err_msg)
                    raise HTTPException(status_code=response.status_code, detail=err_msg)
                elif response.status_code == 429:
                    err_msg = "Gnani Prisma rate limit reached (HTTP 429). Out of credits or concurrency limit exceeded."
                    logger.warning(err_msg)
                    last_error = err_msg
                    time.sleep(1.5)
                else:
                    err_msg = f"Gnani Prisma API returned HTTP {response.status_code}: {response.text[:200]}"
                    logger.error(err_msg)
                    last_error = err_msg
                    time.sleep(1.0)
            except HTTPException:
                raise
            except requests.exceptions.RequestException as e:
                err_msg = f"Network connection error to Gnani Prisma endpoint: {str(e)}"
                logger.error(err_msg)
                last_error = err_msg
                time.sleep(1.0)

        # In Real API Mode, NEVER silently substitute simulated mock data
        raise HTTPException(
            status_code=502,
            detail=f"Gnani Prisma V3.0 API request failed: {last_error}"
        )

    def _normalize_prisma_response(self, raw: Dict[str, Any], requested_lang: str) -> Dict[str, Any]:
        """
        Normalizes Gnani Prisma STT output to unified internal schema.
        Preserves genuine provider data without fabricating timestamps or language.
        """
        transcript_id = raw.get("request_id") or raw.get("transcript_id", f"TR-{uuid.uuid4().hex[:8].upper()}")
        
        # Extract transcript text across standard Gnani response fields
        full_text = (
            raw.get("transcript") or 
            raw.get("text") or 
            raw.get("full_text") or 
            (raw.get("data") and raw["data"].get("transcript")) or 
            ""
        ).strip()
        
        # Strict validation: Ensure non-empty transcript was returned
        if not full_text:
            raise HTTPException(
                status_code=502,
                detail="Gnani Prisma V3.0 returned an empty transcript. No recognizable speech detected."
            )
        
        # Extract detected language directly from provider without guessing
        detected_lang = (
            raw.get("detected_language_code") or
            raw.get("language_code") or 
            raw.get("language") or 
            raw.get("detected_language") or 
            requested_lang
        )
        
        segments = []
        raw_segments = raw.get("segments") or (raw.get("data") and raw["data"].get("segments")) or []
        if raw_segments and isinstance(raw_segments, list):
            for s in raw_segments:
                # Only record timestamps when genuinely provided
                start_val = float(s["start"]) if ("start" in s and s["start"] is not None) else None
                end_val = float(s["end"]) if ("end" in s and s["end"] is not None) else None
                segments.append({
                    "start": start_val,
                    "end": end_val,
                    "text": str(s.get("text", "")).strip(),
                    "language": str(s.get("language", detected_lang))
                })
        else:
            # Never fabricate fake timestamp ranges if provider didn't return segment boundaries
            provider_duration = raw.get("duration") or raw.get("audio_duration")
            segments.append({
                "start": 0.0 if provider_duration is not None else None,
                "end": float(provider_duration) if provider_duration is not None else None,
                "text": full_text,
                "language": detected_lang
            })

        return {
            "transcript_id": transcript_id,
            "language": detected_lang,
            "detected_languages": list(set([detected_lang.split("-")[0], "en"])),
            "segments": segments,
            "full_text": full_text,
            "provider": "gnani_prisma_v3.0",
            "is_mock": False,
            "raw_response": raw
        }

    def _generate_simulated_transcript(self, audio_path: str, language: str, is_mock: bool = True) -> Dict[str, Any]:
        """Produces realistic synthetic speech recognition transcripts for development and testing."""
        fname = os.path.basename(audio_path).lower()

        # 1. Bank Security Awareness & Advisories (Educational Precedence Guard)
        if "awareness" in fname or "advisory" in fname:
            detected_lang = "en"
            segments = [
                {"start": 0.0, "end": 4.8, "text": "Dear customer, this is an official security awareness announcement from your bank.", "language": "en"},
                {"start": 4.9, "end": 11.0, "text": "Please remember that bank officials and police never ask for your confidential OTP, UPI PIN, or passwords over the phone.", "language": "en"},
                {"start": 11.1, "end": 16.0, "text": "Stay safe from scam calls and beware of fake digital arrest threats. Report cyber fraud on helpline 1930.", "language": "en"}
            ]
            full_text = "Dear customer, this is an official security awareness announcement from your bank. Please remember that bank officials and police never ask for your confidential OTP, UPI PIN, or passwords over the phone. Stay safe from scam calls and beware of fake digital arrest threats. Report cyber fraud on helpline 1930."

        # 2. Legitimate Customer Care & Routine Support (Verified Benign)
        elif "safe" in fname or "legit" in fname or "support" in fname or "utility" in fname:
            detected_lang = "en"
            segments = [
                {"start": 0.0, "end": 5.0, "text": "Hello, thank you for reaching out to customer support regarding your internet broadband ticket.", "language": "en"},
                {"start": 5.1, "end": 10.0, "text": "Your connection speed has been restored and ticket #4819 is now resolved. Have a great day.", "language": "en"}
            ]
            full_text = "Hello, thank you for reaching out to customer support regarding your internet broadband ticket. Your connection speed has been restored and ticket #4819 is now resolved. Have a great day."

        # 3. Ambiguous Courier / Bank Inquiry
        elif "ambig" in fname or "courier" in fname or "delivery" in fname:
            detected_lang = "en"
            segments = [
                {"start": 0.0, "end": 6.5, "text": "Hello, am I speaking with the account holder? This is DTDC courier dispatch team.", "language": "en"},
                {"start": 6.6, "end": 14.0, "text": "Regarding a speed post parcel from HDFC Bank containing your renewed checkbook.", "language": "en"},
                {"start": 14.1, "end": 22.0, "text": "Nobody was available at your registered address. Could you confirm if you will be available tomorrow between 10 AM and 2 PM?", "language": "en"}
            ]
            full_text = "Hello, am I speaking with the account holder? This is DTDC courier dispatch team regarding a speed post parcel from HDFC Bank containing your renewed checkbook. Nobody was available at your registered address. Could you confirm if you will be available tomorrow between 10 AM and 2 PM?"

        # 4. CBI / Police Digital Arrest Scam
        elif "digital_arrest" in fname or "cbi" in fname or "police" in fname or "scam-001" in fname or "01_scam" in fname:
            detected_lang = "hi"
            segments = [
                {"start": 0.0, "end": 4.5, "text": "Namaste. I am Inspector Sharma from CBI headquarters Delhi.", "language": "en"},
                {"start": 4.6, "end": 11.2, "text": "Your Aadhaar number is linked with an international narcotics money laundering racket in Mumbai.", "language": "en"},
                {"start": 11.3, "end": 18.0, "text": "Supreme Court has placed you under Digital Arrest right now. Do not disconnect the video call or tell your family, otherwise police team will arrest you within 1 hour.", "language": "en"}
            ]
            full_text = "Namaste. I am Inspector Sharma from CBI headquarters Delhi. Your Aadhaar number is linked with an international narcotics money laundering racket in Mumbai. Supreme Court has placed you under Digital Arrest right now. Do not disconnect the video call or tell your family, otherwise police team will arrest you within 1 hour."

        # 5. Bank KYC & OTP Scam
        elif "kyc" in fname or "otp" in fname or "scam-002" in fname or "02_scam" in fname:
            detected_lang = "en"
            segments = [
                {"start": 0.0, "end": 4.0, "text": "Good morning sir, calling from State Bank of India KYC verification desk.", "language": "en"},
                {"start": 4.1, "end": 9.5, "text": "Your ATM card and net banking account are blocked due to pending KYC update.", "language": "en"},
                {"start": 9.6, "end": 15.0, "text": "To unfreeze your account immediately, share the 6-digit OTP and your UPI PIN right now.", "language": "en"}
            ]
            full_text = "Good morning sir, calling from State Bank of India KYC verification desk. Your ATM card and net banking account are blocked due to pending KYC update. To unfreeze your account immediately, share the 6-digit OTP and your UPI PIN right now."

        # 6. Telugu Coercion Scam
        elif "telugu" in fname or "te_" in fname or "scam-003" in fname:
            detected_lang = "te"
            segments = [
                {"start": 0.0, "end": 4.2, "text": "నమస్కారం, మీ బ్యాంకు అకౌంట్ మరియు ఏటీఎం కార్డు వెంటనే బ్లాక్ అవుతుంది.", "language": "te"},
                {"start": 4.3, "end": 9.8, "text": "వెంటనే మీ మొబైల్ కి వచ్చిన ఓటీపీ మరియు ఏటీఎం పిన్ నంబర్ చెప్పండి.", "language": "te"},
                {"start": 9.9, "end": 15.0, "text": "లేదంటే మీ పై పోలీస్ స్టేషన్ లో కేసు ఫైల్ చేస్తాం, అరెస్ట్ చేస్తారు.", "language": "te"}
            ]
            full_text = "నమస్కారం, మీ బ్యాంకు అకౌంట్ మరియు ఏటీఎం కార్డు వెంటనే బ్లాక్ అవుతుంది. వెంటనే మీ మొబైల్ కి వచ్చిన ఓటీపీ మరియు ఏటీఎం పిన్ నంబర్ చెప్పండి. లేదంటే మీ పై పోలీస్ స్టేషన్ లో కేసు ఫైల్ చేస్తాం, అరెస్ట్ చేస్తారు."

        # 7. Default Fallback
        else:
            detected_lang = "en"
            segments = [
                {"start": 0.0, "end": 5.0, "text": "Routine verification call. Ingested audio stream processed successfully.", "language": "en"}
            ]
            full_text = "Routine verification call. Ingested audio stream processed successfully."


        return {
            "transcript_id": f"TR-{uuid.uuid4().hex[:8].upper()}",
            "language": detected_lang,
            "detected_languages": [detected_lang, "en"],
            "segments": segments,
            "full_text": full_text,
            "provider": "gnani_prisma_v3.0 (Simulated / Demo Mode)",
            "is_mock": True
        }
