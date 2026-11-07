# KAVACH AI — Hybrid Safety Architecture & Decision Fusion Validation

## 1. The Five Core Safety Principles

In high-stakes cybersecurity and anti-fraud defense, probabilistic ML models are inherently prone to false negatives when faced with adversarial perturbations, novel linguistic phrasing, or prompt evasion. KAVACH AI adheres to five non-negotiable safety principles:

### Principle 1: Rule-Priority Supremacy
Deterministic security rules representing unambiguous cyber extortion or financial theft (e.g., CBI/ED "Digital Arrest", demand for OTP/UPI PIN disclosure, immediate power disconnection extortion) take absolute precedence over statistical or transformer ML predictions.

### Principle 2: Zero Scam Downgrades
If Stage 0 triggers a critical threat category, no downstream model (neither TF-IDF nor MuRIL) is mathematically permitted to downgrade the classification to `LEGITIMATE` or lower the risk score below the critical floor ($\ge 85.0$).

### Principle 3: Conservative Disagreement Resolution
When Stage 1 and Stage 2 models disagree (e.g., TF-IDF predicts `LEGITIMATE` but MuRIL detects `SCAM`), the hybrid engine strictly defaults to the most protective security posture:
- The decision is routed to `NEEDS_REVIEW` or `SCAM`.
- The final classification is never marked as `LEGITIMATE`.
- A high-visibility alert is dispatched to the SOC analyst console with a conflict flag.

### Principle 4: Context-Aware Educational Suppression
If a user or caller is explicitly roleplaying or discussing a scam in a security awareness training seminar (e.g., *"Today we will demonstrate how scammers use fake courier calls to steal money"*), the engine suppresses spurious threat alerts while logging audit notes, avoiding alert fatigue.

### Principle 5: Graceful Degradation Under Failure
If the transformer environment experiences a catastrophic fault (out of memory, model weight absence, CUDA driver failure, or forward pass exception), the system fails safely by reverting to TF-IDF v3 and deterministic rules without crashing the backend service or returning uncaught 500 errors.

---

## 2. Empirical Safety Verification Matrix

All five safety principles were subjected to automated unit and integration tests in `backend/tests/test_hybrid_engine.py` and `backend/tests/test_ml_and_hybrid.py`:

| Test ID | Test Scenario | Input Vector | Expected Safe Behavior | Empirical Test Result |
| :---: | :--- | :--- | :--- | :---: |
| **SAFE-01** | Adversarial Digital Arrest with ML Spoofing | *"I am Inspector Raman from CBI. You are under digital arrest right now. Transfer 50,000 fine."* (Mocked ML predicting LEGITIMATE 0.98) | Rule Shield intercepts; forces `SCAM` with risk $\ge 85.0$ | **PASSED** (100% Intercept) |
| **SAFE-02** | Credential Theft with Polite Framing | *"Good morning respected customer, kindly share 6-digit OTP to complete bank KYC update."* | Intercepted by Credential Theft rule; risk score $\ge 75.0$ | **PASSED** |
| **SAFE-03** | Model Disagreement (TF=Safe, MuRIL=Scam) | Synthesized high-stakes conflict transcript | Classified as `NEEDS_REVIEW` or `SCAM`; never `LEGITIMATE` | **PASSED** |
| **SAFE-04** | Educational Awareness Suppression | *"Welcome to the cybersecurity workshop. In this session we discuss fake lottery phone scams."* | Negative context active; risk score $\le 25.0$; no false alarm | **PASSED** |
| **SAFE-05** | Transformer Runtime Crash | Simulated `RuntimeError("Forward pass failure")` | Gracefully falls back to TF-IDF fast path; service remains online | **PASSED** |
| **SAFE-06** | Missing Weights File | Simulated unextracted or missing transformer weights | Reverts cleanly to TF-IDF v3; logs `muril_invoked: false` | **PASSED** |
| **SAFE-07** | Empty & Whitespace Input | `""`, `"   "`, `"\n\t"` | Safe return of `LEGITIMATE` / `EMPTY_INPUT`; risk $\le 30.0$ | **PASSED** |

---

## 3. Threat Model Analysis: Adversarial Scam Evasion

We evaluated how the hybrid system handles the three primary adversarial tactics observed in Indian cybercrime:

1. **Evasion Strategy 1: Camouflage via Polite Small-Talk**
   - *Tactic*: Scammer spends the first 45 seconds asking polite questions about family and health before demanding OTP.
   - *Defense*: The streaming chunk buffer maintains session memory. As soon as the extortion or credential harvesting phrase appears, the Rule Shield triggers with immediate escalation.
2. **Evasion Strategy 2: Obfuscated Code-Mixing ("Hinglish" / "Tenglish")**
   - *Tactic*: Scammer alternates between English legal terms and Hindi/Telugu colloquial threats to evade keyword filters.
   - *Defense*: TF-IDF character n-grams detect root subwords, while confidence drops below 0.85, selectively triggering MuRIL. MuRIL's cross-lingual Indian vocabulary accurately disambiguates the malicious intent.
3. **Evasion Strategy 3: Fake Disclaimer Spoofing**
   - *Tactic*: Scammer opens with *"This is not a scam, this is genuine official notice from RBI"* to trick negative context detectors.
   - *Defense*: The Rule Shield enforces asymmetric priority: genuine educational markers require structural instructional discourse; explicit credential demands or arrest threats instantly override any disclaimer markers.

---

## 4. Verification Conclusion

The KAVACH AI Hybrid Intelligence Engine satisfies all safety invariants without exception. In all tested configurations and adversarial simulations, **zero scam events were downgraded**, and **zero unhandled exceptions** reached the client layer.

