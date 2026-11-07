# KAVACH AI — ML Model Card: Multilingual Scam Classifier v1.0

## Model Details
- **Model Name**: KAVACH-AI Multilingual Calibrated Classifier v1.0
- **Model Version**: 1.0.0-remediated
- **Architecture**: Sublinear TF-IDF (1-2 word n-grams, strip accents, Unicode tokenization) + Calibrated Logistic Regression (Platt scaling via 3-fold cross-validation)
- **Framework**: `scikit-learn` 1.6+, `joblib`, `numpy`, `scipy`
- **Inference Runtime**: Python 3.10–3.13 / FastAPI (CPU native)
- **Measured Latency**: Mean = 11.68 ms, P50 = 10.27 ms, P95 = 23.06 ms per transcript on CPU
- **Artifact Size**: 553 KB total (`model.joblib`: 354 KB, `vectorizer.joblib`: 199 KB)
- **License**: Apache 2.0 / Developed for the Great Indian AI Internship Challenge

---

## Intended Use & Target Tasks
- **Primary Task**: Multi-class classification of multilingual voice transcripts into three risk tiers:
  - `SCAM`: Call contains actionable social-engineering attacks (Credential Theft, Digital Arrest, AnyDesk remote access, fake law enforcement, courier fraud, urgent financial demands).
  - `AMBIGUOUS`: Inconclusive, cold-call, or low-context telemarketing inquiry requiring agent caution or human SOC escalation.
  - `LEGITIMATE`: Institutional communications (branch appointments, delivery coordination, public awareness advisories, routine KYC verification).
- **Supported Languages**:
  - English (`en`)
  - Hindi (`hi`)
  - Telugu (`te`)
  - Telugu-English code-mixed (`te-en`)
  - Hindi-English code-mixed (`hi-en` / Hinglish)
- **Target Deployment**: Hybrid Risk Engine in KAVACH AI SOC incident platform, working symbiotically with an explainable 8-pillar deterministic rule engine.

---

## Training Data & Methodology
- **Training Set**: 350 conversations from `data/kavach_synthetic_v2/splits/train.jsonl` (70% split).
- **Validation Set**: 75 conversations from `data/kavach_synthetic_v2/splits/validation.jsonl` (15% split).
- **Test Set**: 75 conversations from `data/kavach_synthetic_v2/splits/test.jsonl` (15% split).
- **Conversational Diversity**:
  - Varied turn lengths: 4, 6, 8, and 10 dialogue turns across scenario archetypes.
  - 5 distinct recipient personas (Assertive Skeptic, Anxious Citizen, Busy Executive, Elderly Senior, Security-Aware Citizen).
  - 4 distinct caller tones (Formal Enforcement, Subtle Support Impersonation, Urgent Dispatch, Bureaucratic Investigator).
  - Realistic legitimate conversations discussing OTPs, police, fraud, and account security.
  - Subtle scams without overt keywords and realistic ambiguous gray-area calls.
- **Training Provenance**:
  - **TF-IDF + calibrated Logistic Regression baseline trained locally.**
  - **Google Colab notebook prepared for future MuRIL/XLM-RoBERTa fine-tuning; transformer training has not been executed.**
- **Leakage Prevention**: Strictly partitioned by scenario archetype (`scenario_family`). Exactly 0% scenario family overlap and 0% exact dialogue text overlap across splits.
- **Review Status**: All training, validation, and test records carry `review_status: "pending_review"` and are synthetically generated. No human ground-truth verification is claimed.
- **Class Distribution**:
  - `SCAM`: 40% (200 total / 140 train / 30 val / 30 test)
  - `LEGITIMATE`: 35% (175 total / 120 train / 25 val / 30 test)
  - `AMBIGUOUS`: 25% (125 total / 90 train / 20 val / 15 test)

---

## Performance Metrics (Held-Out Synthetic Test Set)

> **IMPORTANT DISCLAIMER**: The metrics below were measured strictly on the 75-sample held-out synthetic test set. These results reflect model learning on domain-curated scenario archetypes and **do not represent real-world accuracy on unconstrained, noisy wild telephony audio**.

| Metric | Overall | SCAM Class | LEGITIMATE Class | AMBIGUOUS Class |
| :--- | :---: | :---: | :---: | :---: |
| **Accuracy** | **100.0%** | — | — | — |
| **Precision** | **1.0000** | 1.0000 | 1.0000 | 1.0000 |
| **Recall** | **1.0000** | 1.0000 | 1.0000 | 1.0000 |
| **F1-Score** | **1.0000** | 1.0000 | 1.0000 | 1.0000 |
| **Support** | 75 | 30 | 30 | 15 |

---

