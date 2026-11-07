"""
KAVACH AI — Hybrid Intelligence Engine
Integrates Deterministic Rule-Priority Shield, TF-IDF v3 Fast Classifier,
Selective MuRIL v1 Deep Multilingual Classifier, and Safety-First Decision Fusion.
"""

import time
import uuid
import logging
from typing import Dict, Any, Optional, Tuple, List
from datetime import datetime, timezone

from app.ml.hybrid_config import HybridEngineConfig, HybridMode, DisagreementPolicy
from app.ml.tfidf_v3_loader import get_tfidf_v3_classifier, TFIDFV3Classifier
from app.ml.muril_classifier import get_muril_classifier, MuRILClassifier
from app.detection.engine import analyze_transcript

logger = logging.getLogger("kavach.ml.hybrid_engine")

CRITICAL_THREAT_CATEGORIES = {
    "Digital Arrest Patterns",
    "OTP / Credential Harvesting",
    "Authority Impersonation",
    "Remote Access Trojan Coercion",
    "Banking & Account Compromise",
    "Urgent Payment Coercion",
    "Sextortion / Blackmail Patterns",
    "Lottery / Prize Scam Pretexting"
}

class HybridAnalysisOutput:
    """Structured container for hybrid detection outputs and audit telemetry."""
    def __init__(
        self,
        request_id: str,
        final_decision: str,
        final_risk_score: float,
        severity: str,
        rule_score: float,
        rule_result: Dict[str, Any],
        critical_rule_triggered: bool,
        rule_shield_active: bool,
        tfidf_result: Dict[str, Any],
        muril_invoked: bool,
        muril_result: Optional[Dict[str, Any]],
        escalation_reason: Optional[str],
        model_agreement: Optional[bool],
        disagreement_details: Optional[str],
        total_latency_ms: float,
        timestamp: str
    ):
        self.request_id = request_id
        self.final_decision = final_decision
        self.final_risk_score = final_risk_score
        self.severity = severity
        self.rule_score = rule_score
        self.rule_result = rule_result
        self.critical_rule_triggered = critical_rule_triggered
        self.rule_shield_active = rule_shield_active
        self.tfidf_result = tfidf_result
        self.muril_invoked = muril_invoked
        self.muril_result = muril_result
        self.escalation_reason = escalation_reason
        self.model_agreement = model_agreement
        self.disagreement_details = disagreement_details
        self.total_latency_ms = total_latency_ms
        self.timestamp = timestamp

    def to_dict(self) -> Dict[str, Any]:
        return {
            "request_id": self.request_id,
            "final_decision": self.final_decision,
            "final_risk_score": round(self.final_risk_score, 2),
            "severity": self.severity,
            "rule_score": round(self.rule_score, 2),
            "critical_rule_triggered": self.critical_rule_triggered,
            "rule_shield_active": self.rule_shield_active,
            "tfidf_result": self.tfidf_result,
            "muril_invoked": self.muril_invoked,
            "muril_result": self.muril_result,
            "escalation_reason": self.escalation_reason,
            "model_agreement": self.model_agreement,
            "disagreement_details": self.disagreement_details,
            "total_latency_ms": round(self.total_latency_ms, 2),
            "timestamp": self.timestamp
        }

