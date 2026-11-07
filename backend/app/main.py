import os
import uuid
import json
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException, status, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.config import settings
from app.core.logging import logger
from app.database.session import init_db, get_db
from app.database.models import (
    AudioFileDB, TranscriptDB, TranscriptSegmentDB, 
    AnalysisResultDB, DetectedThreatDB, IncidentDB, 
    IncidentTimelineDB, ReportDB, FeedbackDB, SystemSettingsDB
)
from app.audio.processor import (
    save_upload_file, delete_audio_file, extract_audio_metadata, purge_expired_audio_files
)
from app.audio.validator import read_and_validate_stream, sanitize_filename
from app.gnani.prisma_service import process_transcription, generate_warning_audio
from app.detection.engine import analyze_transcript, get_safety_warning_text
from app.ml import perform_hybrid_analysis
from app.ml.hybrid_engine import get_hybrid_engine
from app.ml.hybrid_config import HybridEngineConfig, HybridMode
from app.reports.pdf_generator import generate_pdf_report
from app.services.evaluation import run_evaluation_pipeline, LABELS_FILE

# Initialize DB and validate runtime environment
init_db()
settings.validate_runtime_mode()
logger.info(f"KAVACH AI Backend initialized. Runtime mode: {'DEMO' if settings.DEMO_MODE else 'REAL API'}. SQLite ready.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Multilingual AI-Powered Voice Scam Detection and Security Incident Response Platform",
    version="1.0.0"
)

# Secure CORS Middleware with explicit origins and Vercel preview domain support
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_allowed_origins(),
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Runtime verification state tracker (distinguishes live session calls from disk history)
SESSION_LIVE_VERIFIED: Dict[str, Any] = {
    "prisma": False,
    "timbre": False,
    "last_verified_at": None
}

# Strict Localhost Authorization Middleware
@app.middleware("http")
async def enforce_localhost_only(request: Request, call_next):
    """
    Enforces strict local access boundary for the SOC prototype.
    Blocks any remote LAN / WAN IP from accessing audio, incidents, or reports.
    """
    client_host = request.client.host if request.client else ""
    # Allow local loopback and internal test harnesses
    if client_host and client_host not in ["127.0.0.1", "localhost", "::1", "testclient"]:
        logger.warning(f"Unauthorized external access attempt blocked from: {client_host}")
        return JSONResponse(
            status_code=403,
            content={"detail": "Access Forbidden: KAVACH AI SOC is restricted to local machine access only."}
        )
    return await call_next(request)

# Mount warnings directory for audio serving if exists
WARNING_AUDIO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../uploads/warnings"))
os.makedirs(WARNING_AUDIO_DIR, exist_ok=True)
app.mount("/static/warnings", StaticFiles(directory=WARNING_AUDIO_DIR), name="warnings")

# ============================================================================
# 1. HEALTH & PROVIDER ENDPOINTS
# ============================================================================
@app.get("/api/v1/health")
def health_check():
    return {
        "status": "healthy",
        "service": "KAVACH AI Backend",
        "version": "1.0.0",
        "demo_mode": settings.DEMO_MODE,
        "environment": "development"
    }

@app.get("/api/v1/health/providers")
def provider_health():
    """
    Returns granular provider status distinguishing configured, verified, 
    simulated demo mode, and unavailable states without leaking secrets.
    """
    key_configured = settings.is_api_key_configured()
    
    if settings.DEMO_MODE:
        prisma_status = "simulated_demo_mode"
        timbre_status = "local_tts_fallback"
    elif key_configured:
        # Distinguish verified within this live session vs configured and ready
        prisma_status = "verified_in_session" if SESSION_LIVE_VERIFIED["prisma"] else "configured_ready_for_inference"
        timbre_status = "verified_in_session" if SESSION_LIVE_VERIFIED["timbre"] else "configured_ready_for_inference"
    else:
        prisma_status = "unavailable_missing_credentials"
        timbre_status = "unavailable_missing_credentials"

    return {
        "gnani_prisma": {
            "name": "Gnani Prisma v3.0 Speech-to-Text",
            "status": prisma_status,
            "version": "v3.0",
            "endpoint": settings.GNANI_PRISMA_ENDPOINT,
            "languages": ["en-IN", "hi-IN", "te-IN", "indic-auto"]
        },
        "gnani_timbre": {
            "name": "Gnani Timbre v2.5 Text-to-Speech",
            "status": timbre_status,
            "version": "v2.5",
            "endpoint": settings.GNANI_TIMBRE_ENDPOINT,
            "voice": "Nalini",
            "languages": ["en-IN", "hi-IN", "te-IN"]
        },
        "gnani_evon": {
            "name": "Gnani Evon v3.3 Text Generation",
            "status": "unavailable_scope_not_allowed",
            "version": "v3.3",
            "details": "Hosted REST API inference returned 403 SCOPE_NOT_ALLOWED; text generation executed via Domain-Curated Multilingual Scenario Engine."
        }
    }

