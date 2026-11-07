"""
Data schemas for KAVACH AI Machine Learning and Hybrid Detection Engine.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class MLPredictionResult(BaseModel):
    predicted_class: str = Field(..., description="Predicted class: LEGITIMATE, SCAM, or AMBIGUOUS")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Calibrated class confidence score")
    probabilities: Dict[str, float] = Field(default_factory=dict, description="Calibrated probabilities per class")
    model_version: str = Field(..., description="Identifier and version of the ML model")
    model_name: str = Field(..., description="Display name of the model architecture")
    uncertainty: float = Field(0.0, ge=0.0, le=1.0, description="Model uncertainty indicator")
    is_abstaining: bool = Field(False, description="Whether the classifier abstained due to high uncertainty")

class HybridAnalysisResult(BaseModel):
    detection_mode: str = Field(..., description="'HYBRID' when ML inference succeeded, 'RULE_ONLY' if fallback used")
    risk_score: float = Field(..., ge=0.0, le=100.0, description="Final combined risk score (0-100)")
    severity: str = Field(..., description="Cybersecurity severity: Low, Guarded, Medium, High, Critical")
    rule_score: float = Field(..., ge=0.0, le=100.0, description="Original score from 8-pillar rule engine")
    ml_score: Optional[float] = Field(None, ge=0.0, le=100.0, description="Continuous risk score from ML model")
    ml_result: Optional[MLPredictionResult] = Field(None, description="Detailed ML classifier output")
    threats: List[Dict[str, Any]] = Field(default_factory=list, description="Verbatim matched threat evidence")
    categories: List[str] = Field(default_factory=list, description="Flagged threat categories")
    recommendations: List[str] = Field(default_factory=list, description="Actionable safety guidance")
    context_suppressed: bool = Field(False, description="Whether threat was suppressed by negative awareness context")
    context_note: str = Field("", description="Explanation of context suppression if applicable")
    conflict_detected: bool = Field(False, description="Whether rule engine and ML model had divergent verdicts")
    conflict_explanation: Optional[str] = Field(None, description="Explanation of resolution strategy on conflict")
    explanation: str = Field(..., description="Comprehensive explainable rationale for the decision")
    engine_version: str = Field("2.0.0-hybrid", description="Version of the hybrid detection engine")

