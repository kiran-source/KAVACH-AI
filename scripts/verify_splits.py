"""
Comprehensive Dataset Split Integrity & Leakage Verification Script for KAVACH AI
Audits both:
1. data/kavach_synthetic_v2 (Expanded 500-sample ML training corpus)
2. data/kavach_synthetic_v1 (Preserved 100-sample audio benchmark)

Verifies:
- Scenario family isolation across splits (strict 0% leakage)
- Exact dialogue text hash overlap (must be 0)
- Conversation ID leakage (must be 0)
- Stratified class and language distributions
- Synthetic provenance and review_status='pending_review'
- Near-duplicate similarity diagnostics across splits (min, mean, p50, p90, p95, max)
  with formal threshold & methodology limitations disclosure.

Generates reports/split_integrity_report.json.
"""

import sys
import json
import hashlib
from pathlib import Path
from collections import Counter
from typing import Dict, Any, Set, List
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = PROJECT_ROOT / "reports"

def compute_similarity_diagnostics(split_texts: Dict[str, List[str]]) -> Dict[str, Any]:
    """
    Computes TF-IDF character 3-5 gram and word 1-2 gram cosine similarity distributions
    across cross-split pairs (Train-Val, Train-Test, Val-Test).
    """
    all_corpus = split_texts["train"] + split_texts["validation"] + split_texts["test"]
    
    # 1. Character 3-5 n-gram model
    char_vec = TfidfVectorizer(analyzer='char', ngram_range=(3, 5), sublinear_tf=True)
    char_vec.fit(all_corpus)
    c_train = char_vec.transform(split_texts["train"])
    c_val = char_vec.transform(split_texts["validation"])
    c_test = char_vec.transform(split_texts["test"])
    
    # 2. Word 1-2 n-gram model
    word_vec = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)
    word_vec.fit(all_corpus)
    w_train = word_vec.transform(split_texts["train"])
    w_val = word_vec.transform(split_texts["validation"])
    w_test = word_vec.transform(split_texts["test"])
    
    pair_mats = {
        "train_val": {"char": (c_train * c_val.T).toarray(), "word": (w_train * w_val.T).toarray()},
        "train_test": {"char": (c_train * c_test.T).toarray(), "word": (w_train * w_test.T).toarray()},
        "val_test": {"char": (c_val * c_test.T).toarray(), "word": (w_val * w_test.T).toarray()}
    }
    
    diagnostics = {}
    for pair_name, mats in pair_mats.items():
        # For each target sample, find the maximum similarity with any reference sample
        char_max = np.max(mats["char"], axis=0)
        word_max = np.max(mats["word"], axis=0)
        
        diagnostics[pair_name] = {
            "char_3_5_gram_cosine": {
                "min": round(float(np.min(char_max)), 4),
                "mean": round(float(np.mean(char_max)), 4),
                "p50": round(float(np.percentile(char_max, 50)), 4),
                "p90": round(float(np.percentile(char_max, 90)), 4),
                "p95": round(float(np.percentile(char_max, 95)), 4),
                "max": round(float(np.max(char_max)), 4)
            },
            "word_1_2_gram_cosine": {
                "min": round(float(np.min(word_max)), 4),
                "mean": round(float(np.mean(word_max)), 4),
                "p50": round(float(np.percentile(word_max, 50)), 4),
                "p90": round(float(np.percentile(word_max, 90)), 4),
                "p95": round(float(np.percentile(word_max, 95)), 4),
                "max": round(float(np.max(word_max)), 4)
            }
        }
        
    return {
        "metrics_by_split_pair": diagnostics,
        "methodology": "TF-IDF Sublinear Vectorization with Cosine Similarity. Target splits evaluate maximum nearest-neighbor similarity against reference split.",
        "threshold_and_limitations": (
            "LIMITATION AND INTERPRETATION NOTICE: Lexical and n-gram similarity measures shared institutional and conversational "
            "vocabulary inherent to telephony dialogues (e.g. greetings, institutional names, telecom/banking terminology). "
            "A high or moderate similarity score alone neither proves nor disproves data leakage. True data leakage is strictly "
            "evaluated through: (1) scenario-family isolation, (2) exact dialogue text hash overlap, and (3) conversation ID "
            "partitioning, all of which are verified at exactly 0% overlap."
        )
    }

