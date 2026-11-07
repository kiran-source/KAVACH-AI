# KAVACH AI — Multilingual Dataset Card: Synthetic Vishing & Scam Corpora

## Dataset Summary
The KAVACH AI dataset suite comprises two versioned, domain-curated multilingual corpora designed specifically to benchmark and train voice scam detection algorithms across regional Indian contexts.

1. **`kavach_synthetic_v1` (Prototype & Audio Benchmark)**:
   - Exactly 100 domain-curated multi-turn dialogues across 5 language categories.
   - 20 synthesized authentic speech audio files generated via Gnani Timbre v2.5 TTS (4 files per language category: English, Hindi, Telugu, Telugu-English, Hindi-English; total duration: 331.84 seconds).
   - Validated against Gnani Prisma v3.0 STT integration and rule-based scam engines.

2. **`kavach_synthetic_v2` (Expanded Remediated ML Benchmark & Training Corpus)**:
   - Exactly 500 domain-curated conversations (100 per language category).
   - Strictly stratified 70% / 15% / 15% scenario-grouped splits (Train: 350, Validation: 75, Test: 75).
   - **Zero Exact Duplicates**: All 500 conversations have completely unique dialogue text (500 unique SHA-256 hashes).
   - **Zero Leakage**: Exactly 0% scenario family overlap and 0% dialogue text overlap between Train, Validation, and Test.
   - **High Conversational Diversity**:
     - Variable turn lengths: 4, 6, 8, and 10 turns.
     - 5 distinct recipient personas (Assertive Skeptic, Anxious Citizen, Busy Executive, Elderly Senior, Security-Aware Citizen).
     - 4 distinct caller approaches (Formal Enforcement Officer, Helpful Support Impersonation, Urgent Dispatch Ultimatum, Bureaucratic Investigator).
     - Legitimate calls discussing OTPs, police, fraud, and account security without being scams.
     - Subtle scams without overt keywords and realistic ambiguous gray-area calls.
   - **Honest Provenance & Status**: All 500 records carry `review_status: "pending_review"` and `synthetic_source: "KAVACH Domain-Curated Multilingual Scenario Engine v2.0"`. No human review or ground-truth verification is claimed.

---

## Language Distribution

| Language Category | Code | v1 Conversations | v1 Audio Files | v2 Conversations | Script / Form |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **English** | `en` | 20 | 4 WAVs | 100 | Latin / Indian English dialect |
| **Hindi** | `hi` | 20 | 4 WAVs | 100 | Devanagari script |
| **Telugu** | `te` | 20 | 4 WAVs | 100 | Telugu script |
| **Telugu-English** | `te-en` | 20 | 4 WAVs | 100 | Code-mixed Telugu + Latin English |
| **Hindi-English** | `hi-en` | 20 | 4 WAVs | 100 | Code-mixed Hindi + Latin Hinglish |
| **Total** | — | **100** | **20 WAVs** | **500** | — |

---

## Conversational Architecture & Diversity Metrics

To prevent synthetic template repetition across splits:
1. **Dialogue Length Distribution**:
   - 4 turns: 125 conversations (25%) — Swift, direct interactions.
   - 6 turns: 125 conversations (25%) — Progressive escalation interactions.
   - 8 turns: 125 conversations (25%) — Detailed investigative dialogues.
   - 10 turns: 125 conversations (25%) — Multi-stage complex interactions.
2. **5 Recipient Communication Personas**:
   - *Persona 0 (Assertive Skeptic)*: Demands case file numbers, badge ID, and written postal summons; states intent to verify with police.
   - *Persona 1 (Anxious Citizen)*: Shaken by the call, asks how an error occurred, consults spouse or family before taking action.
   - *Persona 2 (Busy Corporate Executive)*: Interrupts caller, in a boardroom meeting, requires formal communication sent to verified work email.
   - *Persona 3 (Elderly Senior / Pensioner)*: Non-technical, cannot navigate net banking or mobile apps, defers all financial matters to adult children.
   - *Persona 4 (Security-Aware Citizen)*: Detects social engineering patterns immediately, cites cyber safety rules, warns caller of police helpline 1930.

---

## Near-Duplicate Diagnostics & Cross-Split Similarity

Nearest-neighbor TF-IDF similarity computed across all split pairs:

| Split Comparison | Word (1-2) Min | Word (1-2) Mean | Word (1-2) P50 | Word (1-2) P90 | Word (1-2) Max | Char (3-5) P50 | Char (3-5) Max |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Train -> Validation** | 0.260 | 0.580 | 0.593 | 0.740 | 0.807 | 0.713 | 0.833 |
| **Train -> Test** | 0.276 | 0.605 | 0.622 | 0.730 | 0.791 | 0.728 | 0.834 |
| **Validation -> Test** | 0.249 | 0.576 | 0.594 | 0.716 | 0.781 | 0.712 | 0.817 |

> **Threshold & Limitations Disclosure**: Lexical similarity naturally captures shared domain-specific institutional and telephonic vocabulary (e.g. banking, courier, and legal terms). A similarity score alone neither proves nor disproves data leakage. Split independence is strictly enforced through 0% scenario-family overlap, 0% exact dialogue text hash overlap, and 0% conversation ID leakage.

---

## Split Allocation & Scenario Family Isolation (v2)

To eliminate train/test contamination:
- The 40 SCAM scenario archetypes are partitioned: 28 Train, 6 Validation, 6 Test.
- The 35 LEGITIMATE scenario archetypes are partitioned: 24 Train, 5 Validation, 6 Test.
- The 25 AMBIGUOUS scenario archetypes are partitioned: 18 Train, 4 Validation, 3 Test.

| Split | SCAM | LEGITIMATE | AMBIGUOUS | Total per Language | Total (5 Languages) | Ratio |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Train** | 28 | 24 | 18 | 70 | 350 | 70% |
| **Validation** | 6 | 5 | 4 | 15 | 75 | 15% |
| **Test** | 6 | 6 | 3 | 15 | 75 | 15% |
| **Total** | **40** | **35** | **25** | **100** | **500** | **100%** |

### Leakage Audit Results (`reports/split_integrity_report.json`):
- Train ∩ Validation exact duplicate dialogues: **0**
- Train ∩ Test exact duplicate dialogues: **0**
- Validation ∩ Test exact duplicate dialogues: **0**
- Train ∩ Validation scenario family overlap: **0**
- Train ∩ Test scenario family overlap: **0**
- Validation ∩ Test scenario family overlap: **0**

---

## Privacy, Ethics & Limitations
- **Zero Real PII**: All names, account references, phone numbers, and IDs are synthetic placeholders.
- **Unverified Labels**: All records carry `review_status: "pending_review"`. The dataset is an experimental synthetic prototype generated for model development and benchmarking under challenge constraints.
- **Telephony Noise Limitation**: Transcripts do not model real telephony audio channel artifacts (codec compression, packet loss, ambient acoustic noise, varied accents). Real-world wild telephony requires field validation.