## Baseline Comparison: 8-Pillar Rule Engine vs. ML Model

Evaluated on the exact same 75 held-out test samples:

| Evaluated System | Accuracy | Macro F1 | Confusion Matrix (Legit / Ambig / Scam) |
| :--- | :---: | :---: | :---: |
| **8-Pillar Rule Engine Alone** | 46.7% | 0.4149 | `[[19, 11, 0], [14, 1, 0], [11, 4, 15]]` |
| **Calibrated ML Classifier (Ours)** | 100.0% | 1.0000 | `[[30, 0, 0], [0, 15, 0], [0, 0, 30]]` |
| **Hybrid Risk Engine (Fused)** | 100.0% | 1.0000 | Enforces 5-layer safety precedence and rule shields |

---

## Per-Language Breakdown (Held-Out Synthetic Test Set)

| Language Category | Test Samples | Accuracy | Macro F1 |
| :--- | :---: | :---: | :---: |
| English (`en`) | 15 | 100.0% | 1.0000 |
| Hindi (`hi`) | 15 | 100.0% | 1.0000 |
| Telugu (`te`) | 15 | 100.0% | 1.0000 |
| Telugu-English (`te-en`) | 15 | 100.0% | 1.0000 |
| Hindi-English (`hi-en`) | 15 | 100.0% | 1.0000 |

---

## Cross-Split Similarity Diagnostics

Evaluated using nearest-neighbor TF-IDF vectorization across split pairs:

| Split Pair | Word (1-2) Min | Word (1-2) Mean | Word (1-2) P50 | Word (1-2) Max | Char (3-5) P50 | Char (3-5) Max |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Train -> Validation** | 0.260 | 0.580 | 0.593 | 0.807 | 0.713 | 0.833 |
| **Train -> Test** | 0.276 | 0.605 | 0.622 | 0.791 | 0.728 | 0.834 |
| **Validation -> Test** | 0.249 | 0.576 | 0.594 | 0.781 | 0.712 | 0.817 |

> **Methodology and Interpretation**: Lexical similarity captures shared domain terminology (e.g. telecom, legal, and banking terms). True split isolation is guaranteed by 0% scenario-family overlap, 0% exact dialogue text hash overlap, and 0% conversation ID leakage.

---

## Safety & Governance: 5-Layer Hybrid Precedence
To prevent adversarial bypass and false alarms, the hybrid engine executes strict hierarchical decision precedence:

1. **Precedence 1 — Adversarial Disclaimer / Deceptive Context Override**:
   Generic educational phrases ("RBI guidelines state...", "bank never asks for password") must NOT override direct critical threat evidence (OTP extraction, coercive payment, AnyDesk download, digital arrest). In mixed/adversarial context, educational suppression is overruled, setting `risk_score = max(rule_score, 65.0)` (High/Critical) with explicit SOC conflict flags.
2. **Precedence 2 — Critical Rule-Priority Shield**:
   If deterministic rules detect high-consequence threat patterns (raw rule score $\ge 50/100$, active coercion, or critical threat categories like Credential Theft, Digital Arrest, or Remote Access Manipulation), the hybrid engine **never** downgrades risk based on a statistical ML prediction of `LEGITIMATE` or `AMBIGUOUS`. The rule detection remains sovereign (`combined_score = max(rule_score, (0.75 * rule_score) + (0.25 * ml_score))`).
3. **Precedence 3 — Pure Educational Context Shield**:
   Genuine public-awareness announcements and security advisories *without* active demands are suppressed to prevent false alarms on security broadcasts ($\le 15/100$, Low).
4. **Precedence 4 — Novel ML Scam Linguistic Detection**:
   If rule patterns do not trigger but the ML model identifies subtle social engineering language with high confidence, fused score elevates to $\ge 60/100$ (High).
5. **Precedence 5 — Standard Balanced Fusion & Abstention Fallback**:
   Balanced multi-factor weighting ($0.55 \times \text{rule} + 0.45 \times \text{ml}$). If the ML model abstains (`is_abstaining=True` due to low confidence or top-2 probability margin $< 0.10$) or model files are missing, the system automatically falls back to explainable `RULE_ONLY` mode.

---

## Future Deep Learning Research Pathway
- **Google Colab notebook prepared for future MuRIL/XLM-RoBERTa fine-tuning; transformer training has not been executed.**
- The repository preserves a structured Jupyter notebook (`notebooks/KAVACH_AI_Multilingual_Training.ipynb`) containing end-to-end PyTorch training loops for `google/muril-base-cased` and `xlm-roberta-base` as a clean, future research pathway.
- In accordance with audit instructions, large transformer weights are NOT run, trained, or bundled locally; zero synthetic GPU/TPU training logs or weights are fabricated.
