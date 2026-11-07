"""
Unit and Integration Regression Tests for KAVACH AI Machine Learning & Hybrid Risk Engine.

Specifically tests the 7 required critical safety & precedence regression cases:
1. Critical rule + ML LEGITIMATE (Rule-Priority Shield must not downgrade).
2. Critical rule + ML AMBIGUOUS (Rule-Priority Shield must not downgrade).
3. Critical rule + ML SCAM (Full agreement, preserves high/critical risk).
4. Educational discussion without active malicious demand (Educational Context Shield active).
5. Educational discussion combined with an active malicious demand (Safety Shield Override overrules suppression).
6. Adversarial disclaimer combined with an OTP harvesting request (Adversarial disclaimer detected, high/critical risk).
7. Legitimate customer-service conversation discussing OTP without requesting disclosure (Low/Guarded risk).

Plus auxiliary tests for model loading, bounds, low-confidence, abstention, and code-mixed inputs.
"""

import pytest
from app.ml import (
    load_ml_artifacts,
    is_model_available,
    get_classifier,
    perform_hybrid_analysis,
    HybridAnalysisResult,
    MLPredictionResult
)
from app.ml import classifier as ml_classifier

# ==============================================================================
# 7 REQUIRED SAFETY & PRECEDENCE REGRESSION TESTS
# ==============================================================================

# --- Regression Case 1: Critical rule + ML LEGITIMATE ---
def test_critical_rule_with_ml_predicting_legitimate(monkeypatch):
    """
    When deterministic rules detect high-consequence threats (Digital Arrest, CBI, OTP theft),
    an ML prediction of LEGITIMATE must NOT downgrade the risk score.
    The Rule-Priority Shield must preserve the rule score and flag a conflict.
    """
    mock_ml_res = MLPredictionResult(
        predicted_class="LEGITIMATE",
        confidence=0.94,
        probabilities={"LEGITIMATE": 0.94, "AMBIGUOUS": 0.04, "SCAM": 0.02},
        model_version="v1.0",
        model_name="TF-IDF + Calibrated Logistic Regression",
        uncertainty=0.10,
        is_abstaining=False
    )
    class MockClf:
        is_loaded = True
        def predict(self, text):
            return mock_ml_res
            
    monkeypatch.setattr(ml_classifier, "get_classifier", lambda: MockClf())
    
    critical_text = (
        "I am Inspector Sharma from CBI headquarters. You are placed under digital arrest right now. "
        "Do not disconnect the video call. Tell me your 6 digit OTP immediately."
    )
    res = perform_hybrid_analysis(critical_text, "en")
    
    assert res.detection_mode == "HYBRID"
    assert res.conflict_detected is True
    assert "Rule-Priority Shield active" in (res.conflict_explanation or "")
    assert res.rule_score >= 50.0
    # Must preserve the rule score (never downgraded below rule_score)
    assert res.risk_score >= res.rule_score
    assert res.risk_score >= 60.0
    assert res.severity in ["High", "Critical"]
    assert "Digital Arrest Patterns" in res.categories

# --- Regression Case 2: Critical rule + ML AMBIGUOUS ---
def test_critical_rule_with_ml_predicting_ambiguous(monkeypatch):
    """
    When deterministic rules detect high-consequence threats,
    an ML prediction of AMBIGUOUS must NOT downgrade the risk score.
    The Rule-Priority Shield must protect against downgrades from AMBIGUOUS predictions.
    """
    mock_ml_res = MLPredictionResult(
        predicted_class="AMBIGUOUS",
        confidence=0.65,
        probabilities={"LEGITIMATE": 0.20, "AMBIGUOUS": 0.65, "SCAM": 0.15},
        model_version="v1.0",
        model_name="TF-IDF + Calibrated Logistic Regression",
        uncertainty=0.50,
        is_abstaining=False
    )
    class MockClf:
        is_loaded = True
        def predict(self, text):
            return mock_ml_res
            
    monkeypatch.setattr(ml_classifier, "get_classifier", lambda: MockClf())
    
    critical_text = (
        "Notice from Mumbai Police Cyber Cell. A warrant is issued against your name. "
        "Download AnyDesk immediately, keep camera on, and transfer forty-five thousand rupees to the safe account."
    )
    res = perform_hybrid_analysis(critical_text, "en")
    
    assert res.detection_mode == "HYBRID"
    assert res.conflict_detected is True
    assert "Rule-Priority Shield active" in (res.conflict_explanation or "")
    assert res.rule_score >= 50.0
    # Must not be downgraded by the AMBIGUOUS prediction
    assert res.risk_score >= res.rule_score
    assert res.risk_score >= 60.0
    assert res.severity in ["High", "Critical"]