class HybridIntelligenceEngine:
    """
    Two-stage hybrid engine combining fast TF-IDF v3 with selective MuRIL v1 inference
    under the authoritative supervision of the Rule-Priority Shield.
    """
    def __init__(
        self,
        config: Optional[HybridEngineConfig] = None,
        tfidf_clf: Optional[Any] = None,
        muril_clf: Optional[Any] = None
    ):
        self.config = config or HybridEngineConfig()
        self.tfidf_clf = tfidf_clf if tfidf_clf is not None else get_tfidf_v3_classifier()
        self.muril_clf = muril_clf if muril_clf is not None else get_muril_classifier()

    def evaluate_escalation(
        self,
        tfidf_res: Dict[str, Any],
        language_hint: str
    ) -> Tuple[bool, Optional[str]]:
        """
        Evaluates whether transcript should escalate to MuRIL transformer in Stage 2.
        Based on validation-calibrated uncertainty, ambiguity, and code-mixed conditions.
        """
        mode = self.config.mode

        if mode == HybridMode.BASELINE_ONLY:
            return False, None

        if mode == HybridMode.HYBRID_ALWAYS:
            return True, "FORCED_BENCHMARK_MODE"

        # Check if MuRIL is available
        if not self.muril_clf.is_loaded:
            return False, None

        # 1. TF-IDF predicts AMBIGUOUS
        if self.config.escalate_on_ambiguous and tfidf_res.get("predicted_label") == "AMBIGUOUS":
            return True, "TFIDF_PREDICTED_AMBIGUOUS"

        # 2. Confidence below threshold
        conf = float(tfidf_res.get("confidence", 1.0))
        if conf < self.config.escalation_confidence_threshold:
            return True, f"LOW_CONFIDENCE_{conf:.2f}_BELOW_{self.config.escalation_confidence_threshold}"

        # 3. Class probability margin check
        probs = tfidf_res.get("probabilities", {})
        sorted_p = sorted(probs.values(), reverse=True)
        margin = (sorted_p[0] - sorted_p[1]) if len(sorted_p) > 1 else 1.0
        if margin < self.config.escalation_margin_threshold:
            return True, f"LOW_PROBABILITY_MARGIN_{margin:.2f}"

        # 4. Code-mixed / Indic sensitive escalation
        if self.config.escalate_on_codemixed and language_hint in ["hi-en", "te-en"] and conf < 0.90:
            return True, f"CODEMIXED_UNCERTAINTY_{language_hint}"

        return False, None

    def analyze(
        self,
        text: str,
        language_hint: str = "en",
        request_id: Optional[str] = None
    ) -> HybridAnalysisOutput:
        """
        Executes full safety-first hybrid threat analysis:
        STAGE 0: Deterministic Rule-Priority Shield
        STAGE 1: TF-IDF v3 inference (<5 ms CPU)
        STAGE 2: Selective MuRIL escalation (if indicated)
        DECISION FUSION: Safety-first resolution & audit logging
        """
        start_time = time.perf_counter()
        req_id = request_id or f"hyb-{uuid.uuid4().hex[:10]}"
        timestamp = datetime.now(timezone.utc).isoformat()

        # ======================================================================
        # STAGE 0: DETERMINISTIC RULE-PRIORITY SHIELD
        # ======================================================================
        rule_start = time.perf_counter()
        rule_res = analyze_transcript(text, language_hint=language_hint)
        rule_latency = (time.perf_counter() - rule_start) * 1000.0

        rule_score = float(rule_res.get("risk_score", 0.0))
        detected_categories = set(rule_res.get("categories", []))
        critical_categories = detected_categories & CRITICAL_THREAT_CATEGORIES
        active_coercion = bool(rule_res.get("active_coercion_detected", False))

        # A critical rule is triggered if critical categories are matched or active coercion present
        critical_rule_triggered = bool(critical_categories or active_coercion or rule_score >= 50.0)

        # ======================================================================
        # STAGE 1: TF-IDF v3 (FAST PATH)
        # ======================================================================
        t1_start = time.perf_counter()
        tfidf_pred = self.tfidf_clf.predict(text)
        tfidf_latency = (time.perf_counter() - t1_start) * 1000.0
        tfidf_pred["latency_ms"] = round(tfidf_latency, 2)

        # ======================================================================
        # STAGE 2: SELECTIVE MURIL INFERENCE (DEEP PATH)
        # ======================================================================
        should_escalate, escalation_reason = self.evaluate_escalation(tfidf_pred, language_hint)
        muril_invoked = False
        muril_pred = None

        if should_escalate and self.muril_clf.is_loaded:
            try:
                muril_invoked = True
                m_start = time.perf_counter()
                muril_pred = self.muril_clf.predict(text)
                muril_latency = (time.perf_counter() - m_start) * 1000.0
                muril_pred["latency_ms"] = round(muril_latency, 2)
            except Exception as e:
                logger.warning(f"MuRIL inference failed, falling back to TF-IDF: {e}")
                muril_invoked = False
                muril_pred = None

        # ======================================================================
        # DECISION FUSION LAYER
        # ======================================================================
        model_agreement: Optional[bool] = None
        disagreement_details: Optional[str] = None
        rule_shield_active: bool = False
        final_decision: str = "LEGITIMATE"
        final_risk: float = 0.0

        tfidf_label = tfidf_pred.get("predicted_label", "AMBIGUOUS")

        if muril_invoked and muril_pred:
            muril_label = muril_pred.get("predicted_label", "AMBIGUOUS")
            if tfidf_label == muril_label:
                model_agreement = True
                preliminary_decision = tfidf_label
            else:
                model_agreement = False
                disagreement_details = f"TF-IDF={tfidf_label} vs MuRIL={muril_label}"
                
                # Safety Principle: If either model detects SCAM, never default to LEGITIMATE
                if "SCAM" in [tfidf_label, muril_label]:
                    if self.config.disagreement_policy == DisagreementPolicy.CONSERVATIVE_RISK:
                        preliminary_decision = "SCAM"
                    else:
                        preliminary_decision = "NEEDS_REVIEW"
                elif "AMBIGUOUS" in [tfidf_label, muril_label]:
                    preliminary_decision = "AMBIGUOUS"
                else:
                    preliminary_decision = "NEEDS_REVIEW"
        else:
            preliminary_decision = tfidf_label

        # Apply Rule-Priority Shield
        if critical_rule_triggered and self.config.rule_priority_enabled:
            rule_shield_active = True
            final_decision = "SCAM"
            # Invariant: Critical rules strictly enforce a risk floor of at least 85.0
            final_risk = max(rule_score, 85.0)
            if preliminary_decision in ["LEGITIMATE", "AMBIGUOUS"]:
                cat_desc = ", ".join(critical_categories) if critical_categories else "Active Coercion"
                disagreement_details = (
                    f"Rule Shield Override: Critical rule ({cat_desc}) strictly overrode "
                    f"ML preliminary prediction '{preliminary_decision}'. Zero-downgrade enforced SCAM."
                )
        else:
            # Non-critical rule: map preliminary decision to risk score
            final_decision = preliminary_decision
            if final_decision == "SCAM":
                p_scam = tfidf_pred.get("probabilities", {}).get("SCAM", 0.8)
                if muril_pred:
                    p_scam = max(p_scam, muril_pred.get("probabilities", {}).get("SCAM", 0.8))
                final_risk = max(rule_score, p_scam * 100.0)
            elif final_decision == "NEEDS_REVIEW":
                final_risk = max(rule_score, 50.0)
            elif final_decision == "AMBIGUOUS":
                final_risk = max(rule_score, 30.0)
            else: # LEGITIMATE
                final_risk = min(rule_score, 15.0)

        # Compute severity
        final_risk = min(100.0, max(0.0, final_risk))
        if final_risk >= 75.0:
            severity = "Critical" if final_risk >= 85.0 else "High"
        elif final_risk >= 45.0:
            severity = "Elevated"
        elif final_risk >= 20.0:
            severity = "Guarded"
        else:
            severity = "Low"

        total_latency = (time.perf_counter() - start_time) * 1000.0

        return HybridAnalysisOutput(
            request_id=req_id,
            final_decision=final_decision,
            final_risk_score=final_risk,
            severity=severity,
            rule_score=rule_score,
            rule_result=rule_res,
            critical_rule_triggered=critical_rule_triggered,
            rule_shield_active=rule_shield_active,
            tfidf_result=tfidf_pred,
            muril_invoked=muril_invoked,
            muril_result=muril_pred,
            escalation_reason=escalation_reason,
            model_agreement=model_agreement,
            disagreement_details=disagreement_details,
            total_latency_ms=total_latency,
            timestamp=timestamp
        )

_GLOBAL_ENGINE: Optional[HybridIntelligenceEngine] = None

def get_hybrid_engine(config: Optional[HybridEngineConfig] = None) -> HybridIntelligenceEngine:
    """Singleton getter for HybridIntelligenceEngine."""
    global _GLOBAL_ENGINE
    if _GLOBAL_ENGINE is None or config is not None:
        _GLOBAL_ENGINE = HybridIntelligenceEngine(config)
    return _GLOBAL_ENGINE