# ============================================================================
# 2. AUDIO INGESTION & MANAGEMENT ENDPOINTS
# ============================================================================
@app.post("/api/v1/audio/upload")
async def upload_audio(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload audio file with chunked streaming validation and magic bytes inspection."""
    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    content, ext = await read_and_validate_stream(file, max_bytes)
    audio_info = save_upload_file(content, file.filename or "upload.wav")

    db_audio = AudioFileDB(
        id=audio_info["audio_id"],
        original_filename=audio_info["original_filename"],
        stored_path=audio_info["stored_path"],
        file_size=audio_info["file_size"],
        duration=audio_info["duration"],
        format=audio_info["format"],
        retention_status="active"
    )
    db.add(db_audio)
    db.commit()

    return {
        "success": True,
        "audio_id": audio_info["audio_id"],
        "filename": audio_info["original_filename"],
        "duration": audio_info["duration"],
        "size": audio_info["file_size"],
        "format": audio_info["format"]
    }

@app.post("/api/v1/audio/recording")
async def upload_recording(
    audio_blob: UploadFile = File(...),
    duration_estimate: float = Form(0.0),
    db: Session = Depends(get_db)
):
    """Receive live audio recording from frontend microphone with streaming validation."""
    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    content, ext = await read_and_validate_stream(audio_blob, max_bytes)
    
    timestamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
    filename = f"mic_recording_{timestamp}.wav"
    audio_info = save_upload_file(content, filename)
    if duration_estimate > 0:
        audio_info["duration"] = round(duration_estimate, 2)

    db_audio = AudioFileDB(
        id=audio_info["audio_id"],
        original_filename=audio_info["original_filename"],
        stored_path=audio_info["stored_path"],
        file_size=audio_info["file_size"],
        duration=audio_info["duration"],
        format="wav",
        retention_status="active"
    )
    db.add(db_audio)
    db.commit()

    return {
        "success": True,
        "audio_id": audio_info["audio_id"],
        "filename": audio_info["original_filename"],
        "duration": audio_info["duration"],
        "size": audio_info["file_size"]
    }

@app.post("/api/v1/audio/purge-expired")
def purge_expired_audio(db: Session = Depends(get_db)):
    """Purge audio recordings older than the configured data retention window."""
    purged = purge_expired_audio_files(db, settings.RETENTION_DAYS)
    return {
        "success": True,
        "purged_count": purged,
        "retention_days": settings.RETENTION_DAYS,
        "message": f"Purged {purged} audio recordings past retention window."
    }

@app.get("/api/v1/audio/{audio_id}")
def get_audio(audio_id: str, db: Session = Depends(get_db)):
    """Retrieve audio metadata or stream audio binary."""
    audio = db.query(AudioFileDB).filter(AudioFileDB.id == audio_id).first()
    if not audio:
        raise HTTPException(status_code=404, detail="Audio file not found")
        
    if os.path.exists(audio.stored_path):
        media_type = f"audio/{audio.format}" if audio.format in ["wav", "mp3", "ogg"] else "audio/wav"
        return FileResponse(audio.stored_path, media_type=media_type, filename=audio.original_filename)
        
    return {
        "audio_id": audio.id,
        "original_filename": audio.original_filename,
        "file_size": audio.file_size,
        "duration": audio.duration,
        "format": audio.format,
        "created_at": audio.created_at
    }

@app.delete("/api/v1/audio/{audio_id}")
def delete_audio(audio_id: str, db: Session = Depends(get_db)):
    """Delete audio file and cascade records for privacy / data retention compliance."""
    audio = db.query(AudioFileDB).filter(AudioFileDB.id == audio_id).first()
    if not audio:
        raise HTTPException(status_code=404, detail="Audio file not found")

    delete_audio_file(audio.stored_path)
    db.delete(audio)
    db.commit()
    return {"success": True, "message": f"Audio file {audio_id} deleted."}

# ============================================================================
# 3. TRANSCRIPTION (GNANI PRISMA v3)
# ============================================================================
@app.post("/api/v1/transcription/{audio_id}")
def transcribe_audio(audio_id: str, language: str = Form("auto"), db: Session = Depends(get_db)):
    """Transcribes audio using Gnani Prisma v3 STT."""
    audio = db.query(AudioFileDB).filter(AudioFileDB.id == audio_id).first()
    if not audio:
        raise HTTPException(status_code=404, detail="Audio file not found")

    transcript_res = process_transcription(audio.stored_path, language)
    if not transcript_res.get("is_mock"):
        SESSION_LIVE_VERIFIED["prisma"] = True
        SESSION_LIVE_VERIFIED["last_verified_at"] = datetime.now(timezone.utc).isoformat()

    transcript_id = transcript_res["transcript_id"]

    db_transcript = TranscriptDB(
        id=transcript_id,
        audio_id=audio_id,
        full_text=transcript_res["full_text"],
        detected_language=transcript_res["language"],
        provider=transcript_res["provider"]
    )
    db.add(db_transcript)

    for seg in transcript_res.get("segments", []):
        db_seg = TranscriptSegmentDB(
            id=str(uuid.uuid4()),
            transcript_id=transcript_id,
            start_time=seg["start"],
            end_time=seg["end"],
            text=seg["text"],
            language=seg.get("language", transcript_res["language"])
        )
        db.add(db_seg)

    db.commit()
    return transcript_res

@app.get("/api/v1/transcription/{transcript_id}")
def get_transcript(transcript_id: str, db: Session = Depends(get_db)):
    """Retrieve detailed transcript by ID with segment timestamps."""
    tr = db.query(TranscriptDB).filter(TranscriptDB.id == transcript_id).first()
    if not tr:
        raise HTTPException(status_code=404, detail="Transcript not found")

    segments = [{"start": s.start_time, "end": s.end_time, "text": s.text, "language": s.language} for s in tr.segments]
    return {
        "transcript_id": tr.id,
        "audio_id": tr.audio_id,
        "full_text": tr.full_text,
        "language": tr.detected_language,
        "detected_languages": [tr.detected_language, "en"],
        "segments": segments,
        "provider": tr.provider,
        "created_at": tr.created_at
    }

# ============================================================================
# 4. THREAT ANALYSIS & RISK SCORING
# ============================================================================
@app.post("/api/v1/analysis/{transcript_id}")
def analyze_transcript_endpoint(transcript_id: str, db: Session = Depends(get_db)):
    """Analyzes transcript using Hybrid Risk Engine (Rules + Calibrated ML), calculates risk score, and initiates incidents."""
    tr = db.query(TranscriptDB).filter(TranscriptDB.id == transcript_id).first()
    if not tr:
        raise HTTPException(status_code=404, detail="Transcript not found")

    hybrid_res = perform_hybrid_analysis(tr.full_text, language_hint=tr.detected_language)
    analysis_id = f"AN-{uuid.uuid4().hex[:8].upper()}"

    db_analysis = AnalysisResultDB(
        id=analysis_id,
        transcript_id=transcript_id,
        risk_score=hybrid_res.risk_score,
        severity=hybrid_res.severity,
        analysis_status="completed",
        engine_version=hybrid_res.engine_version,
        detection_mode=hybrid_res.detection_mode,
        ml_predicted_class=hybrid_res.ml_result.predicted_class if hybrid_res.ml_result else None,
        ml_confidence=hybrid_res.ml_result.confidence if hybrid_res.ml_result else None,
        ml_model_version=hybrid_res.ml_result.model_version if hybrid_res.ml_result else None,
        rule_score=hybrid_res.rule_score,
        ml_score=hybrid_res.ml_score
    )
    db.add(db_analysis)

    for th in hybrid_res.threats:
        db_th = DetectedThreatDB(
            id=str(uuid.uuid4()),
            analysis_id=analysis_id,
            rule_id=th["rule_id"],
            category=th["category"],
            matched_text=th["matched_text"],
            evidence_start=th.get("evidence_start"),
            evidence_end=th.get("evidence_end"),
            contribution=th["contribution"],
            explanation=th["explanation"]
        )
        db.add(db_th)

    # Automated incident creation for Medium, High, or Critical threats (risk >= 40)
    created_incident_id = None
    if hybrid_res.risk_score >= 40.0:
        incident_num = f"INC-{uuid.uuid4().hex[:6].upper()}"
        primary_threat = hybrid_res.categories[0] if hybrid_res.categories else "Social Engineering"
        db_inc = IncidentDB(
            id=str(uuid.uuid4()),
            incident_number=incident_num,
            analysis_id=analysis_id,
            title=f"{primary_threat} Detected ({hybrid_res.severity} Risk)",
            severity=hybrid_res.severity,
            status="New",
            assigned_analyst="SOC Analyst 1",
            analyst_notes=f"Auto-generated SOC incident from voice scan. Mode: {hybrid_res.detection_mode}. Risk score: {hybrid_res.risk_score}/100. Tactic categories: {', '.join(hybrid_res.categories)}."
        )
        db.add(db_inc)
        db.flush()
        created_incident_id = db_inc.id

        db_timeline = IncidentTimelineDB(
            id=str(uuid.uuid4()),
            incident_id=db_inc.id,
            event_type="Detection",
            description=f"Detection ({hybrid_res.detection_mode}): Rule score {hybrid_res.rule_score:.1f}, ML score {hybrid_res.ml_score if hybrid_res.ml_score is not None else 'N/A'}. Final risk: {hybrid_res.risk_score:.1f}/100 ({hybrid_res.severity})."
        )
        db.add(db_timeline)

    db.commit()

    return {
        "analysis_id": analysis_id,
        "transcript_id": transcript_id,
        "detection_mode": hybrid_res.detection_mode,
        "risk_score": hybrid_res.risk_score,
        "severity": hybrid_res.severity,
        "rule_score": hybrid_res.rule_score,
        "ml_score": hybrid_res.ml_score,
        "ml_result": hybrid_res.ml_result.model_dump() if hybrid_res.ml_result else None,
        "threats": hybrid_res.threats,
        "categories": hybrid_res.categories,
        "recommendations": hybrid_res.recommendations,
        "context_suppressed": hybrid_res.context_suppressed,
        "context_note": hybrid_res.context_note,
        "conflict_detected": hybrid_res.conflict_detected,
        "conflict_explanation": hybrid_res.conflict_explanation,
        "explanation": hybrid_res.explanation,
        "incident_id": created_incident_id
    }

@app.post("/api/v1/analysis/text")
def analyze_raw_text(text: str = Form(...), language: str = Form("en")):
    """Evaluates raw transcript text using Hybrid Risk Engine for fast incremental threat scoring (used by live microphone chunk analysis)."""
    if not text or not text.strip():
        return {
            "detection_mode": "RULE_ONLY",
            "risk_score": 0.0,
            "severity": "Low",
            "rule_score": 0.0,
            "ml_score": None,
            "threats": [],
            "categories": [],
            "recommendations": [],
            "context_suppressed": False,
            "explanation": "No text provided for analysis."
        }
    hybrid_res = perform_hybrid_analysis(text.strip(), language_hint=language)
    return {
        "detection_mode": hybrid_res.detection_mode,
        "risk_score": hybrid_res.risk_score,
        "severity": hybrid_res.severity,
        "rule_score": hybrid_res.rule_score,
        "ml_score": hybrid_res.ml_score,
        "ml_result": hybrid_res.ml_result.model_dump() if hybrid_res.ml_result else None,
        "threats": hybrid_res.threats,
        "categories": hybrid_res.categories,
        "recommendations": hybrid_res.recommendations,
        "context_suppressed": hybrid_res.context_suppressed,
        "context_note": hybrid_res.context_note,
        "conflict_detected": hybrid_res.conflict_detected,
        "conflict_explanation": hybrid_res.conflict_explanation,
        "explanation": hybrid_res.explanation
    }

# ============================================================================
# 4.1 EXPERIMENTAL HYBRID INTELLIGENCE ENGINE (TF-IDF v3 + MuRIL v1)
# ============================================================================
class HybridAnalysisRequest(BaseModel):
    text: str = ""
    language: Optional[str] = "en"
    mode: Optional[str] = "hybrid_selective"

@app.post("/api/v1/hybrid/analyze")
def analyze_with_hybrid_engine(payload: HybridAnalysisRequest):
    """
    Experimental Hybrid Intelligence endpoint:
    Combines Deterministic Rule-Priority Shield, TF-IDF v3 Fast Classifier,
    Selective MuRIL v1 Multilingual Transformer, and Safety-First Decision Fusion.
    """
    input_text = payload.text if payload else ""
    input_lang = (payload.language or "en") if payload else "en"
    input_mode = (payload.mode or "hybrid_selective") if payload else "hybrid_selective"

    if not input_text or not input_text.strip():
        return {
            "status": "EMPTY_INPUT",
            "final_decision": "AMBIGUOUS",
            "final_risk_score": 0.0,
            "severity": "Low",
            "rule_score": 0.0,
            "critical_rule_triggered": False,
            "rule_shield_active": False,
            "tfidf_result": None,
            "muril_invoked": False,
            "muril_result": None,
            "explanation": "No text provided for hybrid analysis."
        }

    try:
        cfg = HybridEngineConfig(
            mode=HybridMode(input_mode) if input_mode in [m.value for m in HybridMode] else HybridMode.HYBRID_SELECTIVE
        )
        engine = get_hybrid_engine(cfg)
        res = engine.analyze(input_text.strip(), language_hint=input_lang)
        out = res.to_dict()
        out["status"] = "SUCCESS"
        return out
    except Exception as e:
        logger.error(f"Hybrid analysis error: {e}")
        # Graceful fallback to deterministic rule engine
        fallback_rule = analyze_transcript(input_text.strip(), language_hint=input_lang)
        return {
            "status": "FALLBACK_RULE_ONLY",
            "error": str(e),
            "final_decision": "SCAM" if fallback_rule.get("risk_score", 0.0) >= 40.0 else "LEGITIMATE",
            "final_risk_score": fallback_rule.get("risk_score", 0.0),
            "severity": fallback_rule.get("severity", "Low"),
            "rule_score": fallback_rule.get("risk_score", 0.0),
            "critical_rule_triggered": False,
            "rule_shield_active": False,
            "tfidf_result": None,
            "muril_invoked": False,
            "muril_result": None,
            "explanation": "Hybrid engine error; safely reverted to deterministic rules."
        }

@app.get("/api/v1/analysis/{analysis_id}")
def get_analysis(analysis_id: str, db: Session = Depends(get_db)):
    """Retrieve full analysis report by ID."""
    an = db.query(AnalysisResultDB).filter(AnalysisResultDB.id == analysis_id).first()
    if not an:
        raise HTTPException(status_code=404, detail="Analysis result not found")

    threats = [{
        "rule_id": t.rule_id,
        "category": t.category,
        "matched_text": t.matched_text,
        "evidence_start": t.evidence_start,
        "evidence_end": t.evidence_end,
        "contribution": t.contribution,
        "explanation": t.explanation
    } for t in an.threats]

    tr = an.transcript
    return {
        "analysis_id": an.id,
        "transcript_id": an.transcript_id,
        "risk_score": an.risk_score,
        "severity": an.severity,
        "threats": threats,
        "engine_version": an.engine_version,
        "created_at": an.created_at,
        "full_text": tr.full_text if tr else "",
        "detected_language": tr.detected_language if tr else "en",
        "audio_id": tr.audio_id if tr else None
    }

@app.get("/api/v1/analysis")
def list_analyses(limit: int = 50, db: Session = Depends(get_db)):
    """List recent call analyses."""
    analyses = db.query(AnalysisResultDB).order_by(AnalysisResultDB.created_at.desc()).limit(limit).all()
    results = []
    for an in analyses:
        tr = an.transcript
        results.append({
            "analysis_id": an.id,
            "transcript_id": an.transcript_id,
            "risk_score": an.risk_score,
            "severity": an.severity,
            "created_at": an.created_at,
            "language": tr.detected_language if tr else "en",
            "snippet": tr.full_text[:80] if tr and tr.full_text else ""
        })
    return results

# ============================================================================
# 5. SAFETY WARNINGS (GNANI TIMBRE v2.5)
# ============================================================================
@app.post("/api/v1/warnings/generate")
def generate_warning(
    language: str = Form("en"),
    categories: str = Form(""),
    custom_text: Optional[str] = Form(None)
):
    """Synthesizes multilingual voice safety warning using Gnani Timbre v2.5."""
    cats = [c.strip() for c in categories.split(",") if c.strip()]
    text = custom_text or get_safety_warning_text(language, cats)

    tts_result = generate_warning_audio(text, language)
    if not tts_result.get("is_fallback"):
        SESSION_LIVE_VERIFIED["timbre"] = True
        SESSION_LIVE_VERIFIED["last_verified_at"] = datetime.now(timezone.utc).isoformat()

    audio_filename = tts_result["filename"]
    audio_url = f"/static/warnings/{audio_filename}"

    return {
        "success": True,
        "language": language,
        "warning_text": text,
        "audio_url": audio_url,
        "provider": tts_result["provider"],
        "is_fallback": tts_result["is_fallback"]
    }

# ============================================================================
# 6. INCIDENT MANAGEMENT
# ============================================================================
@app.get("/api/v1/incidents")
def list_incidents(status: Optional[str] = None, severity: Optional[str] = None, db: Session = Depends(get_db)):
    """Retrieve security incidents with optional status/severity filtering."""
    query = db.query(IncidentDB)
    if status and status != "All":
        query = query.filter(IncidentDB.status == status)
    if severity and severity != "All":
        query = query.filter(IncidentDB.severity == severity)

    incidents = query.order_by(IncidentDB.created_at.desc()).all()
    results = []
    for inc in incidents:
        analysis = inc.analysis
        results.append({
            "id": inc.id,
            "incident_number": inc.incident_number,
            "title": inc.title,
            "severity": inc.severity,
            "status": inc.status,
            "assigned_analyst": inc.assigned_analyst,
            "risk_score": analysis.risk_score if analysis else 0.0,
            "created_at": inc.created_at,
            "updated_at": inc.updated_at
        })
    return results

@app.get("/api/v1/incidents/{incident_id}")
def get_incident(incident_id: str, db: Session = Depends(get_db)):
    """Retrieve complete incident details, evidence, and timeline."""
    inc = db.query(IncidentDB).filter(IncidentDB.id == incident_id).first()
    if not inc:
        raise HTTPException(status_code=404, detail="Incident not found")

    analysis = inc.analysis
    transcript = analysis.transcript if analysis else None
    audio = transcript.audio_file if transcript else None

    threats = []
    if analysis:
        threats = [{
            "category": t.category,
            "matched_text": t.matched_text,
            "contribution": t.contribution,
            "explanation": t.explanation
        } for t in analysis.threats]

    timeline = [{
        "event_type": tm.event_type,
        "description": tm.description,
        "event_time": tm.event_time
    } for tm in inc.timeline]

    # Check if a report has been generated
    report = inc.reports[0] if inc.reports else None

    return {
        "id": inc.id,
        "incident_number": inc.incident_number,
        "analysis_id": inc.analysis_id,
        "title": inc.title,
        "severity": inc.severity,
        "status": inc.status,
        "assigned_analyst": inc.assigned_analyst,
        "analyst_notes": inc.analyst_notes,
        "created_at": inc.created_at,
        "updated_at": inc.updated_at,
        "risk_score": analysis.risk_score if analysis else 0.0,
        "transcript_text": transcript.full_text if transcript else "",
        "detected_language": transcript.detected_language if transcript else "en",
        "audio_filename": audio.original_filename if audio else "N/A",
        "audio_id": audio.id if audio else None,
        "threats": threats,
        "timeline": timeline,
        "report_id": report.id if report else None
    }

@app.patch("/api/v1/incidents/{incident_id}")
def update_incident(
    incident_id: str,
    status: Optional[str] = Form(None),
    assigned_analyst: Optional[str] = Form(None),
    analyst_notes: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """Updates incident status or assigned analyst and records audit event in timeline."""
    inc = db.query(IncidentDB).filter(IncidentDB.id == incident_id).first()
    if not inc:
        raise HTTPException(status_code=404, detail="Incident not found")

    old_status = inc.status
    if status and isinstance(status, str) and status != old_status:
        inc.status = status
        db_timeline = IncidentTimelineDB(
            id=str(uuid.uuid4()),
            incident_id=inc.id,
            event_type="Status Change",
            description=f"Status transitioned from '{old_status}' to '{status}'."
        )
        db.add(db_timeline)

    if assigned_analyst and isinstance(assigned_analyst, str):
        inc.assigned_analyst = assigned_analyst

    if analyst_notes is not None and isinstance(analyst_notes, str):
        inc.analyst_notes = analyst_notes
        db_timeline = IncidentTimelineDB(
            id=str(uuid.uuid4()),
            incident_id=inc.id,
            event_type="Analyst Note Added",
            description="Analyst investigation notes updated."
        )
        db.add(db_timeline)

    inc.updated_at = datetime.now(timezone.utc)
    db.commit()
    return {"success": True, "message": "Incident updated successfully", "status": inc.status}

@app.post("/api/v1/incidents/{incident_id}/notes")
def add_incident_note(incident_id: str, notes: str = Form(...), db: Session = Depends(get_db)):
    """Appends note to incident investigation log."""
    inc = db.query(IncidentDB).filter(IncidentDB.id == incident_id).first()
    if not inc:
        raise HTTPException(status_code=404, detail="Incident not found")

    current_notes = inc.analyst_notes or ""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    new_entry = f"[{timestamp}] {notes}"
    inc.analyst_notes = f"{current_notes}\n{new_entry}".strip()
    inc.updated_at = datetime.now(timezone.utc)

    db_timeline = IncidentTimelineDB(
        id=str(uuid.uuid4()),
        incident_id=inc.id,
        event_type="Analyst Log",
        description=f"Appended investigation note: {notes[:80]}"
    )
    db.add(db_timeline)
    db.commit()

    return {"success": True, "analyst_notes": inc.analyst_notes}

# ============================================================================
# 7. SOC REPORT GENERATION & PDF EXPORT
# ============================================================================
@app.post("/api/v1/reports/{incident_id}")
def create_report(incident_id: str, db: Session = Depends(get_db)):
    """Generates official SOC Incident Report PDF."""
    inc = db.query(IncidentDB).filter(IncidentDB.id == incident_id).first()
    if not inc:
        raise HTTPException(status_code=404, detail="Incident not found")

    analysis = inc.analysis
    transcript = analysis.transcript if analysis else None

    threats = []
    if analysis:
        threats = [{
            "category": t.category,
            "matched_text": t.matched_text,
            "contribution": t.contribution,
            "explanation": t.explanation
        } for t in analysis.threats]

    incident_data = {
        "incident_number": inc.incident_number,
        "title": inc.title,
        "severity": inc.severity,
        "status": inc.status,
        "risk_score": analysis.risk_score if analysis else 0.0,
        "detection_mode": getattr(analysis, "detection_mode", "RULE_ONLY") if analysis else "RULE_ONLY",
        "ml_predicted_class": getattr(analysis, "ml_predicted_class", None) if analysis else None,
        "ml_confidence": getattr(analysis, "ml_confidence", None) if analysis else None,
        "rule_score": getattr(analysis, "rule_score", None) if analysis else None,
        "ml_score": getattr(analysis, "ml_score", None) if analysis else None,
        "assigned_analyst": inc.assigned_analyst,
        "created_at": inc.created_at.strftime("%Y-%m-%d %H:%M:%S UTC") if inc.created_at else "N/A",
        "transcript_text": transcript.full_text if transcript else "",
        "detected_language": transcript.detected_language if transcript else "en",
        "threats": threats,
        "analyst_notes": inc.analyst_notes
    }

    pdf_path = generate_pdf_report(incident_data)

    db_rep = ReportDB(
        id=str(uuid.uuid4()),
        incident_id=incident_id,
        file_path=pdf_path
    )
    db.add(db_rep)

    db_timeline = IncidentTimelineDB(
        id=str(uuid.uuid4()),
        incident_id=inc.id,
        event_type="Report Generated",
        description=f"Official SOC Incident Report PDF generated ({os.path.basename(pdf_path)})."
    )
    db.add(db_timeline)
    db.commit()

    return {
        "success": True,
        "report_id": db_rep.id,
        "file_path": pdf_path,
        "download_url": f"/api/v1/reports/{db_rep.id}/download"
    }

@app.get("/api/v1/reports")
def list_reports(db: Session = Depends(get_db)):
    """List all generated incident reports."""
    reports = db.query(ReportDB).order_by(ReportDB.generated_at.desc()).all()
    results = []
    for r in reports:
        inc = r.incident
        results.append({
            "report_id": r.id,
            "incident_id": r.incident_id,
            "incident_number": inc.incident_number if inc else "N/A",
            "title": inc.title if inc else "Incident Report",
            "severity": inc.severity if inc else "Medium",
            "generated_at": r.generated_at,
            "download_url": f"/api/v1/reports/{r.id}/download"
        })
    return results

@app.get("/api/v1/reports/{report_id}/download")
def download_report(report_id: str, db: Session = Depends(get_db)):
    """Download generated PDF report."""
    rep = db.query(ReportDB).filter(ReportDB.id == report_id).first()
    if not rep or not os.path.exists(rep.file_path):
        raise HTTPException(status_code=404, detail="Report file not found")
    return FileResponse(rep.file_path, media_type="application/pdf", filename=os.path.basename(rep.file_path))

# ============================================================================
# 8. SOC DASHBOARD METRICS (COMPUTED FROM ACTUAL DB)
# ============================================================================
@app.get("/api/v1/dashboard/metrics")
def get_dashboard_metrics(db: Session = Depends(get_db)):
    """Calculates live SOC operational metrics directly from SQLite records."""
    total_analyses = db.query(AnalysisResultDB).count()
    total_incidents = db.query(IncidentDB).count()

    high_risk = db.query(IncidentDB).filter(IncidentDB.severity.in_(["High", "Critical"])).count()
    medium_risk = db.query(IncidentDB).filter(IncidentDB.severity == "Medium").count()
    low_risk = db.query(IncidentDB).filter(IncidentDB.severity.in_(["Low", "Guarded"])).count()
    safe_calls = db.query(AnalysisResultDB).filter(AnalysisResultDB.risk_score < 20.0).count()

    avg_score = db.query(func.avg(AnalysisResultDB.risk_score)).scalar() or 0.0

    # Risk distribution
    critical_count = db.query(AnalysisResultDB).filter(AnalysisResultDB.severity == "Critical").count()
    high_count = db.query(AnalysisResultDB).filter(AnalysisResultDB.severity == "High").count()
    medium_count = db.query(AnalysisResultDB).filter(AnalysisResultDB.severity == "Medium").count()
    guarded_count = db.query(AnalysisResultDB).filter(AnalysisResultDB.severity == "Guarded").count()
    low_count = db.query(AnalysisResultDB).filter(AnalysisResultDB.severity == "Low").count()

    # Language distribution
    lang_records = db.query(TranscriptDB.detected_language, func.count(TranscriptDB.id)).group_by(TranscriptDB.detected_language).all()
    lang_dist = {str(lr[0] or "en"): int(lr[1]) for lr in lang_records}

    # Threat category distribution
    threat_records = db.query(DetectedThreatDB.category, func.count(DetectedThreatDB.id)).group_by(DetectedThreatDB.category).all()
    threat_dist = {str(tr[0]): int(tr[1]) for tr in threat_records}

    # False positive rate from user feedback
    fp_feedback = db.query(FeedbackDB).filter(FeedbackDB.feedback_type == "false_positive").count()
    fp_rate = round((fp_feedback / total_analyses * 100), 1) if total_analyses > 0 else 0.0

    # Detection rate
    detected_threats = total_analyses - safe_calls
    detection_rate = round((detected_threats / total_analyses * 100), 1) if total_analyses > 0 else 0.0

    recent_incidents = db.query(IncidentDB).order_by(IncidentDB.created_at.desc()).limit(5).all()
    recent_inc_list = [{
        "id": inc.id,
        "incident_number": inc.incident_number,
        "title": inc.title,
        "severity": inc.severity,
        "status": inc.status,
        "risk_score": inc.analysis.risk_score if inc.analysis else 0.0,
        "created_at": inc.created_at
    } for inc in recent_incidents]

    return {
        "total_analyzed_calls": total_analyses,
        "total_incidents": total_incidents,
        "high_risk_incidents": high_risk,
        "medium_risk_incidents": medium_risk,
        "low_risk_incidents": low_risk,
        "safe_calls": safe_calls,
        "average_risk_score": round(float(avg_score), 1),
        "detection_rate": detection_rate,
        "false_positive_rate": fp_rate,
        "risk_distribution": {
            "Critical": critical_count,
            "High": high_count,
            "Medium": medium_count,
            "Guarded": guarded_count,
            "Low": low_count
        },
        "language_distribution": lang_dist if lang_dist else {"en": 0, "hi": 0, "te": 0},
        "threat_category_distribution": threat_dist,
        "recent_incidents": recent_inc_list
    }

# ============================================================================
# 9. EVALUATION & BENCHMARKING
# ============================================================================
@app.get("/api/v1/evaluation/scenarios")
def get_evaluation_scenarios():
    """Retrieve synthetic testing dataset scenarios."""
    if not os.path.exists(LABELS_FILE):
        return []
    with open(LABELS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

@app.post("/api/v1/evaluation/run")
def trigger_evaluation_pipeline():
    """Executes automated evaluation pipeline on synthetic dataset."""
    results = run_evaluation_pipeline()
    return results

# ============================================================================
# 10. SYSTEM SETTINGS & PRIVACY
# ============================================================================
@app.get("/api/v1/settings")
def get_settings():
    is_mock = not settings.GNANI_API_KEY or settings.GNANI_API_KEY in ["mock_key", "mock_gnani_api_key_for_testing", "YOUR_ACTUAL_API_KEY", ""]
    return {
        "preferred_language": "en",
        "warning_voice_language": "en",
        "audio_retention_days": settings.RETENTION_DAYS,
        "max_upload_size_mb": settings.MAX_UPLOAD_SIZE_MB,
        "demo_mode": settings.DEMO_MODE,
        "gnani_prisma_connected": not is_mock and not settings.DEMO_MODE,
        "gnani_timbre_connected": not is_mock and not settings.DEMO_MODE,
        "gnani_evon_connected": False,
        "app_version": "1.0.0"
    }

@app.patch("/api/v1/settings")
def update_settings(demo_mode: Optional[bool] = Form(None), retention_days: Optional[int] = Form(None)):
    if demo_mode is not None:
        settings.DEMO_MODE = demo_mode
    if retention_days is not None:
        settings.RETENTION_DAYS = retention_days
    return {"success": True, "message": "Settings updated", "demo_mode": settings.DEMO_MODE}

@app.post("/api/v1/feedback")
def submit_feedback(analysis_id: str = Form(...), feedback_type: str = Form(...), comments: Optional[str] = Form(None), db: Session = Depends(get_db)):
    db_fb = FeedbackDB(
        id=str(uuid.uuid4()),
        analysis_id=analysis_id,
        feedback_type=feedback_type,
        comments=comments
    )
    db.add(db_fb)
    db.commit()
    return {"success": True, "message": "Analyst feedback recorded."}