# --- Regression Case 3: Critical rule + ML SCAM ---
def test_critical_rule_with_ml_predicting_scam(monkeypatch):
    """
    When both deterministic rules and ML model identify high-risk scam patterns,
    they reinforce each other; score must remain high/critical and >= rule_score.
    """
    mock_ml_res = MLPredictionResult(
        predicted_class="SCAM",
        confidence=0.96,
        probabilities={"LEGITIMATE": 0.01, "AMBIGUOUS": 0.03, "SCAM": 0.96},
        model_version="v1.0",
        model_name="TF-IDF + Calibrated Logistic Regression",
        uncertainty=0.06,
        is_abstaining=False
    )
    class MockClf:
        is_loaded = True
        def predict(self, text):
            return mock_ml_res
            
    monkeypatch.setattr(ml_classifier, "get_classifier", lambda: MockClf())
    
    critical_text = (
        "This is Deputy Superintendent Raman from CBI New Delhi. A non-bailable arrest warrant has been sanctioned under your Aadhaar. "
        "You are under immediate Digital Arrest. Do not disconnect this video call or contact your family. "
        "Transfer eighty-five thousand rupees to the RBI verified clearance account right now."
    )
    res = perform_hybrid_analysis(critical_text, "en")
    
    assert res.detection_mode == "HYBRID"
    assert res.risk_score >= res.rule_score
    assert res.risk_score >= 70.0
    assert res.severity in ["High", "Critical"]
    assert res.ml_result.predicted_class == "SCAM"

# --- Regression Case 4: Educational discussion without active malicious demand ---
def test_educational_discussion_without_active_malicious_demand(monkeypatch):
    """
    Educational advisories mention scary words (CBI, police, digital arrest, OTP, password).
    Even if ML predicts SCAM with high confidence due to these words, educational context
    precedence MUST downscale the threat and prevent high-severity alarms as long as no
    active coercion / extraction commands exist.
    """
    mock_ml_res = MLPredictionResult(
        predicted_class="SCAM",
        confidence=0.95,
        probabilities={"LEGITIMATE": 0.02, "AMBIGUOUS": 0.03, "SCAM": 0.95},
        model_version="v1.0",
        model_name="TF-IDF + Calibrated Logistic",
        uncertainty=0.08,
        is_abstaining=False
    )
    class MockClf:
        is_loaded = True
        def predict(self, text):
            return mock_ml_res
            
    monkeypatch.setattr(ml_classifier, "get_classifier", lambda: MockClf())
    
    advisory_text = (
        "RBI public awareness warning: Beware of fraudulent callers posing as CBI police officers demanding OTP "
        "or claiming you are under digital arrest. Bank never asks for your OTP or password. Stay safe from scam calls."
    )
    res = perform_hybrid_analysis(advisory_text, "en")
    
    assert res.context_suppressed is True
    assert res.conflict_detected is True
    assert "Educational Context Shield" in (res.conflict_explanation or "")
    assert res.risk_score <= 25.0
    assert res.severity in ["Low", "Guarded"]

