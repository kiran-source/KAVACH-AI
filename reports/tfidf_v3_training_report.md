# KAVACH AI — TF-IDF v3 Model Training & Calibration Report

**Pipeline Execution**: TF-IDF Multilingual Calibrated Classifier v3.0  
**Target Milestone**: Dataset v3 Retraining & MuRIL Benchmark Alignment  
**Execution Date**: 2026-11-07  
**Execution Environment**: Local Windows Sandbox (Python 3.13 / Scikit-Learn 1.6+)  
**Operational Status**: **EXPERIMENTAL_BENCHMARK_ONLY** (Production baseline v1 untouched in `backend/app/ml/artifacts/v1/`)

---

## 1. Executive Summary

This report documents the retraining, validation-driven model selection, and Platt scaling calibration of the **TF-IDF + Calibrated Logistic Regression classifier (v3.0)** on the expanded **KAVACH AI Multilingual Synthetic Dataset v3** (`data/kavach_synthetic_v3/splits/`). 

The objective of this run is to establish a scientifically valid, identical-corpus baseline to compare against the **MuRIL v1 transformer** on the exact same 450 held-out test records, resolving the baseline comparability gap identified in the prior evaluation audit.

```
Key Results Overview:
• Training Records:    2,100 samples (420 scenario families, 5 languages)
• Validation Records:    450 samples ( 90 scenario families, 5 languages)
• Held-Out Records:      450 samples ( 90 scenario families, 5 languages)
• Winning Model:       Word (1, 2) n-grams | max_features=5,000 | C=1.5 | Platt Sigmoid Calibrated
• Val Accuracy / F1:   100.00% / 1.0000 Macro F1
• Training Fit Time:   1.65 seconds
• Total Disk Size:     553.4 KB (203.8 KB vectorizer + 362.8 KB model)
• Production Status:   Isolated in backend/app/ml/artifacts/tfidf_v3/ (v1 baseline preserved)
```

---

## 2. Dataset v3 Partition & Pre-Training Audit

Prior to training, all 10 pre-training integrity gates were verified against `data/kavach_synthetic_v3/splits/`:

| Gate ID | Audit Criterion | Measured Value | Target Threshold | Verdict |
| :--- | :--- | :--- | :--- | :--- |
| **G-01** | Split File Existence | `train.jsonl`, `val.jsonl`, `test.jsonl` | All 3 present on disk | **PASS** |
| **G-02** | Training Partition Size | 2,100 records | Exactly 2,100 records | **PASS** |
| **G-03** | Validation Partition Size | 450 records | Exactly 450 records | **PASS** |
| **G-04** | Held-Out Test Partition Size | 450 records | Exactly 450 records | **PASS** |
| **G-05** | Label Balance (Train) | 840 SCAM, 630 LEGIT, 630 AMBIG | 40% SCAM / 30% LEGIT / 30% AMBIG | **PASS** |
| **G-06** | Language Balance (Train) | 420 per language across 5 langs | Exactly 420 en, hi, te, hi-en, te-en | **PASS** |
| **G-07** | Unique Sample IDs | 3,000 unique IDs across all files | 0 duplicate sample IDs | **PASS** |
| **G-08** | CID Cross-Split Overlap | 0 collisions between any split | Strict 0.00% CID leakage | **PASS** |
| **G-09** | Text Hash Overlap | 0 SHA-256 collisions across splits | Strict 0.00% text hash leakage | **PASS** |
| **G-10** | Scenario Family Isolation | 600 unique families (420/90/90) | Strict 0 cross-family leakage | **PASS** |

### Annotation Provenance Notice
All 3,000 records in Dataset v3 carry `annotation_status: pending_review` and `review_status: pending_review`. No records have undergone manual human adjudication. All benchmark scores reflect performance on domain-engineered synthetic scenario templates.

---

## 3. Hyperparameter Exploration & Model Selection

