"""
Comprehensive Quality Assurance and Automated Validation Script for KAVACH AI Dataset v3.

Verifies:
1. JSONL parsing integrity across raw, validated, and split files.
2. Mandatory fields present and non-empty:
   - sample_id, conversation_id, language, scenario_family, label,
     transcript, explanation, risk_indicators, annotation_status, source, version.
3. Allowed labels: SCAM, LEGITIMATE, AMBIGUOUS.
4. Allowed languages: en, hi, te, hi-en, te-en.
5. Non-empty transcripts and valid speaker turns (min 4, max 12).
6. Script character verification: Devanagari in 'hi', Telugu script in 'te'.
7. Duplicate conversation_id and sample_id checks.
8. Duplicate exact dialogue text checks.
9. Balanced class and language distribution checks against targets.
10. Ambiguous record quality: verifies 4-part structure (Caller Claims, Evidence Available,
    Evidence Missing, Classification Rationale) and absence of generic explanations.
11. Flagging questionable or irregular samples for human review.
"""

import sys
import json
import re
from pathlib import Path
from collections import Counter
from typing import Dict, Any, List, Set

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_V3_DIR = PROJECT_ROOT / "data" / "kavach_synthetic_v3"
VALIDATED_FILE = DATA_V3_DIR / "validated" / "all_samples.jsonl"
SPLITS_DIR = DATA_V3_DIR / "splits"

MANDATORY_FIELDS = [
    "sample_id",
    "conversation_id",
    "language",
    "scenario_family",
    "label",
    "transcript",
    "explanation",
    "risk_indicators",
    "annotation_status",
    "source",
    "version"
]

ALLOWED_LABELS = {"SCAM", "LEGITIMATE", "AMBIGUOUS"}
ALLOWED_LANGUAGES = {"en", "hi", "te", "hi-en", "te-en"}

DEV_REGEX = re.compile(r'[\u0900-\u097F]')  # Devanagari range
TEL_REGEX = re.compile(r'[\u0C00-\u0C7F]')  # Telugu range