# --- Regression Case 5: Educational discussion combined with an active malicious demand ---
def test_educational_discussion_combined_with_active_malicious_demand():
    """
    Adversarial scammer uses 'cyber safety tip' then demands 'transfer money to RBI safe account'.
    Safety shield MUST overrule educational suppression and preserve High/Critical risk.
    """
    adversarial_payment_text = (
        "This is an official cyber safety notice from police cyber crime branch. Beware of fraudulent calls. "
        "Your account is implicated in financial fraud. To avoid arrest warrant, transfer forty-five thousand "
        "rupees to the RBI verified clearance account right now."
    )
    res = perform_hybrid_analysis(adversarial_payment_text, "en")
    
    assert res.risk_score >= 65.0
    assert res.severity in ["High", "Critical"]
    assert res.conflict_detected is True
    assert "Safety Shield Override" in (res.conflict_explanation or "")

# --- Regression Case 6: Adversarial disclaimer combined with an OTP harvesting request ---
def test_adversarial_disclaimer_combined_with_otp_harvesting():
    """
    An adversarial attacker utters 'bank never asks for OTP' to sound legitimate,
    but then immediately demands: 'Now tell me your 6 digit OTP to verify your card'.
    The safety shield MUST NOT suppress this! It must flag adversarial disclaimer and retain Critical/High risk.
    """
    adversarial_text = (
        "Bank security awareness reminder: Please be aware of fraud. Bank never asks for your password. "
        "However, your card is currently suspended. To unblock it, tell me your 6 digit OTP immediately."
    )
    res = perform_hybrid_analysis(adversarial_text, "en")
    
    assert res.risk_score >= 60.0
    assert res.severity in ["High", "Critical"]
    assert res.conflict_detected is True
    assert "Safety Shield Override" in (res.conflict_explanation or "")
    assert "Credential Theft" in res.categories

# --- Regression Case 7: Legitimate customer-service conversation discussing OTP without requesting disclosure ---
def test_legitimate_customer_service_discussing_otp_without_requesting_disclosure():
    """
    Customer calls bank about an OTP they received:
    'I got an OTP message on my phone. Did someone try to login? Bank: Your account is safe, never share it.'
    Must NOT trigger false positive!
    """
    text = (
        "Good afternoon, I am an account holder with HDFC Bank. I just received an unexpected OTP SMS on my mobile. "
        "I am calling to check if my account is safe. Branch officer: Yes sir, your account is completely secure. "
        "As a rule, please never share your one time password with anyone."
    )
    res = perform_hybrid_analysis(text, "en")
    
    # Must be Low risk (no active extortion, no commands to victim)
    assert res.risk_score <= 35.0
    assert res.severity in ["Low", "Guarded"]

# ==============================================================================
# AUXILIARY SYSTEM & INTEGRATION TESTS
# ==============================================================================

def test_genuine_bank_security_awareness_announcement():
    text = (
        "This is an automated public awareness message from State Bank of India. "
        "Bank never asks for your password, PIN, or OTP. Beware of fraudulent calls. "
        "Stay safe and keep your banking credentials confidential."
    )
    res = perform_hybrid_analysis(text, "en")
    assert res.context_suppressed is True
    assert res.risk_score <= 20.0
    assert res.severity in ["Low", "Guarded"]

def test_digital_arrest_mixed_with_fake_security_disclaimer():
    text = (
        "Stay safe from scam calls. This is Inspector Sharma from CBI special wing. "
        "You are under immediate digital arrest. Do not disconnect the video call or police will come to your house."
    )
    res = perform_hybrid_analysis(text, "en")
    assert res.risk_score >= 65.0
    assert res.severity in ["High", "Critical"]
    assert "Digital Arrest Patterns" in res.categories
    assert res.conflict_detected is True

def test_critical_threats_with_legitimate_looking_introduction():
    text = (
        "Good morning, this is Priya from HDFC Bank customer relations, MG Road branch. "
        "We noticed a security issue on your device. Please open Play Store, download AnyDesk immediately, "
        "and share the 9 digit code on your screen so our engineer can fix it."
    )
    res = perform_hybrid_analysis(text, "en")
    assert res.risk_score >= 55.0
    assert res.severity in ["High", "Critical", "Medium"]
    assert "Remote Access Manipulation" in res.categories

