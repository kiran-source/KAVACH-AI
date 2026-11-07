# KAVACH AI — Synthetic Dataset v3 Quality & Audit Report

**Dataset Version**: v3.0  
**Generated Date**: 2026-11-07  
**Annotation Status**: `pending_review` (All 3,000 records marked pending human audit)  
**Total Corpus Size**: 3,000 records  
- **Existing v2 Accepted & Migrated**: 500 records (100% passed automated schema, diversity, and uniqueness checks)
- **New Synthesized Records**: 2,500 records (500 scenario families across 5 linguistic variants)

---

## 1. Class Distribution

| Class Label | Total Count | Percentage | Train (70%) | Validation (15%) | Test (15%) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **SCAM** | 1,200 | 40.0% | 840 | 180 | 180 |
| **LEGITIMATE** | 900 | 30.0% | 630 | 135 | 135 |
| **AMBIGUOUS** | 900 | 30.0% | 630 | 135 | 135 |
| **TOTAL** | **3,000** | **100.0%** | **2,100** | **450** | **450** |

---

## 2. Language Distribution

| Language Code | Language & Script | Total Records | Train | Validation | Test |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`en`** | English (Natural Colloquial & Corporate) | 600 | 420 | 90 | 90 |
| **`hi`** | Hindi (Devanagari Script) | 600 | 420 | 90 | 90 |
| **`te`** | Telugu (Telugu Script) | 600 | 420 | 90 | 90 |
| **`hi-en`** | Hindi-English Code-Mixed (Natural Hinglish) | 600 | 420 | 90 | 90 |
| **`te-en`** | Telugu-English Code-Mixed (Natural Tenglish) | 600 | 420 | 90 | 90 |
| **TOTAL** | **5 Balanced Linguistic Profiles** | **3,000** | **2,100** | **450** | **450** |

---

## 3. Strict Scenario-Family Partitioning & Leakage Elimination

All records belong to exactly one of **600 distinct scenario families** (5 linguistic records per family).
All 5 linguistic variants of any scenario family remain strictly confined within the same split:

- **Train Families**: 420 families (168 SCAM, 126 LEGIT, 126 AMBIG) = 2,100 records
- **Validation Families**: 90 families (36 SCAM, 27 LEGIT, 27 AMBIG) = 450 records
- **Test Families**: 90 families (36 SCAM, 27 LEGIT, 27 AMBIG) = 450 records

### Verified Cross-Split Leakage
- **Scenario Family Overlap**: **0% (Zero families cross splits)**
- **Exact Dialogue Text Overlap**: **0% (Zero identical transcripts)**
- **Conversation ID Overlap**: **0% (Zero CIDs cross splits)**

---

## 4. AMBIGUOUS Class Enhancement for MuRIL

The v2 dataset exhibited poor AMBIGUOUS recall on transformer models (0% recall on 15 test samples) because ambiguous samples were too sparse and lacked rich conversational evidence.
In dataset v3:
- AMBIGUOUS representations increased from **125 records to 900 records** (7.2x increase).
- Represents 180 distinct scenario families covering: unverified KYC reminders without credential demand, anomalous parcel deliveries, vague recruiter cold outreach, 5G network latency surveys, prematurely disconnected calls, municipal water meter queries, and unauthenticated consumer polls.
- Every AMBIGUOUS sample features a **mandatory 4-part analytical explanation**:
  1. *Caller Claims*: What identity and pretext the caller presents.
  2. *Evidence Available*: Explicit verifiable facts and polite behavior observed in dialogue.
  3. *Evidence Missing*: Crucial institutional authentication tokens missing from call.
  4. *Classification Rationale*: Detailed reasoning explaining why the dialogue cannot be conclusively designated as SCAM or LEGITIMATE.

---

## 5. Automated Quality Checks Passed

1. **JSONL Syntax**: 100% valid JSON per line across all splits.
2. **Mandatory Schema Fields**: `sample_id`, `conversation_id`, `language`, `scenario_family`, `label`, `transcript`, `explanation`, `risk_indicators`, `annotation_status`, `source`, `version`.
3. **Dialogue Turns**: Min 4 turns, Max 12 turns, Average 7.0 turns.
4. **Script Authenticity**: Authentic Devanagari in `hi`, authentic Telugu characters in `te`, authentic conversational transliteration in `hi-en` and `te-en`.
5. **No Synthetic Shortcuts**: Zero placeholder names, zero identical dialogue copy-pasting, zero superficial word substitutions.

---

## 6. Limitations & Human Review Protocol

- **Synthetic Telephony Nature**: Conversations are synthetically generated under domain-curated probabilistic grammars. They do not represent live telephony network recordings.
- **Pending Review Status**: All 3,000 records remain flagged with `annotation_status: pending_review`. Automated validation has passed, but human subject-matter expert review is required prior to safety certification.