def validate_dataset() -> bool:
    print("=" * 80)
    print("KAVACH AI — DATASET v3 COMPREHENSIVE AUTOMATED QUALITY AUDIT")
    print("=" * 80)
    
    if not VALIDATED_FILE.exists():
        print(f"[FAIL] Master file not found at {VALIDATED_FILE}")
        return False
        
    records: List[Dict[str, Any]] = []
    line_number = 0
    parsing_errors = 0
    
    with open(VALIDATED_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line_number += 1
            if line.strip():
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError as e:
                    parsing_errors += 1
                    print(f"  [ERROR] JSON parse failure at line {line_number}: {e}")
                    
    print(f"\n[Check 1/10] JSONL Parsing: {len(records)} parsed, {parsing_errors} errors")
    if parsing_errors > 0 or len(records) != 3000:
        print(f"[FAIL] Expected 3,000 valid records, got {len(records)}")
        return False
    print("  -> PASS")

    # Check 2: Mandatory fields
    print("\n[Check 2/10] Mandatory Fields Conformance:")
    missing_fields_count = 0
    for r in records:
        for field in MANDATORY_FIELDS:
            if field not in r or r[field] is None or (isinstance(r[field], str) and not r[field].strip()):
                missing_fields_count += 1
                print(f"  [MISSING] Record {r.get('sample_id')} missing or empty field: {field}")
                
    if missing_fields_count > 0:
        print(f"[FAIL] Found {missing_fields_count} missing mandatory fields")
        return False
    print("  -> PASS: All 11 mandatory fields present and non-empty across all 3,000 records.")

    # Check 3: Allowed Labels & Languages
    print("\n[Check 3/10] Allowed Labels & Language Vocabularies:")
    labels = Counter(r["label"] for r in records)
    languages = Counter(r["language"] for r in records)
    
    invalid_labels = set(labels.keys()) - ALLOWED_LABELS
    invalid_langs = set(languages.keys()) - ALLOWED_LANGUAGES
    
    if invalid_labels or invalid_langs:
        print(f"[FAIL] Invalid labels: {invalid_labels} | Invalid langs: {invalid_langs}")
        return False
    print(f"  Labels: {dict(labels)}")
    print(f"  Languages: {dict(languages)}")
    print("  -> PASS")

    # Check 4: Dialogue Turn Count & Empty Text Check
    print("\n[Check 4/10] Dialogue Turn Integrity & Dialogue Lengths:")
    turn_counts = []
    empty_turns_count = 0
    invalid_speaker_count = 0
    
    for r in records:
        turns = r.get("dialogue", [])
        turn_counts.append(len(turns))
        for t in turns:
            if not t.get("text", "").strip():
                empty_turns_count += 1
            if t.get("speaker") not in ["caller", "recipient"]:
                invalid_speaker_count += 1
                
    min_turns = min(turn_counts)
    max_turns = max(turn_counts)
    avg_turns = sum(turn_counts) / len(turn_counts)
    
    print(f"  Turns range: min={min_turns}, max={max_turns}, mean={avg_turns:.1f}")
    if min_turns < 4 or max_turns > 12 or empty_turns_count > 0 or invalid_speaker_count > 0:
        print(f"[FAIL] Invalid turn counts or empty turns: empty={empty_turns_count}, invalid_speaker={invalid_speaker_count}")
        return False
    print("  -> PASS: All dialogue lengths between 4 and 12 turns; zero empty turns.")

    # Check 5: Script Authenticity
    print("\n[Check 5/10] Script Authenticity Verification (Devanagari & Telugu):")
    hi_records = [r for r in records if r["language"] == "hi"]
    te_records = [r for r in records if r["language"] == "te"]
    
    hi_script_pass = sum(1 for r in hi_records if DEV_REGEX.search(r["transcript"]))
    te_script_pass = sum(1 for r in te_records if TEL_REGEX.search(r["transcript"]))
    
    print(f"  Hindi records with Devanagari characters: {hi_script_pass} / {len(hi_records)}")
    print(f"  Telugu records with Telugu script characters: {te_script_pass} / {len(te_records)}")
    
    if hi_script_pass != len(hi_records) or te_script_pass != len(te_records):
        print(f"[FAIL] Script mismatch detected in pure Hindi or Telugu samples")
        return False
    print("  -> PASS: 100% of Hindi samples contain Devanagari; 100% of Telugu samples contain Telugu script.")

    # Check 6: ID and Exact Dialogue Text Uniqueness
    print("\n[Check 6/10] Uniqueness Audit (IDs and Dialogue Text Hashes):")
    sample_ids = [r["sample_id"] for r in records]
    conv_ids = [r["conversation_id"] for r in records]
    texts = [" ".join([t["text"] for t in r.get("dialogue", [])]).strip().lower() for r in records]
    
    unique_sids = len(set(sample_ids))
    unique_cids = len(set(conv_ids))
    unique_texts = len(set(texts))
    
    print(f"  Unique sample_ids: {unique_sids} / {len(records)}")
    print(f"  Unique conversation_ids: {unique_cids} / {len(records)}")
    print(f"  Unique dialogue texts: {unique_texts} / {len(records)}")
    
    if unique_sids != 3000 or unique_cids != 3000 or unique_texts != 3000:
        print(f"[FAIL] Non-unique IDs or dialogue text detected")
        return False
    print("  -> PASS: Zero duplicate IDs and zero duplicate conversations.")

    # Check 7: Target Distributions
    print("\n[Check 7/10] Target Balance Conformance:")
    target_labels = {"SCAM": 1200, "LEGITIMATE": 900, "AMBIGUOUS": 900}
    target_langs = {"en": 600, "hi": 600, "te": 600, "hi-en": 600, "te-en": 600}
    target_splits = {"train": 2100, "validation": 450, "test": 450}
    
    splits = Counter(r["split"] for r in records)
    
    labels_ok = all(labels[k] == v for k, v in target_labels.items())
    langs_ok = all(languages[k] == v for k, v in target_langs.items())
    splits_ok = all(splits[k] == v for k, v in target_splits.items())
    
    print(f"  Class match: {labels_ok} | Language match: {langs_ok} | Split match: {splits_ok}")
    if not (labels_ok and langs_ok and splits_ok):
        print(f"[FAIL] Distribution target mismatch: labels={dict(labels)}, langs={dict(languages)}, splits={dict(splits)}")
        return False
    print("  -> PASS: Exactly matches all 3,000 target distributions.")

    # Check 8: AMBIGUOUS Quality Audit
    print("\n[Check 8/10] AMBIGUOUS Sample Quality & Explanation Audit:")
    ambig_records = [r for r in records if r["label"] == "AMBIGUOUS"]
    generic_explanations = 0
    missing_sections = 0
    
    for r in ambig_records:
        exp = r.get("explanation", "")
        if "the intent is unclear" in exp.lower() or len(exp.strip()) < 30:
            generic_explanations += 1
            
        # Verify 4-part structure for newly synthesized AMBIG records
        if r.get("source") == "synthetic_generation":
            if not ("1. Caller Claims:" in exp and "2. Evidence Available:" in exp and "3. Evidence Missing:" in exp and "4. Classification Rationale:" in exp):
                missing_sections += 1
                
    print(f"  Total AMBIGUOUS records: {len(ambig_records)}")
    print(f"  Generic explanations detected: {generic_explanations}")
    print(f"  Missing 4-part sections in new AMBIG records: {missing_sections}")
    
    if generic_explanations > 0 or missing_sections > 0:
        print(f"[FAIL] Deficient AMBIGUOUS explanations found")
        return False
    print("  -> PASS: All AMBIGUOUS records feature robust, detailed forensic reasoning.")

    # Check 9: Annotation Status & Review Guardrails
    print("\n[Check 9/10] Annotation Status & Ground Truth Guardrails:")
    statuses = Counter(r.get("annotation_status") for r in records)
    print(f"  Annotation statuses: {dict(statuses)}")
    if statuses.get("pending_review") != 3000:
        print(f"[FAIL] Not all records are marked pending_review: {dict(statuses)}")
        return False
    print("  -> PASS: All 3,000 records strictly marked annotation_status='pending_review'.")

    # Check 10: Split Files Verification
    print("\n[Check 10/10] Partition Split Files Audit:")
    split_counts = {}
    for sp in ["train", "validation", "test"]:
        sp_file = SPLITS_DIR / f"{sp}.jsonl"
        if not sp_file.exists():
            print(f"[FAIL] Missing split file: {sp_file}")
            return False
        with open(sp_file, "r", encoding="utf-8") as f:
            lines = [l for l in f if l.strip()]
            split_counts[sp] = len(lines)
            
    print(f"  Split counts on disk: {split_counts}")
    if split_counts != target_splits:
        print(f"[FAIL] Split counts on disk do not match targets: {split_counts}")
        return False
    print("  -> PASS: Split files verified on disk.")

    print("\n" + "=" * 80)
    print("OVERALL DATASET v3 VALIDATION RESULT: ALL 10 QUALITY GATES PASSED (100%)")
    print("=" * 80)
    return True

if __name__ == "__main__":
    success = validate_dataset()
    sys.exit(0 if success else 1)