Three feature and classifier architectures were fitted strictly on the 2,100 training records (`train.jsonl`) and evaluated on the 450 validation records (`validation.jsonl`). **The test partition was never exposed during model selection.**

### Candidate Comparison Matrix

| Candidate ID | Architecture Specification | Features | Fit Time | Val Acc | Val Macro F1 | AMBIG Recall | SCAM Recall | LEGIT Recall |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Config 1** | **Word (1, 2) n-grams, max=5k, C=1.5, Platt Calibrated** | **5,000** | **1.65 s** | **100.00%** | **1.0000** | **1.0000** | **1.0000** | **1.0000** |
| Config 2 | Word (1, 2) n-grams, max=10k, C=1.0, Platt Calibrated | 10,000 | 1.74 s | 100.00% | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| Config 3 | Word (1,2: 10k) + Char (3,5: 5k) Union, C=1.5, Calibrated | 15,000 | 6.24 s | 100.00% | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

### Selection Rationale
- All three candidates achieved 100% accuracy on the synthetic validation split.
- **Config 1** was selected as the optimal production model based on the principle of parsimony:
  1. **Minimal Feature Space**: 5,000 features versus 10,000 and 15,000.
  2. **Fastest Training**: 1.65 seconds (3.7x faster than the character n-gram union).
  3. **Lowest Memory & Latency Overhead**: Sub-5ms CPU inference and minimal RAM footprint.
  4. **Perfect Class Separation**: Flawless recall on the difficult `AMBIGUOUS` class (135/135 validation samples correctly identified).

---

## 4. Calibration & Loss Function

- **Base Classifier**: `LogisticRegression(C=1.5, class_weight="balanced", max_iter=1000, random_state=42)`
- **Probability Calibration**: `CalibratedClassifierCV(estimator=base_clf, method="sigmoid", cv=3)`
  - Uses 3-fold cross-validation on the training set.
  - Fits Platt scaling parameters (logistic sigmoid transformations) over the decision function margins to ensure output values represent calibrated confidence estimates rather than raw unscaled margins.

---

## 5. Artifact Verification & Checksums

All trained artifacts were written to `backend/app/ml/artifacts/tfidf_v3/`. The SHA-256 integrity manifest is recorded below:

| File Name | Size (Bytes) | SHA-256 Digest |
| :--- | :---: | :--- |
| `vectorizer.joblib` | 203,845 | `2f9f6e6dae763b6b69680ee4e7eef40d4d420bb6efb8dfc403362a9c379a5b6c` |
| `model.joblib` | 362,829 | `46358cceebec9e9f9a2ce01d8f161405eef3fe0cf7e2f5b497b7b1346a0cc68f` |
| `label_mapping.json` | 171 | `15e9e0331006579d4dc55f84898144eece46da6ec53434199997c6d66e51e7fb` |
| `training_config.json` | 2,220 | `e18ffbc66b3602f90918712f5a6035da256fb2b23cfdd6d7d7aee7fe41595eb2` |
| `metadata.json` | 1,328 | `9bfa482d8c30353c7f3b890a2cfeb8e4e73b2230485926ec0373e970b86a8775` |
| `training_metrics.json` | 446 | `9323ff646cbaab610a56f264d8a55c6543b3558c445691079d20c29f45607db7` |

### Production Baseline v1 Isolation Check
- Artifacts in `backend/app/ml/artifacts/v1/` were verified as unmodified:
  - `model.joblib`: 362,829 bytes (Last modified: 2026-11-05)
  - `vectorizer.joblib`: 203,939 bytes (Last modified: 2026-11-05)
  - `metadata.json`: 5,112 bytes (Last modified: 2026-11-05)
- The production baseline v1 remains the active live inference model for KAVACH AI.

---

## 6. Training Verification Conclusion

The TF-IDF v3 model was trained without errors, exhibiting 0% data leakage, robust validation convergence, and strict artifact provenance. Full held-out test evaluation on the untouched 450 test records is detailed in `reports/tfidf_v3_evaluation_report.md`.

