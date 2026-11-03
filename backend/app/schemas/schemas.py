from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

# --- Audio Schemas ---
class AudioFileMetadata(BaseModel):
    id: str
    original_filename: str
    file_size: int
    duration: float
    format: str
    retention_status: str
    created_at: datetime

    class Config:
        from_attributes = True

class AudioUploadResponse(BaseModel):
    audio_id: str
    original_filename: str
    file_size: int
    duration: float
    format: str
    message: str

# --- Transcription Schemas ---
class TranscriptSegment(BaseModel):
    start: float
    end: float
    text: str
    language: str = "en"

class TranscriptResponse(BaseModel):
    transcript_id: str
    audio_id: Optional[str] = None
    detected_language: str
    detected_languages: List[str] = ["en"]
    full_text: str
    segments: List[TranscriptSegment] = []
    provider: str = "gnani_prisma"
    is_mock: bool = False
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class TranscriptionRequest(BaseModel):
    language_hint: Optional[str] = "auto" # "en", "hi", "te", "auto"

# --- Detection & Threat Schemas ---
class ThreatDetail(BaseModel):
    rule_id: str
    category: str
    matched_text: str
    evidence_start: Optional[float] = None
    evidence_end: Optional[float] = None
    contribution: float
    explanation: str

class ThreatAnalysisResponse(BaseModel):
    analysis_id: str
    transcript_id: str
    risk_score: float # 0 to 100
    severity: str # Low, Guarded, Medium, High, Critical
    threat_categories: List[str]
    detected_tactics: List[ThreatDetail]
    recommendations: List[str]
    analysis_status: str = "completed"
    engine_version: str = "1.0.0"
    created_at: Optional[datetime] = None
    audio_id: Optional[str] = None
    full_text: Optional[str] = None
    detected_language: Optional[str] = None

    class Config:
        from_attributes = True

class AnalysisRequest(BaseModel):
    transcript_text: Optional[str] = None
    language: Optional[str] = "en"

# --- Warning & Timbre Schemas ---
class WarningRequest(BaseModel):
    language: str = "en" # "en", "hi", "te"
    categories: List[str] = []
    risk_score: Optional[float] = 0.0

class WarningResponse(BaseModel):
    language: str
    warning_text: str
    audio_url: Optional[str] = None
    provider: str = "gnani_timbre"
    is_fallback: bool = False

# --- Incident Schemas ---
class IncidentTimelineItem(BaseModel):
    event_type: str
    description: str
    event_time: datetime

    class Config:
        from_attributes = True

class IncidentCreate(BaseModel):
    analysis_id: str
    title: Optional[str] = None
    assigned_analyst: Optional[str] = "SOC Analyst 1"
    analyst_notes: Optional[str] = None

class IncidentUpdate(BaseModel):
    status: Optional[str] = None # New, Under Review, Confirmed Suspicious, False Positive, Resolved
    assigned_analyst: Optional[str] = None
    analyst_notes: Optional[str] = None

class IncidentNotesUpdate(BaseModel):
    notes: str

class IncidentResponse(BaseModel):
    id: str
    incident_number: str
    analysis_id: str
    title: str
    severity: str
    status: str
    assigned_analyst: str
    analyst_notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    risk_score: Optional[float] = None
    detected_language: Optional[str] = None
    threat_categories: List[str] = []
    timeline: List[IncidentTimelineItem] = []

    class Config:
        from_attributes = True

class IncidentDetailResponse(IncidentResponse):
    audio_metadata: Optional[AudioFileMetadata] = None
    full_text: Optional[str] = None
    detected_tactics: List[ThreatDetail] = []
    recommendations: List[str] = []
    report_id: Optional[str] = None

# --- Report Schemas ---
class ReportResponse(BaseModel):
    id: str
    incident_id: str
    incident_number: str
    file_path: str
    download_url: str
    generated_at: datetime

    class Config:
        from_attributes = True

# --- Feedback Schemas ---
class FeedbackCreate(BaseModel):
    analysis_id: str
    feedback_type: str # accurate, false_positive, false_negative
    comments: Optional[str] = None

class FeedbackResponse(BaseModel):
    id: str
    analysis_id: str
    feedback_type: str
    comments: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

# --- Dashboard Schemas ---
class DashboardMetrics(BaseModel):
    total_analyzed_calls: int
    high_risk_incidents: int
    medium_risk_incidents: int
    low_risk_incidents: int
    safe_calls: int
    detection_rate: float
    false_positive_rate: float
    average_risk_score: float
    risk_distribution: Dict[str, int]
    language_distribution: Dict[str, int]
    threat_category_distribution: Dict[str, int]
    recent_incidents: List[IncidentResponse]
    system_health: Dict[str, Any]

# --- Settings Schemas ---
class SettingsResponse(BaseModel):
    preferred_language: str
    warning_voice_language: str
    audio_retention_days: int
    max_upload_size_mb: int
    demo_mode: bool
    gnani_prisma_connected: bool
    gnani_timbre_connected: bool
    gnani_evon_connected: bool
    app_version: str

class SettingsUpdate(BaseModel):
    preferred_language: Optional[str] = None
    warning_voice_language: Optional[str] = None
    audio_retention_days: Optional[int] = None
    max_upload_size_mb: Optional[int] = None
    demo_mode: Optional[bool] = None

