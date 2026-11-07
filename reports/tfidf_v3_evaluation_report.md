# KAVACH AI — TF-IDF v3 Held-Out Test Evaluation Report

**Evaluation Target**: TF-IDF Multilingual Calibrated Classifier v3.0  
**Test Corpus**: `data/kavach_synthetic_v3/splits/test.jsonl` ($N=450$)  
**Evaluation Date**: 2026-11-07  
**Benchmark Script**: `scripts/evaluate_tfidf_v3.py`  
**Operational Status**: **EXPERIMENTAL_BENCHMARK_ONLY**

---

## 1. Executive Summary

This report provides the formal evaluation of the retrained **TF-IDF v3** classifier on the independent, held-out test partition of Dataset v3. The test set comprises exactly **450 records** (180 `SCAM`, 135 `LEGITIMATE`, 135 `AMBIGUOUS`), distributed evenly across 5 languages (90 samples each in English, Hindi, Telugu, Hinglish, and Tenglish).

In addition, the 8-pillar deterministic rule engine was benchmarked on the **exact same 450 records**, establishing the performance differential between deterministic heuristic parsing and statistical ML inference.

```
Headline Performance Metrics:
• Held-Out Test Size:  450 records (100% unseen during training/selection)
• Overall Accuracy:    100.00% (450 / 450)
• Macro F1-Score:      1.0000
• Weighted F1-Score:   1.0000
• AMBIGUOUS Recall:    100.00% (135 / 135)
• SCAM Recall:         100.00% (180 / 180)
• LEGITIMATE Recall:   100.00% (135 / 135)
• Mean CPU Latency:    4.27 ms (P50: 3.77 ms, P95: 7.08 ms)
• Throughput:          234.4 inferences / second
• Rule Engine Delta:   +41.33% Accuracy over Rule-Only Engine (58.67% -> 100.0%)
```

---

## 2. Test Split Composition

The test split exhibits strict balance across labels and languages, with 0% data leakage from training or validation splits:

| Language | Code | SCAM Samples | LEGITIMATE Samples | AMBIGUOUS Samples | Total Records |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **English** | `en` | 36 | 27 | 27 | 90 |
| **Hindi** (Devanagari) | `hi` | 36 | 27 | 27 | 90 |
| **Telugu** (Telugu Script) | `te` | 36 | 27 | 27 | 90 |
| **Hinglish** (Latin Script) | `hi-en` | 36 | 27 | 27 | 90 |
| **Tenglish** (Latin Script) | `te-en` | 36 | 27 | 27 | 90 |
| **TOTAL** | — | **180 (40.0%)** | **135 (30.0%)** | **135 (30.0%)** | **450 (100%)** |

---

## 3. Overall Classification Performance

### Detailed Classification Report

| Class | Precision | Recall | F1-Score | Support (N) | Correct Predictions |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **LEGITIMATE** | 1.0000 | 1.0000 | 1.0000 | 135 | 135 |
| **AMBIGUOUS** | 1.0000 | 1.0000 | 1.0000 | 135 | 135 |
| **SCAM** | 1.0000 | 1.0000 | 1.0000 | 180 | 180 |
| **Macro Average** | **1.0000** | **1.0000** | **1.0000** | **450** | **450** |
| **Weighted Average** | **1.0000** | **1.0000** | **1.0000** | **450** | **450** |

### Confusion Matrix ($3 \times 3$)

```
                        PREDICTED CLASS
                 LEGITIMATE   AMBIGUOUS     SCAM
ACTUAL  LEGIT         135           0          0
CLASS   AMBIG           0         135          0
        SCAM            0           0        180
```

- **True Positives**: 135 LEGITIMATE, 135 AMBIGUOUS, 180 SCAM.
- **False Positives / False Negatives**: 0 across all classes.

---

## 4. Per-Language Performance Breakdown

Every language group was evaluated separately on its 90 allocated test records:

| Language | Script / Modality | Accuracy | Macro Precision | Macro Recall | Macro F1 | AMBIG F1 | SCAM F1 | LEGIT F1 |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **English (`en`)** | Latin (Standard English) | 100.0% | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| **Hindi (`hi`)** | Devanagari Script | 100.0% | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| **Telugu (`te`)** | Telugu Script | 100.0% | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| **Hinglish (`hi-en`)** | Latin (Code-Mixed) | 100.0% | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| **Tenglish (`te-en`)** | Latin (Code-Mixed) | 100.0% | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

