import pytest
import os
import json
from fastapi.testclient import TestClient
from app.main import app
from app.detection.engine import analyze_transcript
from app.gnani.prisma_client import GnaniPrismaClient
from app.database.session import init_db

client = TestClient(app)

def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
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
    res = pc._get_mock_transcript("data/uploads/test_digital_arrest.wav", "en")
    assert "transcript_id" in res
    assert "full_text" in res
    assert len(res["segments"]) > 0
