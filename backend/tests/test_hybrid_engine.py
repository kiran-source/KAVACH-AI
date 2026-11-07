"""
Unit & Integration Regression Tests for KAVACH AI Hybrid Intelligence Engine.
Validates TF-IDF v3, MuRIL v1, Selective Escalation, Safety Fusion, API Endpoints, and Production Isolation.
"""

import pytest
import numpy as np
from pathlib import Path

from app.main import analyze_with_hybrid_engine, HybridAnalysisRequest
from app.ml.hybrid_config import HybridEngineConfig, HybridMode, DisagreementPolicy
from app.ml.hybrid_engine import HybridIntelligenceEngine, get_hybrid_engine
from app.ml.tfidf_v3_loader import get_tfidf_v3_classifier, is_tfidf_v3_available
from app.ml.muril_classifier import get_muril_classifier
from app.ml.muril_loader import is_muril_available, get_device
from app.ml.classifier import get_classifier as get_prod_v1_classifier


# 1. TF-IDF v3 Model Loading
def test_tfidf_v3_model_loading():
    assert is_tfidf_v3_available() is True
    clf = get_tfidf_v3_classifier()
    assert clf.is_loaded is True
    meta = clf.model_metadata()
    assert meta["model_name"] == "tfidf_v3"
    assert meta["status"] == "LOADED"

# 2. MuRIL Model Loading from Extracted ZIP
def test_muril_model_loading():
    assert is_muril_available() is True
    clf = get_muril_classifier()
    assert clf.is_loaded is True
    meta = clf.model_metadata()
    assert meta["model_name"] == "muril_v1"
    assert meta["base_checkpoint"] == "google/muril-base-cased"
    assert meta["num_parameters"] == 237558531

# 3. Both Models Producing Valid Three-Class Predictions
def test_both_models_three_class_predictions():
    tfidf = get_tfidf_v3_classifier()
    muril = get_muril_classifier()
    sample = "This is a call from Mumbai police cyber cell regarding illegal transfer."

    res_tf = tfidf.predict(sample)
    assert res_tf["predicted_label"] in ["LEGITIMATE", "AMBIGUOUS", "SCAM"]
    assert len(res_tf["probabilities"]) == 3
    assert set(res_tf["probabilities"].keys()) == {"LEGITIMATE", "AMBIGUOUS", "SCAM"}

    res_m = muril.predict(sample)
    assert res_m["predicted_label"] in ["LEGITIMATE", "AMBIGUOUS", "SCAM"]
    assert len(res_m["probabilities"]) == 3
    assert set(res_m["probabilities"].keys()) == {"LEGITIMATE", "AMBIGUOUS", "SCAM"}

# 4. Probability Validation
def test_probability_distribution_bounds():
    tfidf = get_tfidf_v3_classifier()
    muril = get_muril_classifier()
    sample = "Routine customer verification procedure."

    probs_tf = tfidf.predict_proba(sample)
    for p in probs_tf.values():
        assert 0.0 <= p <= 1.0
    assert abs(sum(probs_tf.values()) - 1.0) < 1e-3

    probs_m = muril.predict_proba(sample)
    for p in probs_m.values():
        assert 0.0 <= p <= 1.0
    assert abs(sum(probs_m.values()) - 1.0) < 1e-3

# 5. CPU-Only Inference Readiness
def test_cpu_inference_support():
    muril = get_muril_classifier()
    device = get_device()
    assert device in ["cpu", "cuda"]
    sample_text = "CPU smoke test verification."
    res = muril.predict(sample_text)
    assert res["predicted_label"] in ["LEGITIMATE", "AMBIGUOUS", "SCAM"]

# 6. CUDA / Device Check
def test_device_fallback_or_cuda():
    import torch
    expected_device = "cuda" if torch.cuda.is_available() else "cpu"
    assert get_device() == expected_device

# 7. Missing MuRIL Model Behavior
def test_missing_muril_graceful_handling():
    class DummyMissingMuRIL:
        is_loaded = False
        def predict(self, text):
            return {"predicted_label": "AMBIGUOUS", "probabilities": {"LEGITIMATE": 0.33, "AMBIGUOUS": 0.34, "SCAM": 0.33}, "confidence": 0.34, "model_name": "muril_v1"}

    engine = HybridIntelligenceEngine(muril_clf=DummyMissingMuRIL())
    out = engine.analyze("Testing missing muril fallback", "en")
    assert out.final_decision in ["LEGITIMATE", "AMBIGUOUS", "SCAM"]
    assert out.muril_invoked is False

