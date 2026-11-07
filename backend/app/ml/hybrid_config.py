"""
Configuration schemas and operational parameters for KAVACH AI Hybrid Intelligence Engine.
Governs multi-stage inference, selective escalation, and safety-first decision fusion.
"""

from enum import Enum
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class HybridMode(str, Enum):
    """Operational mode for the hybrid intelligence engine."""
    BASELINE_ONLY = "baseline_only"          # TF-IDF v3 only, never invoke MuRIL
    HYBRID_SELECTIVE = "hybrid_selective"    # Default: Invoke MuRIL selectively on uncertainty/ambiguity
    HYBRID_ALWAYS = "hybrid_always"          # Benchmark mode: Always invoke MuRIL for comparison

class DisagreementPolicy(str, Enum):
    """Strategy for handling irreconcilable disagreements between TF-IDF and MuRIL."""
    NEEDS_REVIEW = "needs_review"            # Flag for human SOC analyst review
    CONSERVATIVE_RISK = "conservative_risk"  # Escalate to higher risk class (e.g. SCAM over LEGIT)

class HybridEngineConfig(BaseModel):
    """Settings controlling selective inference thresholds and fusion behavior."""
    mode: HybridMode = Field(
        default=HybridMode.HYBRID_SELECTIVE,
        description="Operating mode of the hybrid inference engine."
    )
    escalation_confidence_threshold: float = Field(
        default=0.85,
        ge=0.0,
        le=1.0,
        description="Escalate to MuRIL if TF-IDF top confidence falls below this threshold."
    )
    escalation_margin_threshold: float = Field(
        default=0.15,
        ge=0.0,
        le=1.0,
        description="Escalate to MuRIL if margin between top 2 class probabilities is less than this."
    )
    escalate_on_ambiguous: bool = Field(
        default=True,
        description="Automatically invoke MuRIL whenever TF-IDF predicts AMBIGUOUS."
    )
    escalate_on_codemixed: bool = Field(
        default=True,
        description="Enable sensitive escalation condition for Hinglish / Tenglish code-mixed calls."
    )
    disagreement_policy: DisagreementPolicy = Field(
        default=DisagreementPolicy.NEEDS_REVIEW,
        description="Policy to apply when models disagree without clear resolution."
    )
    rule_priority_enabled: bool = Field(
        default=True,
        description="Enforce deterministic Rule-Priority Shield (critical scam rules cannot be downgraded)."
    )
    device: str = Field(
        default="cpu",
        description="Device target for transformer inference ('cuda' if available else 'cpu')."
    )

    class Config:
        frozen = False

