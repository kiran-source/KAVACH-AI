"""
Hybrid Risk Fusion Engine for KAVACH AI
Combines explainable deterministic rule-based threat scoring with calibrated ML classification.
Implements Rule-Priority Shield, Conflict Detection, and Rule-Only fallback.
"""

import logging
from typing import Dict, Any, Optional

from app.detection.engine import analyze_transcript
from app.ml import classifier as ml_classifier
from app.ml.schemas import HybridAnalysisResult, MLPredictionResult

logger = logging.getLogger("kavach.ml.fusion")

def score_to_severity(score: float) -> str:
    if score >= 80.0:
        return "Critical"
    elif score >= 60.0:
        return "High"
    elif score >= 40.0:
        return "Medium"
    elif score >= 20.0:
        return "Guarded"
    return "Low"

def perform_hybrid_analysis(transcript_text: str, language_hint: str = "en") -> HybridAnalysisResult:
    """
    Executes hybrid detection pipeline:
    1. Evaluates 8-pillar explainable rule engine.
    2. Runs calibrated multilingual ML classifier (if loaded).
    3. Fuses scores using safety shields and conflict resolution.
    4. Falls back seamlessly to RULE_ONLY if ML model is unavailable.
    """
    # 1. Rule Engine Execution (Always performed)
    rule_res = analyze_transcript(transcript_text, language_hint=language_hint)
    rule_score = float(rule_res.get("risk_score", 0.0))
    threats = rule_res.get("threats", [])
    categories = rule_res.get("categories", [])
    recommendations = rule_res.get("recommendations", [])
    context_suppressed = rule_res.get("context_suppressed", False)
    context_note = rule_res.get("context_note", "")

    # 2. ML Classifier Execution
    classifier = ml_classifier.get_classifier()
    ml_result: Optional[MLPredictionResult] = None
    
    if classifier.is_loaded:
        ml_result = classifier.predict(transcript_text)

    # 3. Decision Strategy: Fallback to RULE_ONLY if ML unavailable or abstaining
    has_active_coercion = bool(rule_res.get("active_coercion_detected", False))
    adversarial_disclaimer = bool(rule_res.get("adversarial_disclaimer_detected", False))
    
    if ml_result is None or ml_result.is_abstaining:
        abstain_reason = "ML model abstained due to high uncertainty/low margin." if (ml_result and ml_result.is_abstaining) else "ML model not available."
        logger.info(f"Executing in RULE_ONLY mode: {abstain_reason}")
        
        final_risk_score = rule_score
        conflict_detected = False
        conflict_explanation = None
        
        # Enforce safety shield override if adversarial disclaimer was detected
        if adversarial_disclaimer or (has_active_coercion and context_suppressed):
            final_risk_score = max(rule_score, 65.0)
            conflict_detected = True
            conflict_explanation = (
                "Safety Shield Override: Deceptive Context Detected. Caller uttered generic security/awareness "
                "phrases but dialogue contains active critical threats (e.g. OTP demand, remote access, coercive extortion, or digital arrest). "
                "Educational suppression overruled to protect against social engineering."
            )
            
        severity = score_to_severity(final_risk_score)
        explanation = f"Evaluated via 8-pillar deterministic threat rules ({abstain_reason})"
        if conflict_detected and conflict_explanation:
            explanation += f" Note: {conflict_explanation}"

        return HybridAnalysisResult(
            detection_mode="RULE_ONLY",
            risk_score=final_risk_score,
            severity=severity,
            rule_score=rule_score,
            ml_score=None,
            ml_result=ml_result,
            threats=threats,
            categories=categories,
            recommendations=recommendations,
            context_suppressed=context_suppressed,
            context_note=context_note,
            conflict_detected=conflict_detected,
            conflict_explanation=conflict_explanation,
            explanation=explanation,
            engine_version="1.0.0-rule_only"
        )

    # 4. Map ML Prediction to continuous scale [0, 100]
    p_class = ml_result.predicted_class
    conf = ml_result.confidence
    
    if p_class == "SCAM":
        # Scam confidence maps to 50 - 100
        ml_score = 50.0 + (50.0 * conf)
    elif p_class == "AMBIGUOUS":
        # Ambiguous confidence maps to 25 - 50
        ml_score = 25.0 + (25.0 * conf)
    else:  # LEGITIMATE
        # Legitimate confidence maps to 0 - 25
        ml_score = 25.0 * (1.0 - conf)
        
    ml_score = round(max(0.0, min(100.0, ml_score)), 2)

    # 5. Hybrid Fusion with Rule-Priority Shield and Safety Precedence
    conflict_detected = False
    conflict_explanation = None
    
    has_critical_categories = any(c in ["Credential Theft", "Digital Arrest Patterns", "Remote Access Manipulation", "Financial Fraud"] for c in categories)
    is_critical_rule = bool(rule_score >= 50.0 or has_critical_categories or has_active_coercion)

    # Precedence 1: Adversarial Disclaimer / Deceptive Context Override
    # Generic educational phrases must NOT override direct critical threat evidence (OTP extraction, coercive transfer, remote access, digital arrest)
    if adversarial_disclaimer or (has_active_coercion and context_suppressed):
        conflict_detected = True
        conflict_explanation = (
            "Safety Shield Override: Deceptive Context Detected. Caller uttered generic security/awareness "
            "phrases but dialogue contains active critical threats (e.g. OTP demand, remote access, coercive extortion, or digital arrest). "
            "Educational suppression overruled to protect against social engineering."
        )
        combined_score = max(rule_score, 65.0)

    # Precedence 2: Pure Educational / Security Awareness Context (No active demands or critical coercion)
    elif context_suppressed:
        combined_score = min(rule_score, 15.0)
        if p_class == "SCAM":
            conflict_detected = True
            conflict_explanation = (
                "Educational Context Shield active: Document is a genuine security advisory / awareness broadcast without active coercion. "
                "Downscaled statistical ML scam prediction to prevent false alarm on educational material."
            )
        else:
            conflict_explanation = "Negative awareness context confirmed: genuine advisory without coercive demands."

    # Precedence 3: Critical Rule-Priority Shield (Never downgrade deterministic critical threat patterns)
    # Critical threat patterns must NOT be downgraded merely because the statistical model predicts LEGITIMATE or AMBIGUOUS.
    elif is_critical_rule and p_class in ["LEGITIMATE", "AMBIGUOUS"]:
        conflict_detected = True
        conflict_explanation = (
            f"Rule-Priority Shield active: Deterministic rules flagged critical scam indicators (score: {rule_score:.1f}/100), "
            f"while statistical model predicted '{p_class}'. Preserving rule-priority score to prevent false negatives."
        )
        combined_score = max(rule_score, (0.75 * rule_score) + (0.25 * ml_score))

    elif is_critical_rule and p_class == "SCAM":
        # Both rules and ML model identify scam patterns; ensure score never falls below deterministic rule score
        combined_score = max(rule_score, (0.55 * rule_score) + (0.45 * ml_score))

    # Precedence 4: Novel ML Scam Linguistic Detection (Rules quiet, ML highly confident)
    elif rule_score < 25.0 and p_class == "SCAM" and conf >= 0.70:
        conflict_detected = True
        conflict_explanation = (
            "Divergence detected: Multilingual model identified strong scam linguistic patterns without triggering "
            "specific regex rules. Elevating to Guarded status for SOC investigation."
        )
        combined_score = (0.35 * rule_score) + (0.65 * ml_score)

    else:
        # Precedence 5: Standard balanced fusion
        combined_score = (0.55 * rule_score) + (0.45 * ml_score)

    combined_score = round(max(0.0, min(100.0, combined_score)), 1)
    severity = score_to_severity(combined_score)

    explanation = (
        f"Hybrid Decision: Rule engine evaluated {len(threats)} threat pattern(s) (score: {rule_score:.1f}/100). "
        f"Multilingual model predicted '{p_class}' with {conf*100:.1f}% confidence (ML score: {ml_score:.1f}/100). "
        f"Fused risk score: {combined_score:.1f}/100 ({severity})."
    )
    if conflict_detected and conflict_explanation:
        explanation += f" Note: {conflict_explanation}"

    return HybridAnalysisResult(
        detection_mode="HYBRID",
        risk_score=combined_score,
        severity=severity,
        rule_score=rule_score,
        ml_score=ml_score,
        ml_result=ml_result,
        threats=threats,
        categories=categories,
        recommendations=recommendations,
        context_suppressed=context_suppressed,
        context_note=context_note,
        conflict_detected=conflict_detected,
        conflict_explanation=conflict_explanation,
        explanation=explanation,
        engine_version="2.0.0-hybrid"
    )
