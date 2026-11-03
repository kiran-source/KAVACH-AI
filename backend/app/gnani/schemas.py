from pydantic import BaseModel
from typing import List, Optional

class TranscriptSegment(BaseModel):
    start: float
    end: float
    text: str
    language: str

class TranscriptResponse(BaseModel):
    transcript_id: str
    language: str
    detected_languages: List[str]
    segments: List[TranscriptSegment]
    full_text: str
    provider: str

class WarningRequest(BaseModel):
    text: Optional[str] = None
    language: str = "en"
    threat_category: Optional[str] = None
