# KAVACH AI Synthetic Voice Scam & Vishing Dataset v3.0

The **KAVACH Synthetic Dataset v3** is an expanded, high-diversity, multilingual voice-call dataset designed to train and benchmark speech and NLP models (such as Google's MuRIL) for scam, vishing, and financial fraud detection across Indian telephony languages.

---

## Dataset Overview

- **Total Conversations**: 3,000 multi-turn phone dialogues
- **Total Scenario Families**: 600 distinct scenario families (5 language records per family)
- **Languages**: 
  - English (`en`): 600
  - Hindi in Devanagari script (`hi`): 600
  - Telugu in Telugu script (`te`): 600
  - Hindi-English code-mixed / Hinglish (`hi-en`): 600
  - Telugu-English code-mixed / Tenglish (`te-en`): 600
- **Class Labels**:
  - `SCAM`: 1,200 records (40.0%)
  - `LEGITIMATE`: 900 records (30.0%)
  - `AMBIGUOUS`: 900 records (30.0%)
- **Splits**:
  - Train: 2,100 records (70.0%)
  - Validation: 450 records (15.0%)
  - Test: 450 records (15.0%)
- **Turn Counts**: 4 to 12 turns per dialogue (mean: 7.0 turns)
- **Annotation Status**: `pending_review`

---

## Directory Structure

```
data/kavach_synthetic_v3/
├── manifest.json                  # Machine-readable dataset manifest and split hashes
├── quality_report.md              # Comprehensive QA and anti-duplication report
├── ambiguous_review_report.md     # In-depth analysis of the 900 AMBIGUOUS records
├── README.md                      # This documentation card
├── raw/
│   └── generated_samples.jsonl    # 2,500 newly generated synthetic records
├── validated/
│   └── all_samples.jsonl          # 3,000 combined and validated master records
└── splits/
    ├── train.jsonl                # 2,100 training samples (70%)
    ├── validation.jsonl           # 450 validation samples (15%)
    └── test.jsonl                 # 450 held-out test samples (15%)
```

---

## Schema Reference

Each record in the JSONL files conforms to the following schema:

```json
{
  "sample_id": "KAV-SYNTH3-0001",
  "conversation_id": "KAV-SYNTH3-0001",
  "language": "en",
  "scenario_family": "CBI Money Laundering & Digital Arrest",
  "scenario": "CBI Money Laundering & Digital Arrest (EN)",
  "label": "SCAM",
  "primary_label": "SCAM",
  "dialogue": [
    {"speaker": "caller", "text": "..."},
    {"speaker": "recipient", "text": "..."}
  ],
  "transcript": "caller: ...\nrecipient: ...",
  "explanation": "Forensic description of scam or legitimate interaction...",
  "risk_indicators": ["DIGITAL_ARREST", "AUTHORITY_IMPERSONATION"],
  "annotation_status": "pending_review",
  "review_status": "pending_review",
  "source": "synthetic_generation",
  "version": "v3",
  "dataset_version": "v3.0",
  "archetype_id": "SCAM_V3_001",
  "split": "train"
}
```

---

## Leakage Prevention & Provenance

1. **Scenario-Family Isolation**: The 600 scenario families are strictly partitioned into 420 Train, 90 Validation, and 90 Test. Zero scenario families cross split boundaries.
2. **Dialogue Hash Uniqueness**: 3,000 / 3,000 dialogue texts are distinct.
3. **No Ground Truth Fabrications**: All samples are explicitly designated `annotation_status: pending_review`.
