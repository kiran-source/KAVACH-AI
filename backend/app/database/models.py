from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class UserDB(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class AudioFileDB(Base):
    __tablename__ = "audio_files"
    
    id = Column(String, primary_key=True, index=True)
    original_filename = Column(String)
    stored_path = Column(String)
    file_size = Column(Integer)
    duration = Column(Float, default=0.0)
    format = Column(String)
    retention_status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    transcripts = relationship("TranscriptDB", back_populates="audio_file", cascade="all, delete-orphan")

class TranscriptDB(Base):
    __tablename__ = "transcripts"
    
    id = Column(String, primary_key=True, index=True)
    audio_id = Column(String, ForeignKey("audio_files.id"))
    full_text = Column(Text)
    detected_language = Column(String, default="en")
    provider = Column(String, default="gnani_prisma")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    audio_file = relationship("AudioFileDB", back_populates="transcripts")
    segments = relationship("TranscriptSegmentDB", back_populates="transcript", cascade="all, delete-orphan")
    analyses = relationship("AnalysisResultDB", back_populates="transcript", cascade="all, delete-orphan")

class TranscriptSegmentDB(Base):
    __tablename__ = "transcript_segments"
    
    id = Column(String, primary_key=True, index=True)
    transcript_id = Column(String, ForeignKey("transcripts.id"))
    start_time = Column(Float)
    end_time = Column(Float)
    text = Column(Text)
    language = Column(String, default="en")
    
    transcript = relationship("TranscriptDB", back_populates="segments")

class AnalysisResultDB(Base):
    __tablename__ = "analysis_results"
    
    id = Column(String, primary_key=True, index=True)
    transcript_id = Column(String, ForeignKey("transcripts.id"))
    risk_score = Column(Float)
    severity = Column(String) # Low, Guarded, Medium, High, Critical
    analysis_status = Column(String, default="completed")
    engine_version = Column(String, default="1.0.0")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    transcript = relationship("TranscriptDB", back_populates="analyses")
    threats = relationship("DetectedThreatDB", back_populates="analysis", cascade="all, delete-orphan")
    incidents = relationship("IncidentDB", back_populates="analysis", cascade="all, delete-orphan")

class DetectedThreatDB(Base):
    __tablename__ = "detected_threats"
    
    id = Column(String, primary_key=True, index=True)
    analysis_id = Column(String, ForeignKey("analysis_results.id"))
    rule_id = Column(String)
    category = Column(String)
    matched_text = Column(Text)
    evidence_start = Column(Float, nullable=True)
    evidence_end = Column(Float, nullable=True)
    contribution = Column(Float)
    explanation = Column(Text)
    
    analysis = relationship("AnalysisResultDB", back_populates="threats")

class IncidentDB(Base):
    __tablename__ = "incidents"
    
    id = Column(String, primary_key=True, index=True)
    incident_number = Column(String, unique=True, index=True)
    analysis_id = Column(String, ForeignKey("analysis_results.id"))
    title = Column(String)
    severity = Column(String)
    status = Column(String, default="New") # New, Under Review, Confirmed Suspicious, False Positive, Resolved
    assigned_analyst = Column(String, default="SOC Analyst 1")
    analyst_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    analysis = relationship("AnalysisResultDB", back_populates="incidents")
    timeline = relationship("IncidentTimelineDB", back_populates="incident", cascade="all, delete-orphan")
    reports = relationship("ReportDB", back_populates="incident", cascade="all, delete-orphan")

class IncidentTimelineDB(Base):
    __tablename__ = "incident_timeline"
    
    id = Column(String, primary_key=True, index=True)
    incident_id = Column(String, ForeignKey("incidents.id"))
    event_type = Column(String)
    description = Column(Text)
    event_time = Column(DateTime, default=datetime.utcnow)
    
    incident = relationship("IncidentDB", back_populates="timeline")

class ReportDB(Base):
    __tablename__ = "reports"
    
    id = Column(String, primary_key=True, index=True)
    incident_id = Column(String, ForeignKey("incidents.id"))
    file_path = Column(String)
    generated_at = Column(DateTime, default=datetime.utcnow)
    
    incident = relationship("IncidentDB", back_populates="reports")

class FeedbackDB(Base):
    __tablename__ = "feedback"
    
    id = Column(String, primary_key=True, index=True)
    analysis_id = Column(String, ForeignKey("analysis_results.id"))
    feedback_type = Column(String) # accurate, false_positive, false_negative
    comments = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class SystemSettingsDB(Base):
    __tablename__ = "system_settings"
    
    key = Column(String, primary_key=True, index=True)
    value = Column(Text)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