# 8. MuRIL Inference Failure Fallback
def test_muril_inference_exception_fallback():
    class DummyFailingMuRIL:
        is_loaded = True
        def predict(self, text):
            raise RuntimeError("Simulated forward pass failure")

    engine = HybridIntelligenceEngine(muril_clf=DummyFailingMuRIL())
    # Should not crash the process
    try:
        out = engine.analyze("Simulated failure call", "en")
        assert out.final_decision is not None
    except Exception:
        pytest.fail("Hybrid engine did not handle model failure safely")

# 9. TF-IDF Only Mode
def test_baseline_only_mode():
    cfg = HybridEngineConfig(mode=HybridMode.BASELINE_ONLY)
    engine = HybridIntelligenceEngine(config=cfg)
    out = engine.analyze("Hello, this is a routine banking balance update.", "en")
    assert out.muril_invoked is False
    assert out.escalation_reason is None

# 10. Selective Escalation Mode
def test_selective_escalation_on_ambiguous():
    cfg = HybridEngineConfig(mode=HybridMode.HYBRID_SELECTIVE, escalate_on_ambiguous=True)
    engine = HybridIntelligenceEngine(config=cfg)
    
    # Text crafted to cause uncertainty/ambiguity
    ambig_text = "Your account has unusual activity. We may request your verification details later."
    out = engine.analyze(ambig_text, "en")
    # If TF-IDF confidence is below threshold or AMBIGUOUS, it escalates
    if out.tfidf_result["predicted_label"] == "AMBIGUOUS" or out.tfidf_result["confidence"] < 0.85:
        assert out.muril_invoked is True
        assert out.escalation_reason is not None

# 11. Model Agreement Handling
def test_model_agreement_fusion():
    class MockTF:
        is_loaded = True
        def predict(self, text):
            return {"predicted_label": "SCAM", "probabilities": {"LEGITIMATE": 0.05, "AMBIGUOUS": 0.10, "SCAM": 0.85}, "confidence": 0.85, "model_name": "tfidf_v3"}
    class MockMuril:
        is_loaded = True
        def predict(self, text):
            return {"predicted_label": "SCAM", "probabilities": {"LEGITIMATE": 0.02, "AMBIGUOUS": 0.08, "SCAM": 0.90}, "confidence": 0.90, "model_name": "muril_v1"}

    cfg = HybridEngineConfig(mode=HybridMode.HYBRID_ALWAYS)
    engine = HybridIntelligenceEngine(config=cfg, tfidf_clf=MockTF(), muril_clf=MockMuril())
    out = engine.analyze("Agreement test call", "en")
    assert out.model_agreement is True
    assert out.final_decision == "SCAM"
    assert out.final_risk_score >= 80.0

# 12. Model Disagreement Handling
def test_model_disagreement_conservative_safety():
    # TF-IDF predicts LEGITIMATE, but MuRIL detects SCAM
    class MockTF:
        is_loaded = True
        def predict(self, text):
            return {"predicted_label": "LEGITIMATE", "probabilities": {"LEGITIMATE": 0.60, "AMBIGUOUS": 0.20, "SCAM": 0.20}, "confidence": 0.60, "model_name": "tfidf_v3"}
    class MockMuril:
        is_loaded = True
        def predict(self, text):
            return {"predicted_label": "SCAM", "probabilities": {"LEGITIMATE": 0.10, "AMBIGUOUS": 0.10, "SCAM": 0.80}, "confidence": 0.80, "model_name": "muril_v1"}

    cfg = HybridEngineConfig(mode=HybridMode.HYBRID_ALWAYS, disagreement_policy=DisagreementPolicy.NEEDS_REVIEW)
    engine = HybridIntelligenceEngine(config=cfg, tfidf_clf=MockTF(), muril_clf=MockMuril())
    out = engine.analyze("Conflict test call", "en")
    assert out.model_agreement is False
    # Crucial safety rule: Never classify as LEGITIMATE when a model flags SCAM
    assert out.final_decision in ["NEEDS_REVIEW", "SCAM"]
    assert out.final_decision != "LEGITIMATE"

# 13. Critical Rule-Priority Enforcement
def test_critical_rule_priority_enforcement():
    engine = HybridIntelligenceEngine()
    critical_text = (
        "I am Inspector Raman from CBI. You are under digital arrest right now. "
        "Do not disconnect this call. Pay the 50,000 fine to clear your Aadhaar."
    )
    out = engine.analyze(critical_text, "en")
    assert out.critical_rule_triggered is True
    assert out.rule_shield_active is True
    assert out.final_decision == "SCAM"
    assert out.severity == "Critical"
    assert out.final_risk_score >= 85.0

