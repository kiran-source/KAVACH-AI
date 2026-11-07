import os
import io
import pytest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException

from app.core.config import settings
from app.gnani.prisma_client import GnaniPrismaClient
from app.gnani.timbre_client import GnaniTimbreClient
from app.detection.engine import analyze_transcript

# ============================================================================
# 1. CONFIGURATION LOADING
# ============================================================================
def test_gnani_configuration_loading():
    assert settings.GNANI_PRISMA_ENDPOINT == "https://api.vachana.ai/stt/v3"
    assert settings.GNANI_TIMBRE_ENDPOINT == "https://api.vachana.ai/api/v1/tts/inference"
    assert isinstance(settings.DEMO_MODE, bool)
    assert settings.RETENTION_DAYS >= 1
    assert settings.MAX_UPLOAD_SIZE_MB >= 10

# ============================================================================
# 2. MISSING / PLACEHOLDER API KEY HANDLING
# ============================================================================
def test_missing_or_placeholder_key_in_demo_mode():
    client = GnaniPrismaClient()
    client.api_key = "YOUR_ACTUAL_API_KEY"
    
    # Should safely return simulated transcript rather than throwing an exception
    dummy_wav = "data/synthetic_audio/ambig-001_clean.wav"
    if os.path.exists(dummy_wav):
        res = client.transcribe(dummy_wav, language="hi")
        assert res["is_mock"] is True
        assert "Simulated" in res["provider"]

# ============================================================================
# 3. PRISMA V3.0 REQUEST CONSTRUCTION
# ============================================================================
def test_prisma_request_construction_with_mock():
    client = GnaniPrismaClient()
    client.api_key = "test_valid_key_1234567890"
    
    dummy_wav = "data/synthetic_audio/ambig-001_clean.wav"
    if not os.path.exists(dummy_wav):
        pytest.skip("Test audio sample not found")

    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "success": True,
        "request_id": "REQ-MOCK-PRISMA-001",
        "transcript": "Namaste aapka CBI money laundering case mein naam aaya hai.",
        "model": "prisma-v3.0",
        "detected_language_code": "hi-IN"
    }

    with patch("requests.post", return_value=mock_resp) as mock_post:
        with patch.object(settings, "DEMO_MODE", False):
            res = client.transcribe(dummy_wav, language="hi")
            
            # Verify request headers and fields
            mock_post.assert_called_once()
            call_kwargs = mock_post.call_args[1]
            headers = call_kwargs["headers"]
            assert headers["X-API-Key-ID"] == "test_valid_key_1234567890"
            assert "audio_file" in call_kwargs["files"]
            assert call_kwargs["data"]["model"] == "prisma-v3.0"
            assert call_kwargs["data"]["language_code"] == "hi-IN"

            # Verify parsed output
            assert res["is_mock"] is False
            assert res["full_text"] == "Namaste aapka CBI money laundering case mein naam aaya hai."
            assert res["language"] == "hi-IN"

# ============================================================================
# 4. TIMBRE V2.5 REQUEST CONSTRUCTION & BINARY AUDIO HANDLING
# ============================================================================
def test_timbre_request_construction_with_mock():
    client = GnaniTimbreClient()
    client.api_key = "test_valid_key_1234567890"

    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.headers = {"content-type": "audio/wav"}
    mock_resp.content = b"RIFF" + b"\x00" * 100 # Simulated valid WAV header

    with patch("requests.post", return_value=mock_resp) as mock_post:
        with patch.object(settings, "DEMO_MODE", False), patch.object(settings, "GNANI_API_KEY", "test_valid_key_1234567890"):
            res = client.generate_speech("Beware of digital arrest scams.", language="en")
            
            mock_post.assert_called_once()
            call_kwargs = mock_post.call_args[1]
            headers = call_kwargs["headers"]
            assert headers["X-API-Key-ID"] == "test_valid_key_1234567890"
            assert headers["Content-Type"] == "application/json"
            
            payload = call_kwargs["json"]
            assert payload["model"] == "timbre-v2.5"
            assert payload["voice"] == "Nalini"
            assert payload["language"] == "en-IN"
            assert payload["audio_config"]["container"] == "wav"

            assert res["status"] == "success"
            assert res["is_fallback"] is False
            assert res["provider"] == "gnani_timbre_v2.5"
            assert len(res["audio_bytes"]) > 44

# ============================================================================
# 5. API FAILURE HANDLING IN REAL MODE
# ============================================================================
def test_real_mode_raises_on_auth_failure():
    client = GnaniPrismaClient()
    client.api_key = "invalid_key_xyz"
    
    dummy_wav = "data/synthetic_audio/ambig-001_clean.wav"
    if not os.path.exists(dummy_wav):
        pytest.skip("Test audio sample not found")

    mock_resp = MagicMock()
    mock_resp.status_code = 401
    mock_resp.text = "Unauthorized"

    with patch("requests.post", return_value=mock_resp):
        with patch.object(settings, "DEMO_MODE", False):
            with pytest.raises(HTTPException) as exc_info:
                client.transcribe(dummy_wav, language="en")
            assert exc_info.value.status_code == 401

# ============================================================================
# 6. DEMO MODE SEPARATION
# ============================================================================
def test_demo_mode_separation():
    client = GnaniPrismaClient()
    dummy_wav = "data/synthetic_audio/ambig-001_clean.wav"
    if not os.path.exists(dummy_wav):
        pytest.skip("Test audio sample not found")

    with patch.object(settings, "DEMO_MODE", True):
        res = client.transcribe(dummy_wav, language="hi")
        assert res["is_mock"] is True
        assert "Demo Mode" in res["provider"]

# ============================================================================
# 7. END-TO-END PIPELINE: TRANSCRIPT TO DETECTION & RISK SCORING
# ============================================================================
def test_end_to_end_pipeline_with_real_transcript():
    # Test text obtained from Gnani Prisma V3.0 live run
    real_stt_text = "Namaste, your State Bank of India account KYC verification is pending, please update your details."
    
    # Send through KAVACH rule engine
    res = analyze_transcript(real_stt_text, language_hint="en")
    
    assert res["risk_score"] > 0
    assert "Credential Theft" in res["categories"] or "Urgency and Threats" in res["categories"]
    assert len(res["recommendations"]) >= 1
    assert res["engine_version"] == "1.0.0"