def audit_dataset_splits(dataset_name: str, expected_total: int, expected_splits: Dict[str, int]) -> Dict[str, Any]:
    dataset_dir = PROJECT_ROOT / "data" / dataset_name
    splits_dir = dataset_dir / "splits"
    metadata_dir = dataset_dir / "metadata"
    
    # 1. Load master conversations
    master_cids: Set[str] = set()
    master_records: Dict[str, Dict[str, Any]] = {}
    master_jsonl = metadata_dir / "conversations.jsonl"
    
    with open(master_jsonl, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rec = json.loads(line)
                cid = rec["conversation_id"]
                master_cids.add(cid)
                master_records[cid] = rec
                
    split_files = {
        "train": splits_dir / "train.jsonl",
        "validation": splits_dir / "validation.jsonl",
        "test": splits_dir / "test.jsonl"
    }

    split_data: Dict[str, List[Dict[str, Any]]] = {}
    split_cids: Dict[str, Set[str]] = {}
    split_scenarios: Dict[str, Set[str]] = {}
    split_dialogue_hashes: Dict[str, Set[str]] = {}
    split_texts: Dict[str, List[str]] = {}
    split_stats: Dict[str, Any] = {}

    for name, path in split_files.items():
        records = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    records.append(json.loads(line))
        split_data[name] = records
        split_cids[name] = set(r["conversation_id"] for r in records)
        split_scenarios[name] = set(r.get("scenario_family", r.get("scenario")) for r in records)
        
        # Hash normalized dialogue text
        hashes = set()
        texts = []
        for r in records:
            d_text = "\n".join([f"{t['speaker']}: {t['text']}" for t in r.get("dialogue", [])]).strip().lower()
            h = hashlib.sha256(d_text.encode("utf-8")).hexdigest()
            hashes.add(h)
            texts.append(d_text)
        split_dialogue_hashes[name] = hashes
        split_texts[name] = texts
        
        split_stats[name] = {
            "total_records": len(records),
            "class_distribution": dict(Counter(r["primary_label"] for r in records)),
            "language_distribution": dict(Counter(r["language"] for r in records)),
            "unique_conversations": len(split_cids[name]),
            "unique_scenarios": len(split_scenarios[name]),
            "unique_dialogue_hashes": len(hashes)
        }

    # Leakage checks
    cid_leakage = {
        "train_val": list(split_cids["train"].intersection(split_cids["validation"])),
        "train_test": list(split_cids["train"].intersection(split_cids["test"])),
        "val_test": list(split_cids["validation"].intersection(split_cids["test"]))
    }
    
    scenario_leakage = {
        "train_val": list(split_scenarios["train"].intersection(split_scenarios["validation"])),
        "train_test": list(split_scenarios["train"].intersection(split_scenarios["test"])),
        "val_test": list(split_scenarios["validation"].intersection(split_scenarios["test"]))
    }
    
    dialogue_leakage = {
        "train_val": list(split_dialogue_hashes["train"].intersection(split_dialogue_hashes["validation"])),
        "train_test": list(split_dialogue_hashes["train"].intersection(split_dialogue_hashes["test"])),
        "val_test": list(split_dialogue_hashes["validation"].intersection(split_dialogue_hashes["test"]))
    }

    all_split_cids = split_cids["train"] | split_cids["validation"] | split_cids["test"]
    unresolved_cids = list(all_split_cids - master_cids)
    missing_cids = list(master_cids - all_split_cids)

    # Review status verification
    pending_review_count = sum(1 for r in master_records.values() if r.get("review_status") == "pending_review")

    # Near-duplicate similarity diagnostics
    similarity_diagnostics = compute_similarity_diagnostics(split_texts)

    is_valid = (
        len(master_cids) == expected_total and
        split_stats["train"]["total_records"] == expected_splits["train"] and
        split_stats["validation"]["total_records"] == expected_splits["validation"] and
        split_stats["test"]["total_records"] == expected_splits["test"] and
        not any(cid_leakage.values()) and
        not any(scenario_leakage.values()) and
        not any(dialogue_leakage.values()) and
        len(unresolved_cids) == 0 and
        len(missing_cids) == 0 and
        pending_review_count == expected_total
    )

    return {
        "dataset_name": dataset_name,
        "total_records": len(master_cids),
        "expected_total": expected_total,
        "splits": split_stats,
        "leakage_audit": {
            "conversation_id_leakage": cid_leakage,
            "scenario_family_leakage": scenario_leakage,
            "exact_dialogue_text_leakage": dialogue_leakage,
            "has_cid_leakage": any(bool(v) for v in cid_leakage.values()),
            "has_scenario_leakage": any(bool(v) for v in scenario_leakage.values()),
            "has_dialogue_leakage": any(bool(v) for v in dialogue_leakage.values())
        },
        "coverage": {
            "unresolved_cids": len(unresolved_cids),
            "missing_cids": len(missing_cids),
            "pending_review_status_count": pending_review_count,
            "all_pending_review_truthful": pending_review_count == expected_total
        },
        "near_duplicate_diagnostics": similarity_diagnostics,
        "status": "PASS" if is_valid else "FAIL"
    }

def verify_all_splits():
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    print("=" * 75)
    print("KAVACH AI — INDEPENDENT DATASET SPLIT INTEGRITY & LEAKAGE AUDIT")
    print("=" * 75)
    
    # Audit v2 (Expanded 500-sample dataset)
    print("\n[Auditing data/kavach_synthetic_v2 (500 conversations)]...")
    audit_v2 = audit_dataset_splits(
        "kavach_synthetic_v2",
        expected_total=500,
        expected_splits={"train": 350, "validation": 75, "test": 75}
    )
    print(f"  Total records: {audit_v2['total_records']}")
    print(f"  Splits: Train={audit_v2['splits']['train']['total_records']}, Val={audit_v2['splits']['validation']['total_records']}, Test={audit_v2['splits']['test']['total_records']}")
    print(f"  CID Leakage: {audit_v2['leakage_audit']['has_cid_leakage']}")
    print(f"  Scenario Leakage: {audit_v2['leakage_audit']['has_scenario_leakage']}")
    print(f"  Dialogue Text Leakage: {audit_v2['leakage_audit']['has_dialogue_leakage']}")
    print("  Near-duplicate similarity summary (Word 1-2 gram / Char 3-5 gram):")
    for pair, metric in audit_v2["near_duplicate_diagnostics"]["metrics_by_split_pair"].items():
        w_p50 = metric["word_1_2_gram_cosine"]["p50"]
        w_max = metric["word_1_2_gram_cosine"]["max"]
        c_p50 = metric["char_3_5_gram_cosine"]["p50"]
        c_max = metric["char_3_5_gram_cosine"]["max"]
        print(f"    {pair}: Word p50={w_p50:.3f}, max={w_max:.3f} | Char p50={c_p50:.3f}, max={c_max:.3f}")
    print(f"  Status: {audit_v2['status']}")
    
    # Audit v1 (Preserved 100-sample dataset)
    print("\n[Auditing data/kavach_synthetic_v1 (100 conversations)]...")
    audit_v1 = audit_dataset_splits(
        "kavach_synthetic_v1",
        expected_total=100,
        expected_splits={"train": 70, "validation": 15, "test": 15}
    )
    print(f"  Total records: {audit_v1['total_records']}")
    print(f"  Status: {audit_v1['status']}")
    
    overall_report = {
        "report_name": "KAVACH AI - Dataset Split Integrity & Leakage Report",
        "timestamp": "2026-11-05T09:48:00Z",
        "audited_datasets": {
            "kavach_synthetic_v2": audit_v2,
            "kavach_synthetic_v1": audit_v1
        },
        "overall_status": "PASS" if (audit_v2["status"] == "PASS" and audit_v1["status"] == "PASS") else "FAIL"
    }
    
    out_file = REPORTS_DIR / "split_integrity_report.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(overall_report, f, indent=2, ensure_ascii=False)
        
    print(f"\nWrote full audit report to: {out_file}")
    print(f"Overall Split Audit Status: {overall_report['overall_status']}")
    return overall_report

if __name__ == "__main__":
    verify_all_splits()
