import pytest
import os
import json
from app.main import health_check
from app.detection.engine import analyze_transcript
from app.gnani.prisma_client import GnaniPrismaClient
from fastapi import HTTPException

def test_health_check_direct():
    data = health_check()
    assert data["status"] == "healthy"
    assert data["service"] == "KAVACH AI Backend"

def test_detection_engine_scam():
    transcript = "CBI officer here. Your account is blocked. Tell me your OTP and transfer money to safe account."
    result = analyze_transcript(transcript)
    assert result["risk_score"] > 50
    assert result["severity"] in ["High", "Critical"]
    assert len(result["threats"]) > 0

def test_detection_engine_safe():
    transcript = "Hello customer support, how can I help you with your subscription today?"
    result = analyze_transcript(transcript)
    assert result["risk_score"] < 20
    assert result["severity"] == "Low"

def test_prisma_client_mock():
    pc = GnaniPrismaClient()
    dummy_wav = "data/synthetic_audio/ambig-001_clean.wav"
    res = pc._generate_simulated_transcript(dummy_wav, "en")
    assert "transcript_id" in res
    assert "full_text" in res
    assert len(res["segments"]) > 0
    assert res["is_mock"] is True

def test_prisma_empty_transcript_validation():
    pc = GnaniPrismaClient()
    empty_raw = {
        "success": True,
        "transcript": "   ",
        "detected_language_code": "en-IN"
    }
    with pytest.raises(HTTPException) as exc:
        pc._normalize_prisma_response(empty_raw, "en")
    assert exc.value.status_code == 502
    assert "empty transcript" in exc.value.detail.lower()