### Key Observations:
1. **Script Invariance**: The TF-IDF sublinear n-gram representations captured native Indic scripts (Devanagari, Telugu) as cleanly as Latin-script code-mixed dialogue.
2. **Ambiguous Boundary Disambiguation**: The previous failure mode of baseline v2 models—collapsing `AMBIGUOUS` calls into `LEGITIMATE`—is completely resolved on Dataset v3 due to the balanced 30% ambiguous training representation (630 samples) and distinct archetype templates.

---

## 5. Comparative Baseline: 8-Pillar Rule Engine on the Same Test Split

To demonstrate the concrete value of the ML classifier over rule-only heuristics, the deterministic 8-pillar threat engine was evaluated on the identical 450 test records:

| System | Test Accuracy | Macro Precision | Macro Recall | Macro F1 | SCAM Recall | AMBIG Recall | LEGIT Recall |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **8-Pillar Deterministic Rule Engine** | 58.67% | 0.6185 | 0.5753 | 0.5844 | 68.89% | 60.00% | 43.70% |
| **TF-IDF v3 Multilingual Model** | **100.00%** | **1.0000** | **1.0000** | **1.0000** | **100.00%** | **100.00%** | **100.00%** |
| **Performance Advantage ($\Delta$)** | **+41.33%** | **+0.3815** | **+0.4247** | **+0.4156** | **+31.11%** | **+40.00%** | **+56.30%** |

### Rule Engine Confusion Matrix ($N=450$)

```
                 PREDICTED (Rule-Only)
                 LEGITIMATE   AMBIGUOUS     SCAM
ACTUAL  LEGIT          59          76          0
CLASS   AMBIG          54          81          0
        SCAM           45          11        124
```

### Analysis of Rule Engine Limitations:
1. **Under-detection of Subtle Scams (45 False Negatives)**: 45 SCAM conversations used social engineering without invoking hardcoded keywords (e.g. subtle refund pretexting, urgent survey verification), causing the rule engine to score them as LEGITIMATE ($<20.0$ risk score).
2. **Ambiguity Conflation (76 False Ambiguities)**: 76 LEGITIMATE calls mentioning routine account security procedures were marked AMBIGUOUS ($20-39$ risk score) by rules because keywords like "account" and "verification" triggered low-severity heuristic rules.
3. **Hybrid Validation**: This empirical comparison justifies KAVACH AI's hybrid architecture: the ML classifier provides generalizable semantic discrimination, while the deterministic rule engine provides the unbreakable Rule-Priority Shield against high-consequence zero-day bypasses.

---

## 6. CPU Latency & Resource Utilization Benchmark

Benchmarked over **200 consecutive inference cycles** on local hardware:

| Benchmark Metric | Measured Value | Production SLA Target | Compliance |
| :--- | :---: | :---: | :---: |
| **Mean CPU Latency** | **4.27 ms** | $< 25.0$ ms | **PASS (Superior)** |
| **Median (P50) Latency** | **3.77 ms** | $< 20.0$ ms | **PASS (Superior)** |
| **95th Percentile (P95) Latency** | **7.08 ms** | $< 50.0$ ms | **PASS (Superior)** |
| **Throughput** | **234.4 inferences/sec** | $> 50$ inferences/sec | **PASS (Superior)** |
| **Vectorizer Disk Footprint** | 199.1 KB | $< 5.0$ MB | **PASS** |
| **Classifier Model Disk Footprint** | 354.3 KB | $< 10.0$ MB | **PASS** |
| **Total Artifact Footprint** | **553.4 KB** | $< 15.0$ MB | **PASS** |

---

## 7. Limitations & Honest Disclosures

1. **Synthetic Telephony Boundary**: A 100% test score on synthetically generated text transcripts does not establish 100% field accuracy on wild telephone calls. Real telephone calls contain acoustic distortions, 8 kHz AMR-NB speech codec artifacts, speech-to-text recognition errors (WER 15–30%), and unscripted caller interruptions.
2. **Annotation Provenance**: All 450 test records carry `annotation_status: pending_review`. No records were verified by certified human cybersecurity analysts.
3. **Historical Non-Comparability**: Historical benchmark results on Dataset v2 ($N=75$) cannot be directly compared to Dataset v3 ($N=450$) due to differing sample sizes, vocabulary sizes, and scenario distributions.

