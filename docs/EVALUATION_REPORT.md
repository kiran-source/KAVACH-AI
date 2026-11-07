# KAVACH AI — Benchmark Evaluation Report

## 1. Executive Summary
This report documents the empirical evaluation of KAVACH AI's detection algorithms across the remediated 500-conversation multilingual corpus (`kavach_synthetic_v2`).

The evaluation compares:
1. **Explainable 8-Pillar Rule Engine** (Deterministic regex & multi-factor pattern scoring).
2. **KAVACH-AI Multilingual Calibrated Classifier v1.0** (Sublinear TF-IDF + Platt-scaled Logistic Regression).
3. **Hybrid Risk Engine** (5-layer hierarchical safety precedence and Rule-Priority Shield fusion).

> **HONEST SCOPE DISCLOSURE**: All metrics in this report were measured strictly on the 75-sample held-out synthetic test set. These results demonstrate that the classifier has successfully learned the distinctive vocabulary and structure of the synthetic scenario archetypes across diverse turn lengths (4, 6, 8, 10 turns) and personas. **They do not represent real-world performance on unconstrained, noisy telecommunications audio in the field.**

---

## 2. Test Dataset Specification
- **Test Set Size**: 75 conversations (independent, held-out scenario archetypes; 0% train/val leakage).
- **Languages**: 15 English (`en`), 15 Hindi (`hi`), 15 Telugu (`te`), 15 Telugu-English (`te-en`), 15 Hindi-English (`hi-en`).
- **Class Breakdown**: 30 SCAM (40.0%), 30 LEGITIMATE (40.0%), 15 AMBIGUOUS (20.0%).
- **Turn Lengths**: Stratified across 4, 6, 8, and 10 dialogue turns.

---

## 3. Comparative Benchmark Results

| System / Architecture | Test Accuracy | Macro Precision | Macro Recall | Macro F1 | Measured CPU Latency (P50 / P95) | Artifact Footprint |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **8-Pillar Rule Engine Alone** | 46.7% | 0.5080 | 0.4556 | 0.4149 | **0.9 ms / 1.8 ms** | < 2 MB |
| **Calibrated ML Classifier (Ours)** | **100.0%** | **1.0000** | **1.0000** | **1.0000** | **10.27 ms / 23.06 ms** | **553 KB** |
| **Hybrid Risk Engine (Rules + ML)** | **100.0%** | **1.0000** | **1.0000** | **1.0000** | **11.20 ms / 24.50 ms** | **~5 MB** |

*Note on Transformer Architectures: Structured notebooks for fine-tuning XLM-RoBERTa and MuRIL are preserved in `notebooks/KAVACH_AI_Multilingual_Training.ipynb` as future research workflows for GPU execution. They have not been fine-tuned locally and no benchmark claims are made for unexecuted models.*

---

## 4. Confusion Matrix (Calibrated ML Classifier on Test Set)

```
                    PREDICTED CLASS
                LEGITIMATE   AMBIGUOUS   SCAM
ACTUAL  LEGIT       30           0         0
CLASS   AMBIG        0          15         0
        SCAM         0           0        30
```

- **Accuracy**: 100.0% (75/75 correct)
- **Macro F1**: 1.0000
- **Weighted F1**: 1.0000

---

## 5. Baseline Comparison: Rule Engine vs. ML Model
The 8-pillar deterministic rule engine is engineered to identify explicit threat signatures (CBI, digital arrest, AnyDesk, OTP theft, coercive safe accounts).
- On the held-out test set, the rule engine achieves 46.7% accuracy (`[[19, 11, 0], [14, 1, 0], [11, 4, 15]]`).
- It flags explicit scam attacks effectively, but conservative scoring means ambiguous inquiries and subtle scams without explicit keywords require statistical classification.
- **Role of the ML Classifier**: The TF-IDF model learns the vocabulary of legitimate institutional communications, ambiguous pushback inquiries, and subtle scams across Indian languages.
- **Role of Hybrid Fusion**: The Hybrid Risk Engine combines deterministic explainability and guaranteed safety shields with the statistical discriminative power of the calibrated ML model.

---

## 6. Cross-Split Similarity Diagnostics

Evaluated across split pairs using nearest-neighbor TF-IDF vectorization:

| Split Comparison | Word (1-2) Min | Word (1-2) Mean | Word (1-2) P50 | Word (1-2) P90 | Word (1-2) Max | Char (3-5) P50 | Char (3-5) Max |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Train -> Validation** | 0.260 | 0.580 | 0.593 | 0.740 | 0.807 | 0.713 | 0.833 |
| **Train -> Test** | 0.276 | 0.605 | 0.622 | 0.730 | 0.791 | 0.728 | 0.834 |
| **Validation -> Test** | 0.249 | 0.576 | 0.594 | 0.716 | 0.781 | 0.712 | 0.817 |

---

## 7. Real Latency Measurements on Host CPU
Measured over 100 iterations of full text vectorization and calibrated probability inference:
- **Mean Latency**: 11.68 ms
- **Median (P50) Latency**: 10.27 ms
- **95th Percentile (P95) Latency**: 23.06 ms
- **Throughput**: ~85 transcripts per second on a single CPU core.
