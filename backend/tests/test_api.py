import os
import uuid
import pytest
from app.main import (
    health_check, provider_health, get_dashboard_metrics,
    analyze_transcript_endpoint, create_report, get_incident,
    update_incident, add_incident_note, generate_warning
)
from app.database.session import SessionLocal, init_db
from app.database.models import (
    AudioFileDB, TranscriptDB, TranscriptSegmentDB, 
    AnalysisResultDB, IncidentDB, ReportDB
)
from app.detection.engine import analyze_transcript, get_safety_warning_text
from app.services.evaluation import run_evaluation_pipeline
from app.audio.processor import extract_audio_metadata
from app.gnani.prisma_service import process_transcription, generate_warning_audio

@pytest.fixture(scope="module")
def db():
    init_db()
    session = SessionLocal()
    yield session
    session.close()

def test_health_check():
    res = health_check()
    assert res["status"] == "healthy"
    assert res["service"] == "KAVACH AI Backend"
    assert res["version"] == "1.0.0"

def test_provider_health():
    res = provider_health()
    assert "gnani_prisma" in res
    assert "gnani_timbre" in res
    assert res["gnani_prisma"]["version"] == "v2.5"

def test_threat_detection_engine_credential_theft():
    text = "Sir please tell me your 6 digit OTP and UPI PIN immediately or your account will be blocked."
    res = analyze_transcript(text)
    assert res["risk_score"] >= 45.0
    assert "Credential Theft" in res["categories"]
    assert "Urgency and Threats" in res["categories"]
    assert res["severity"] in ["Medium", "High", "Critical"]

def test_threat_detection_engine_digital_arrest():
    text = "I am Inspector Sharma from CBI headquarters. You are placed under digital arrest right now. Do not disconnect the video call."
    res = analyze_transcript(text)
    assert res["risk_score"] >= 60.0
    assert "Digital Arrest Patterns" in res["categories"]
    assert "Authority Impersonation" in res["categories"]
    assert res["severity"] in ["High", "Critical"]

def test_threat_detection_engine_negative_context():
    advisory_text = "RBI security advisory: Bank never asks for your OTP or password. Stay safe from scam calls."
    res = analyze_transcript(advisory_text)
    assert res["context_suppressed"] is True
    assert res["risk_score"] < 40.0
    assert res["severity"] in ["Low", "Guarded"]

def test_multilingual_safety_warnings():
    en_warn = get_safety_warning_text("en", ["Credential Theft"])
    assert "OTP" in en_warn
    
    hi_warn = get_safety_warning_text("hi", ["Credential Theft"])
    assert "OTP" in hi_warn
    
    te_warn = get_safety_warning_text("te", ["Credential Theft"])
    assert "OTP" in te_warn

def test_audio_metadata_extraction():
    test_audio = os.path.abspath("data/synthetic_audio/scam-001_telephone-band.wav")
    if os.path.exists(test_audio):
        meta = extract_audio_metadata(test_audio)
        assert meta["duration"] > 0
        assert meta["sample_rate"] == 16000
        assert meta["channels"] == 1

def test_end_to_end_incident_and_report_flow(db):
    # 1. Create Audio File Record
    audio_id = str(uuid.uuid4())
    audio_rec = AudioFileDB(
        id=audio_id,
        original_filename="digital_arrest_sample.wav",
        stored_path=os.path.abspath("data/synthetic_audio/scam-001_telephone-band.wav"),
        file_size=192000,
        duration=6.0,
        format="wav"
    )
    db.add(audio_rec)
    db.commit()

    # 2. Transcribe
    tr_res = process_transcription(audio_rec.stored_path, language="auto")
    tr_id = tr_res["transcript_id"]
    tr_rec = TranscriptDB(
        id=tr_id,
        audio_id=audio_id,
        full_text=tr_res["full_text"],
        detected_language=tr_res["language"],
        provider=tr_res["provider"]
    )
    db.add(tr_rec)
    db.commit()

    # 3. Analyze Endpoint Call
    analysis_data = analyze_transcript_endpoint(transcript_id=tr_id, db=db)
    assert analysis_data["risk_score"] >= 40.0
    incident_id = analysis_data["incident_id"]
    assert incident_id is not None

    # 4. Inspect Incident
    incident_data = get_incident(incident_id=incident_id, db=db)
    assert incident_data["status"] == "New"
    assert len(incident_data["threats"]) > 0
    assert len(incident_data["timeline"]) >= 1

    # 5. Update Status
    update_res = update_incident(incident_id=incident_id, status="Under Review", db=db)
    assert update_res["success"] is True

    # 6. Add Note
    note_res = add_incident_note(incident_id=incident_id, notes="Verified suspect claiming CBI officer.", db=db)
    assert "Verified suspect" in note_res["analyst_notes"]

    # 7. Generate PDF Report
    report_res = create_report(incident_id=incident_id, db=db)
    assert report_res["success"] is True
    assert os.path.exists(report_res["file_path"])

    # 8. Check Dashboard Metrics reflection
    metrics = get_dashboard_metrics(db=db)
    assert metrics["total_analyzed_calls"] >= 1
    assert metrics["total_incidents"] >= 1
    assert (metrics["medium_risk_incidents"] + metrics["high_risk_incidents"]) >= 1

def test_evaluation_pipeline_metrics():
    res = run_evaluation_pipeline()
    assert res["dataset_size"] == 20
    assert res["metrics"]["f1_score"] >= 0.90
    assert res["metrics"]["precision"] >= 0.90
    assert res["metrics"]["recall"] >= 0.90
    assert res["confusion_matrix"]["false_positives"] == 0