# 14. Critical Scam Cannot Be Downgraded by ML
def test_critical_scam_cannot_be_downgraded_by_ml_legitimate():
    # Adversarial mock: Both ML models predict LEGITIMATE on an obvious digital arrest call
    class MockTF:
        is_loaded = True
        def predict(self, text):
            return {"predicted_label": "LEGITIMATE", "probabilities": {"LEGITIMATE": 0.95, "AMBIGUOUS": 0.03, "SCAM": 0.02}, "confidence": 0.95, "model_name": "tfidf_v3"}
    class MockMuril:
        is_loaded = True
        def predict(self, text):
            return {"predicted_label": "LEGITIMATE", "probabilities": {"LEGITIMATE": 0.98, "AMBIGUOUS": 0.01, "SCAM": 0.01}, "confidence": 0.98, "model_name": "muril_v1"}

    engine = HybridIntelligenceEngine(tfidf_clf=MockTF(), muril_clf=MockMuril())
    critical_text = "This is CBI officer. You are placed under digital arrest right now. Transfer money immediately."
    out = engine.analyze(critical_text, "en")
    # Rule-Priority Shield MUST intercept and force SCAM
    assert out.rule_shield_active is True
    assert out.final_decision == "SCAM"
    assert out.final_risk_score >= 85.0
    assert out.severity == "Critical"

# 15. Empty Transcript Handling
def test_empty_transcript_handling():
    engine = HybridIntelligenceEngine()
    for empty_val in ["", "   ", "\n\t"]:
        out = engine.analyze(empty_val, "en")
        assert out.final_decision in ["LEGITIMATE", "AMBIGUOUS"]
        assert out.final_risk_score <= 30.0

# 16. Multilingual Input (English, Hindi, Telugu)
def test_multilingual_inputs():
    engine = HybridIntelligenceEngine()
    inputs = {
        "en": "Hello, this is a routine banking service call.",
        "hi": "नमस्ते, यह आपके बैंक खाते के बारे में सामान्य सूचना है।",
        "te": "నమస్కారం, ఇది మీ బ్యాంక్ ఖాతా గురించిన సాధారణ సమాచారం."
    }
    for lang, text in inputs.items():
        out = engine.analyze(text, lang)
        assert out.final_decision in ["LEGITIMATE", "AMBIGUOUS", "SCAM"]
        assert 0.0 <= out.final_risk_score <= 100.0

# 17. Code-Mixed Input (Hinglish, Tenglish)
def test_codemixed_inputs():
    engine = HybridIntelligenceEngine()
    inputs = {
        "hi-en": "Hello sir, aapke account mein suspicious activity detect hui hai, please verify karein.",
        "te-en": "Sir, mee account lo unusual transaction jarigindi, urgent ga details ivvandi."
    }
    for lang, text in inputs.items():
        out = engine.analyze(text, lang)
        assert out.final_decision in ["LEGITIMATE", "AMBIGUOUS", "SCAM", "NEEDS_REVIEW"]

# 18. API Endpoint Validation (POST /api/v1/hybrid/analyze)
def test_hybrid_api_endpoint():
    # Valid Request
    req = HybridAnalysisRequest(
        text="Digital arrest scam transfer money immediately.",
        language="en",
        mode="hybrid_selective"
    )
    data = analyze_with_hybrid_engine(req)
    assert data["status"] == "SUCCESS"
    assert data["final_decision"] == "SCAM"
    assert data["rule_shield_active"] is True
    assert data["critical_rule_triggered"] is True
    assert data["final_risk_score"] >= 85.0
    assert data["severity"] == "Critical"
    assert "tfidf_result" in data

    # Empty payload check
    req_empty = HybridAnalysisRequest(text="")
    data_empty = analyze_with_hybrid_engine(req_empty)
    assert data_empty["status"] == "EMPTY_INPUT"

# 19. Production Baseline v1 Isolation & Non-Regression
def test_production_baseline_v1_untouched():
    prod_clf = get_prod_v1_classifier()
    assert prod_clf.is_loaded is True
    # Production classifier metadata points to v1.0
    meta = prod_clf.metadata
    assert "v1.0" in meta.get("model_name", "")
    assert "v2" in meta.get("training_dataset", "")