def test_low_confidence_prediction(monkeypatch):
    mock_ml_res = MLPredictionResult(
        predicted_class="AMBIGUOUS",
        confidence=0.48,
        probabilities={"LEGITIMATE": 0.28, "AMBIGUOUS": 0.48, "SCAM": 0.24},
        model_version="v1.0",
        model_name="TF-IDF + Calibrated Logistic",
        uncertainty=0.80,
        is_abstaining=False
    )
    class MockClf:
        is_loaded = True
        def predict(self, text):
            return mock_ml_res
            
    monkeypatch.setattr(ml_classifier, "get_classifier", lambda: MockClf())
    
    vague_text = "Hello, calling from customer relations regarding some updates."
    res = perform_hybrid_analysis(vague_text, "en")
    assert res.detection_mode == "HYBRID"
    assert res.ml_result.confidence == 0.48
    assert 0.0 <= res.risk_score <= 100.0

def test_abstaining_prediction_fallback_to_rule_only(monkeypatch):
    mock_ml_res = MLPredictionResult(
        predicted_class="AMBIGUOUS",
        confidence=0.38,
        probabilities={"LEGITIMATE": 0.33, "AMBIGUOUS": 0.38, "SCAM": 0.29},
        model_version="v1.0",
        model_name="TF-IDF + Calibrated Logistic",
        uncertainty=0.95,
        is_abstaining=True
    )
    class MockClf:
        is_loaded = True
        def predict(self, text):
            return mock_ml_res
            
    monkeypatch.setattr(ml_classifier, "get_classifier", lambda: MockClf())
    
    text = "Vague call with poor acoustic reception."
    res = perform_hybrid_analysis(text, "en")
    assert res.detection_mode == "RULE_ONLY"
    assert res.ml_score is None
    assert "abstained" in res.explanation.lower()

def test_model_unavailable_fallback_rule_only(monkeypatch):
    class MockUnloadedClf:
        is_loaded = False
        def predict(self, text):
            return None
            
    monkeypatch.setattr(ml_classifier, "get_classifier", lambda: MockUnloadedClf())
    
    text = "Sir please tell me your 6 digit OTP immediately or account blocked."
    res = perform_hybrid_analysis(text, "en")
    assert res.detection_mode == "RULE_ONLY"
    assert res.ml_result is None
    assert res.rule_score >= 30.0

def test_multilingual_code_mixed_hybrid_inference():
    hi_en_text = (
        "Electricity Board vigilance desk se alert. Unpaid bill update na hone ki wajah se tonight 8:30 PM "
        "power connection cut ho jayega. Normal app mat use karo, hamare quick link par jakar netbanking password verify karo."
    )
    res_hi_en = perform_hybrid_analysis(hi_en_text, "hi-en")
    assert res_hi_en.detection_mode == "HYBRID"
    assert res_hi_en.risk_score >= 40.0

    te_en_text = (
        "SBI Card division nunchi Rajesh matladuthunnanu andi. Mee debit card tonight 12 AM ki complete ga block avthundi. "
        "Mee registered number ki 6 digit reactivation OTP vachindi, ventane cheppandi verify chesthanu."
    )
    res_te_en = perform_hybrid_analysis(te_en_text, "te-en")
    assert res_te_en.detection_mode == "HYBRID"
    assert res_te_en.risk_score >= 45.0

def test_model_loading_and_metadata():
    model, vectorizer, metadata, labels = load_ml_artifacts()
    assert model is not None
    assert vectorizer is not None
    assert metadata is not None
    assert metadata.get("vocabulary_size") > 0
    assert "label2id" in labels

def test_hybrid_score_bounds_and_severity():
    for text in [
        "Normal benign conversation with family.",
        "URGENT: Police arrest warrant issued! Transfer money immediately to avoid jail!",
        "Vague call from unknown number."
    ]:
        res = perform_hybrid_analysis(text)
        assert 0.0 <= res.risk_score <= 100.0
        assert res.severity in ["Low", "Guarded", "Medium", "High", "Critical"]
