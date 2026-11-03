import os
import time
import uuid
import requests
from typing import Dict, Any, List
from app.core.config import settings
from app.core.logging import logger

class GnaniPrismaClient:
    """
    Client for Gnani Prisma v2.5 Speech-to-Text API.
    Provides authentication, bounded retries with exponential backoff,
    response normalization, and clear fallback detection.
    """
    def __init__(self):
        self.api_key = settings.GNANI_API_KEY
        self.endpoint = settings.GNANI_PRISMA_ENDPOINT
        self.max_retries = 2
        self.base_timeout = 30.0

    def transcribe(self, audio_path: str, language: str = "auto") -> Dict[str, Any]:
        """
        Transcribes audio using Gnani Prisma v2.5 STT.
        Normalizes provider response to internal schema.
        Falls back to deterministic synthetic transcript if in demo mode or credentials unconfigured.
        """
        logger.info(f"Submitting audio {os.path.basename(audio_path)} to Gnani Prisma STT (lang={language})")
        
        # Check if running in demo mode or unconfigured API key
        is_mock_key = not self.api_key or self.api_key in ["mock_key", "mock_gnani_api_key_for_testing", ""]
        if settings.DEMO_MODE or is_mock_key:
            logger.info("Demo Mode or unconfigured API credentials. Generating simulated Prisma v2.5 transcript.")
            return self._generate_simulated_transcript(audio_path, language, is_mock=True)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "User-Agent": "Kavach-AI/1.0"
        }

        start_time = time.time()
        for attempt in range(self.max_retries + 1):
            try:
                with open(audio_path, "rb") as f:
                    files = {"audio": (os.path.basename(audio_path), f, "audio/wav")}
                    data = {"language": language, "model_version": "v2.5"}
                    response = requests.post(
                        self.endpoint,
                        headers=headers,
                        files=files,
                        data=data,
                        timeout=self.base_timeout
                    )
                    
                if response.status_code == 200:
                    resp_json = response.json()
                    logger.info("Successfully received Gnani Prisma v2.5 transcription response.")
                    return self._normalize_prisma_response(resp_json, language)
                elif response.status_code in [401, 403]:
                    logger.error(f"Gnani Prisma authentication failed (HTTP {response.status_code}).")
                    break
                elif response.status_code == 429:
                    logger.warning(f"Gnani Prisma rate limit reached. Attempt {attempt + 1}/{self.max_retries + 1}")
                    time.sleep(1.5 * (attempt + 1))
                else:
                    logger.warning(f"Gnani Prisma returned status {response.status_code}: {response.text}")
                    time.sleep(1.0)
            except requests.exceptions.RequestException as e:
                logger.error(f"Network error communicating with Gnani Prisma: {e}")
                time.sleep(1.0)

        logger.warning("Gnani Prisma endpoint unreachable or credentials rejected. Falling back to local demo transcript.")
        return self._generate_simulated_transcript(audio_path, language, is_mock=True)

    def _normalize_prisma_response(self, raw: Dict[str, Any], requested_lang: str) -> Dict[str, Any]:
        """Normalizes Gnani Prisma STT output to unified internal schema."""
        transcript_id = raw.get("transcript_id", f"TR-{uuid.uuid4().hex[:8].upper()}")
        full_text = raw.get("full_text") or raw.get("text") or raw.get("transcript", "")
        detected_lang = raw.get("language") or raw.get("detected_language") or requested_lang
        
        segments = []
        raw_segments = raw.get("segments", [])
        if raw_segments:
            for s in raw_segments:
                segments.append({
                    "start": float(s.get("start", 0.0)),
                    "end": float(s.get("end", 0.0)),
                    "text": str(s.get("text", "")).strip(),
                    "language": str(s.get("language", detected_lang))
                })
        else:
            segments.append({
                "start": 0.0,
                "end": 10.0,
                "text": full_text,
                "language": detected_lang
            })

        return {
            "transcript_id": transcript_id,
            "language": detected_lang,
            "detected_languages": list(set([detected_lang, "en"])),
            "segments": segments,
            "full_text": full_text,
            "provider": "gnani_prisma_v2.5",
            "is_mock": False
        }

    def _generate_simulated_transcript(self, audio_path: str, language: str, is_mock: bool = True) -> Dict[str, Any]:
        """Produces realistic synthetic speech recognition transcripts for development and testing."""
        fname = os.path.basename(audio_path).lower()

        if "digital_arrest" in fname or "cbi" in fname or "police" in fname:
            detected_lang = "hi"
            segments = [
                {"start": 0.0, "end": 4.5, "text": "Namaste. I am Inspector Sharma from CBI headquarters Delhi.", "language": "en"},
                {"start": 4.6, "end": 11.2, "text": "Your Aadhaar number is linked with an international narcotics money laundering racket in Mumbai.", "language": "en"},
                {"start": 11.3, "end": 18.0, "text": "Supreme Court has placed you under Digital Arrest right now. Do not disconnect the video call or tell your family, otherwise police team will arrest you within 1 hour.", "language": "en"}
            ]
            full_text = "Namaste. I am Inspector Sharma from CBI headquarters Delhi. Your Aadhaar number is linked with an international narcotics money laundering racket in Mumbai. Supreme Court has placed you under Digital Arrest right now. Do not disconnect the video call or tell your family, otherwise police team will arrest you within 1 hour."

        elif "kyc" in fname or "bank" in fname or "otp" in fname:
            detected_lang = "en"
            segments = [
                {"start": 0.0, "end": 4.0, "text": "Good morning sir, calling from State Bank of India KYC verification desk.", "language": "en"},
                {"start": 4.1, "end": 9.5, "text": "Your ATM card and net banking account are blocked due to pending KYC update.", "language": "en"},
                {"start": 9.6, "end": 15.0, "text": "To unfreeze your account immediately, share the 6-digit OTP and your UPI PIN right now.", "language": "en"}
            ]
            full_text = "Good morning sir, calling from State Bank of India KYC verification desk. Your ATM card and net banking account are blocked due to pending KYC update. To unfreeze your account immediately, share the 6-digit OTP and your UPI PIN right now."

        elif "telugu" in fname or "te_" in fname:
            detected_lang = "te"
            segments = [
                {"start": 0.0, "end": 4.2, "text": "నమస్కారం, మీ బ్యాంకు అకౌంట్ మరియు ఏటీఎం కార్డు వెంటనే బ్లాక్ అవుతుంది.", "language": "te"},
                {"start": 4.3, "end": 9.8, "text": "వెంటనే మీ మొబైల్ కి వచ్చిన ఓటీపీ మరియు ఏటీఎం పిన్ నంబర్ చెప్పండి.", "language": "te"},
                {"start": 9.9, "end": 15.0, "text": "లేదంటే మీ పై పోలీస్ స్టేషన్ లో కేసు ఫైల్ చేస్తాం, అరెస్ట్ చేస్తారు.", "language": "te"}
            ]
            full_text = "నమస్కారం, మీ బ్యాంకు అకౌంట్ మరియు ఏటీఎం కార్డు వెంటనే బ్లాక్ అవుతుంది. వెంటనే మీ మొబైల్ కి వచ్చిన ఓటీపీ మరియు ఏటీఎం పిన్ నంబర్ చెప్పండి. లేదంటే మీ పై పోలీస్ స్టేషన్ లో కేసు ఫైల్ చేస్తాం, అరెస్ట్ చేస్తారు."

        elif "hindi" in fname or "hi_" in fname:
            detected_lang = "hi"
            segments = [
                {"start": 0.0, "end": 4.0, "text": "नमस्कार, मैं टेलीकॉम डिपार्टमेंट और साइबर क्राइम ब्रांच से बात कर रहा हूँ।", "language": "hi"},
                {"start": 4.1, "end": 9.0, "text": "आपके आधार नंबर पर गैरकानूनी गतिविधियां दर्ज हैं और 2 घंटे में सिम ब्लॉक हो जाएगा।", "language": "hi"},
                {"start": 9.1, "end": 14.5, "text": "तुरंत एनीडेस्क ऐप डाउनलोड करके स्क्रीन शेयर करो वरना पुलिस गिरफ्तारी वारंट जारी करेगी।", "language": "hi"}
            ]
            full_text = "नमस्कार, मैं टेलीकॉम डिपार्टमेंट और साइबर क्राइम ब्रांच से बात कर रहा हूँ। आपके आधार नंबर पर गैरकानूनी गतिविधियां दर्ज हैं और 2 घंटे में सिम ब्लॉक हो जाएगा। तुरंत एनीडेस्क ऐप डाउनलोड करके स्क्रीन शेयर करो वरना पुलिस गिरफ्तारी वारंट जारी करेगी।"

        elif "safe" in fname or "legit" in fname:
            detected_lang = "en"
            segments = [
                {"start": 0.0, "end": 5.0, "text": "Hello, thank you for reaching out to customer support regarding your internet broadband ticket.", "language": "en"},
                {"start": 5.1, "end": 10.0, "text": "Your connection speed has been restored and ticket #4819 is now resolved. Have a great day.", "language": "en"}
            ]
            full_text = "Hello, thank you for reaching out to customer support regarding your internet broadband ticket. Your connection speed has been restored and ticket #4819 is now resolved. Have a great day."

        elif "awareness" in fname or "advisory" in fname:
            detected_lang = "en"
            segments = [
                {"start": 0.0, "end": 4.8, "text": "Dear customer, this is an official security awareness announcement from your bank.", "language": "en"},
                {"start": 4.9, "end": 11.0, "text": "Please remember that bank officials never ask for your OTP, UPI PIN, or passwords.", "language": "en"},
                {"start": 11.1, "end": 16.0, "text": "Stay safe from scam calls and beware of fake digital arrest threats.", "language": "en"}
            ]
            full_text = "Dear customer, this is an official security awareness announcement from your bank. Please remember that bank officials never ask for your OTP, UPI PIN, or passwords. Stay safe from scam calls and beware of fake digital arrest threats."

        else:
            detected_lang = "en"
            segments = [
                {"start": 0.0, "end": 4.5, "text": "Urgent alert regarding your bank transaction. Suspicious debit attempted.", "language": "en"},
                {"start": 4.6, "end": 10.0, "text": "Transfer Rs 50,000 to safe government verification account immediately or face arrest.", "language": "en"}
            ]
            full_text = "Urgent alert regarding your bank transaction. Suspicious debit attempted. Transfer Rs 50,000 to safe government verification account immediately or face arrest."

        return {
            "transcript_id": f"TR-{uuid.uuid4().hex[:8].upper()}",
            "language": detected_lang,
            "detected_languages": [detected_lang, "en"],
            "segments": segments,
            "full_text": full_text,
            "provider": "gnani_prisma_v2.5 (Simulated / Demo Mode)" if is_mock else "gnani_prisma_v2.5",
            "is_mock": is_mock
        }
