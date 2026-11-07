# KAVACH AI — Validation-Based Threshold Calibration Report

## 1. Objective and Methodology

The selective escalation mechanism in the KAVACH AI Hybrid Intelligence Engine hinges upon identifying exactly when the fast-path Stage 1 classifier (TF-IDF v3) is sufficiently certain of its decision, versus when an utterance requires escalation to the compute-intensive Stage 2 transformer (Google MuRIL v1).

Tuning this escalation boundary directly on the test partition would constitute methodological data snooping. Therefore, all threshold grid searches and calibration experiments were performed strictly on the **held-out validation partition**:
- **Calibration Split**: `data/kavach_synthetic_v3/splits/validation.jsonl`
- **Total Calibration Samples**: **450 records** (135 LEGITIMATE, 135 AMBIGUOUS, 180 SCAM)
- **Language Balance**: 90 English, 90 Hindi, 90 Telugu, 90 Hinglish, 90 Tenglish
- **Objective Function**: Minimize transformer invocation rate while strictly preserving 100% macro F1 and zero SCAM false negatives ($FN_{\text{scam}} = 0$).

---

## 2. Threshold Grid Search Results

In Stage 1, predictions are evaluated with confidence defined as $C_{\text{tfidf}} = \max_{k} P(y_k \mid x)$. If the predicted label is `AMBIGUOUS` or $C_{\text{tfidf}} < \tau$, the call is escalated to MuRIL.

| Confidence Threshold ($\tau$) | Escalated Calls ($N=450$) | Escalation Rate (%) | Accuracy | Macro F1 | SCAM Recall | AMBIGUOUS Recall | SCAM False Negatives |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **0.60** | 136 | 30.22% | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0 |
| **0.70** | 136 | 30.22% | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0 |
| **0.75** | 136 | 30.22% | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0 |
| **0.80** | 136 | 30.22% | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0 |
| **0.85 (Chosen)** | **138** | **30.67%** | **1.0000** | **1.0000** | **1.0000** | **1.0000** | **0** |
| **0.90** | 140 | 31.11% | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0 |
| **0.95** | 149 | 33.11% | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0 |

---

## 3. Operating Point Selection & Justification

### Selected Operating Point: $\tau = 0.85$
- **Escalation Percentage**: **30.67%** on validation, **32.00%** on held-out test.
- **Fast Path Fraction**: **69.33%** of all calls are fully classified by TF-IDF v3 in $\approx 4.29\text{ ms}$, entirely bypassing transformer forward pass latency.
- **Safety Margin**: Setting $\tau = 0.85$ (rather than 0.60 or 0.70) adds a robust defensive margin against out-of-distribution noise and boundary uncertainty, ensuring that borderline high-stakes calls are routed to MuRIL without causing noticeable latency overhead on the overall call distribution.
- **Empirical Generalization**: When applied blind to the held-out test partition ($N=450$), the 0.85 threshold produced an escalation rate of **32.0%** (144/450), **100% accuracy**, and **0 false negatives**.

---

## 4. Sensitivity Analysis & Edge Case Escalation

1. **Code-Mixed Dialects (`hi-en`, `te-en`)**:
   - Analysis of TF-IDF prediction probabilities on code-mixed utterances revealed slightly wider posterior spreads than monolingual English or Hindi. The 0.85 threshold appropriately captures and escalates these subtle colloquial turns.
2. **Short Utterances**:
   - Utterances shorter than 10 words frequently produce diffused n-gram activations. The threshold safely triggers escalation or falls back to Stage 0 rule checks.
3. **Reproducibility**:
   - Precomputation timings: TF-IDF v3 cached across 450 validation samples in 0.46s; MuRIL v1 batched evaluation took 162.48s on CPU.
   - Exact configuration stored in `reports/hybrid_threshold_calibration.json`.

