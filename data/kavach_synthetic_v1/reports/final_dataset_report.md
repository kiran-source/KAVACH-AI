# KAVACH AI — Complete Synthetic Dataset Final Audit Report

Generated: `2026-11-04 13:54:15 UTC`  
Status: **STAGE 3 BULK GENERATION COMPLETED SUCCESSFULLY**

---

## 1. Acceptance Criteria Verification

| Acceptance Criterion | Target Specification | Actual Realized Metric | Verdict |
| :--- | :---: | :---: | :---: |
| **Total Conversations** | Exactly 100 | **100** | **PASS** |
| **Scam Classification** | Exactly 40 | **40** | **PASS** |
| **Legitimate Classification** | Exactly 35 | **35** | **PASS** |
| **Ambiguous Classification** | Exactly 25 | **25** | **PASS** |
| **Language Balance** | 20 per language across 5 categories | **20 each** (en, hi, te, te-en, hi-en) | **PASS** |
| **Per-Language Class Balance** | 8 Scam, 7 Legit, 5 Ambig per language | **8 / 7 / 5 across all 5 languages** | **PASS** |
| **Synthetic Audio Files** | Exactly 20 Audio Files | **20 Audio Files** | **PASS** |
| **Audio Language Balance** | Exactly 4 Audio Files per language | **4 each** (en, hi, te, te-en, hi-en) | **PASS** |
| **Pilot Data Preservation** | Preserve all 5 Pilot Conversations & Audio | **5/5 Pilots Preserved Intact** | **PASS** |
| **Dialogue Turn Limits** | 6 to 12 Turns per conversation | **All 100 within 6–12 turns (8 turns avg)** | **PASS** |
| **PII & Credential Isolation** | 0 Real Phone / Aadhaar / Card Numbers | **0 Violations (Regex Checked)** | **PASS** |
| **Storage Consumption** | < 500 MB Budget | **10.66 MB used** | **PASS** |
| **Dataset Splits (70/15/15)** | 70 Train / 15 Val / 15 Test | **70 / 15 / 15 (Zero template leak)** | **PASS** |

---

## 2. Audio Synthesis Inventory (20 Files)

| ID | Language | Class | Audio File | Duration (s) | Model |
| :--- | :---: | :---: | :--- | :---: | :--- |
| `KAV-SYNTH-001` | `en` | SCAM | `data\kavach_synthetic_v1\audio\english\kav-synth-pilot-001.wav` | 4.00s | preserved_pilot_audio |
| `KAV-SYNTH-002` | `en` | SCAM | `data\kavach_synthetic_v1\audio\english\kav_synth_002.wav` | 20.32s | preserved_pilot_audio |
| `KAV-SYNTH-009` | `en` | LEGITIMATE | `data\kavach_synthetic_v1\audio\english\kav_synth_009.wav` | 24.16s | preserved_pilot_audio |
| `KAV-SYNTH-016` | `en` | AMBIGUOUS | `data\kavach_synthetic_v1\audio\english\kav_synth_016.wav` | 20.64s | preserved_pilot_audio |
| `KAV-SYNTH-021` | `hi` | SCAM | `data\kavach_synthetic_v1\audio\hindi\kav-synth-pilot-002.wav` | 4.00s | preserved_pilot_audio |
| `KAV-SYNTH-022` | `hi` | SCAM | `data\kavach_synthetic_v1\audio\hindi\kav_synth_022.wav` | 21.60s | preserved_pilot_audio |
| `KAV-SYNTH-029` | `hi` | LEGITIMATE | `data\kavach_synthetic_v1\audio\hindi\kav_synth_029.wav` | 22.08s | preserved_pilot_audio |
| `KAV-SYNTH-036` | `hi` | AMBIGUOUS | `data\kavach_synthetic_v1\audio\hindi\kav_synth_036.wav` | 20.00s | preserved_pilot_audio |
| `KAV-SYNTH-041` | `te` | SCAM | `data\kavach_synthetic_v1\audio\telugu\kav-synth-pilot-003.wav` | 4.00s | preserved_pilot_audio |
| `KAV-SYNTH-042` | `te` | SCAM | `data\kavach_synthetic_v1\audio\telugu\kav_synth_042.wav` | 17.92s | preserved_pilot_audio |
| `KAV-SYNTH-049` | `te` | LEGITIMATE | `data\kavach_synthetic_v1\audio\telugu\kav_synth_049.wav` | 20.32s | preserved_pilot_audio |
| `KAV-SYNTH-056` | `te` | AMBIGUOUS | `data\kavach_synthetic_v1\audio\telugu\kav_synth_056.wav` | 18.56s | preserved_pilot_audio |
| `KAV-SYNTH-061` | `te-en` | SCAM | `data\kavach_synthetic_v1\audio\telugu_english\kav_synth_061.wav` | 20.64s | preserved_pilot_audio |
| `KAV-SYNTH-062` | `te-en` | SCAM | `data\kavach_synthetic_v1\audio\telugu_english\kav_synth_062.wav` | 21.76s | preserved_pilot_audio |
| `KAV-SYNTH-069` | `te-en` | LEGITIMATE | `data\kavach_synthetic_v1\audio\telugu_english\kav_synth_069.wav` | 17.92s | preserved_pilot_audio |
| `KAV-SYNTH-076` | `te-en` | AMBIGUOUS | `data\kavach_synthetic_v1\audio\telugu_english\kav-synth-pilot-004.wav` | 4.00s | preserved_pilot_audio |
| `KAV-SYNTH-081` | `hi-en` | SCAM | `data\kavach_synthetic_v1\audio\hindi_english\kav_synth_081.wav` | 21.44s | preserved_pilot_audio |
| `KAV-SYNTH-082` | `hi-en` | SCAM | `data\kavach_synthetic_v1\audio\hindi_english\kav_synth_082.wav` | 22.72s | preserved_pilot_audio |
| `KAV-SYNTH-089` | `hi-en` | LEGITIMATE | `data\kavach_synthetic_v1\audio\hindi_english\kav-synth-pilot-005.wav` | 4.00s | preserved_pilot_audio |
| `KAV-SYNTH-096` | `hi-en` | AMBIGUOUS | `data\kavach_synthetic_v1\audio\hindi_english\kav_synth_096.wav` | 21.76s | preserved_pilot_audio |

---

## 3. Storage & Resource Accounting

- **Dataset Root**: `data/kavach_synthetic_v1/`
- **Total Dataset Size**: **10.66 MB**
- **Available Free Space on Host**: **57265.6 MB**
- **Storage Budget**: 500.0 MB (Consumed: 2.1%)

---

## 4. API Usage Ledger Summary

- **Total Requests Tracked**: 48
- **Successful Requests**: 48
- **Failed Requests**: 0
- **Total Audio Duration Generated**: 427.84 seconds
- **Prisma STT Validation Note**: Limited strictly to pilot sample in accordance with credit preservation guidelines; Telugu Cloudflare WAF limitation documented as upstream restriction.
