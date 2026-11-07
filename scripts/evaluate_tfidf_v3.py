"""
Comprehensive Evaluation Pipeline for TF-IDF v3 on KAVACH AI Synthetic Dataset v3
Evaluates TF-IDF v3 on the held-out test split (exactly 450 records).
Computes full classification metrics, confusion matrix, per-language breakdown,
and benchmarks CPU latency over 200 iterations.
Also benchmarks the 8-pillar deterministic rule engine on the exact same 450 records.
"""

import sys
import json
import time
from pathlib import Path
from typing import Dict, Any, List, Tuple
from collections import Counter

import joblib
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report, confusion_matrix

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SPLITS_DIR = PROJECT_ROOT / "data" / "kavach_synthetic_v3" / "splits"
TFIDF_V3_DIR = PROJECT_ROOT / "backend" / "app" / "ml" / "artifacts" / "tfidf_v3"
TFIDF_V1_DIR = PROJECT_ROOT / "backend" / "app" / "ml" / "artifacts" / "v1"
REPORTS_DIR = PROJECT_ROOT / "reports"

sys.path.insert(0, str(PROJECT_ROOT / "backend"))
from app.detection.engine import analyze_transcript

LABEL2ID = {"LEGITIMATE": 0, "AMBIGUOUS": 1, "SCAM": 2}
ID2LABEL = {0: "LEGITIMATE", 1: "AMBIGUOUS", 2: "SCAM"}
TARGET_NAMES = ["LEGITIMATE", "AMBIGUOUS", "SCAM"]
LANGUAGES = ["en", "hi", "te", "hi-en", "te-en"]

def load_test_split() -> Tuple[List[str], np.ndarray, List[str], List[str]]:
    test_path = SPLITS_DIR / "test.jsonl"
    texts = []
    labels = []
    languages = []
    cids = []

    with open(test_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            rec = json.loads(line)
            convo = " ".join([turn.get("text", "") for turn in rec.get("dialogue", [])]).strip()
            texts.append(convo)
            labels.append(LABEL2ID[rec["primary_label"]])
            languages.append(rec["language"])
            cids.append(rec["conversation_id"])

    return texts, np.array(labels), languages, cids

def evaluate_rule_engine(texts: List[str], true_labels: np.ndarray, languages: List[str]) -> Dict[str, Any]:
    print("\n--- BENCHMARKING 8-PILLAR RULE ENGINE ON HELD-OUT TEST (N=450) ---")
    rule_preds = []
    for text, lang in zip(texts, languages):
        res = analyze_transcript(text, language_hint=lang)
        score = res.get("risk_score", 0.0)
        # 3-class mapping
        if score >= 40.0:
            pred = LABEL2ID["SCAM"]
        elif score >= 20.0:
            pred = LABEL2ID["AMBIGUOUS"]
        else:
            pred = LABEL2ID["LEGITIMATE"]
        rule_preds.append(pred)

    y_pred = np.array(rule_preds)
    acc = accuracy_score(true_labels, y_pred)
    p_macro, r_macro, f1_macro, _ = precision_recall_fscore_support(true_labels, y_pred, average="macro", zero_division=0)
    cm = confusion_matrix(true_labels, y_pred).tolist()
    rep = classification_report(true_labels, y_pred, target_names=TARGET_NAMES, output_dict=True)

    print(f"Rule Engine Accuracy: {acc*100:.2f}% | Macro F1: {f1_macro:.4f}")
    return {
        "accuracy": round(float(acc), 4),
        "macro_precision": round(float(p_macro), 4),
        "macro_recall": round(float(r_macro), 4),
        "macro_f1": round(float(f1_macro), 4),
        "per_class": {
            k: {
                "precision": round(rep[k]["precision"], 4),
                "recall": round(rep[k]["recall"], 4),
                "f1_score": round(rep[k]["f1-score"], 4),
                "support": rep[k]["support"]
            } for k in TARGET_NAMES
        },
        "confusion_matrix": cm
    }

def run_evaluation():
    print("=" * 80)
    print("KAVACH AI — TF-IDF v3 HELD-OUT TEST EVALUATION (N=450)")
    print("=" * 80)

    # 1. Load Test Split
    texts, y_true, languages, cids = load_test_split()
    total_samples = len(texts)
    print(f"Loaded held-out test split: {total_samples} samples")
    print(f"Class distribution: {dict(Counter(y_true))}")
    print(f"Language distribution: {dict(Counter(languages))}")
    assert total_samples == 450, f"Expected exactly 450 test records, got {total_samples}"

    # 2. Load Model Artifacts
    vec_path = TFIDF_V3_DIR / "vectorizer.joblib"
    model_path = TFIDF_V3_DIR / "model.joblib"
    if not (vec_path.exists() and model_path.exists()):
        raise FileNotFoundError(f"Missing artifacts in {TFIDF_V3_DIR}. Run training first.")

    vectorizer = joblib.load(vec_path)
    model = joblib.load(model_path)
    print(f"Loaded vectorizer and calibrated model from {TFIDF_V3_DIR}")

    # 3. Inference on Held-Out Test Split
    print("\nTransforming test texts and computing calibrated probabilities...")
    X_test = vectorizer.transform(texts)
    y_probs = model.predict_proba(X_test)
    y_preds = np.argmax(y_probs, axis=1)

    # Overall metrics
    acc = accuracy_score(y_true, y_preds)
    p_macro, r_macro, f1_macro, _ = precision_recall_fscore_support(y_true, y_preds, average="macro", zero_division=0)
    p_weighted, r_weighted, f1_weighted, _ = precision_recall_fscore_support(y_true, y_preds, average="weighted", zero_division=0)
    cm = confusion_matrix(y_true, y_preds).tolist()
    clf_rep = classification_report(y_true, y_preds, target_names=TARGET_NAMES, output_dict=True)

    print("\n--- OVERALL TEST PERFORMANCE (N=450) ---")
    print(f"Accuracy:         {acc*100:.2f}%")
    print(f"Macro Precision:  {p_macro:.4f}")
    print(f"Macro Recall:     {r_macro:.4f}")
    print(f"Macro F1:         {f1_macro:.4f}")
    print(f"Weighted F1:      {f1_weighted:.4f}")

    print("\nPer-Class Classification Report:")
    print(classification_report(y_true, y_preds, target_names=TARGET_NAMES, digits=4))
    print(f"Confusion Matrix (Rows: Actual, Cols: Pred):\n{np.array(cm)}")

    # 4. Per-Language Breakdown
    print("\n--- PER-LANGUAGE PERFORMANCE BREAKDOWN (90 samples per language) ---")
    lang_metrics = {}
    for lang in LANGUAGES:
        idx = [i for i, l in enumerate(languages) if l == lang]
        sub_y_true = y_true[idx]
        sub_y_preds = y_preds[idx]

        sub_acc = accuracy_score(sub_y_true, sub_y_preds)
        sub_p, sub_r, sub_f1, _ = precision_recall_fscore_support(sub_y_true, sub_y_preds, average="macro", zero_division=0)
        sub_rep = classification_report(sub_y_true, sub_y_preds, target_names=TARGET_NAMES, output_dict=True)

        lang_metrics[lang] = {
            "samples_count": len(idx),
            "accuracy": round(float(sub_acc), 4),
            "macro_precision": round(float(sub_p), 4),
            "macro_recall": round(float(sub_r), 4),
            "macro_f1": round(float(sub_f1), 4),
            "per_class_f1": {
                k: round(sub_rep[k]["f1-score"], 4) for k in TARGET_NAMES
            }
        }
        print(f"Language [{lang:5s}]: Accuracy={sub_acc*100:5.1f}% | Macro F1={sub_f1:.4f} | Recall: SCAM={sub_rep['SCAM']['recall']:.2f}, AMBIG={sub_rep['AMBIGUOUS']['recall']:.2f}, LEGIT={sub_rep['LEGITIMATE']['recall']:.2f}")

    # 5. Deterministic Rule Engine Benchmark on same 450 records
    rule_results = evaluate_rule_engine(texts, y_true, languages)

    # 6. CPU Latency Benchmark over 200 iterations
    print("\n--- REAL CPU LATENCY BENCHMARK (200 iterations) ---")
    sample_text = texts[0]
    # Warmup
    for _ in range(20):
        _ = model.predict_proba(vectorizer.transform([sample_text]))

    latencies_ms = []
    for _ in range(200):
        t0 = time.perf_counter()
        v = vectorizer.transform([sample_text])
        _ = model.predict_proba(v)
        latencies_ms.append((time.perf_counter() - t0) * 1000.0)

    mean_lat = float(np.mean(latencies_ms))
    p50_lat = float(np.median(latencies_ms))
    p95_lat = float(np.percentile(latencies_ms, 95))
    throughput = 1000.0 / mean_lat if mean_lat > 0 else 0.0

    print(f"Mean Latency: {mean_lat:.2f} ms")
    print(f"P50  Latency: {p50_lat:.2f} ms")
    print(f"P95  Latency: {p95_lat:.2f} ms")
    print(f"Throughput:   {throughput:.1f} inferences/sec")

    # Disk footprint
    vec_size_kb = vec_path.stat().st_size / 1024.0
    model_size_kb = model_path.stat().st_size / 1024.0
    total_size_kb = vec_size_kb + model_size_kb
    print(f"Artifact Disk Size: Vectorizer={vec_size_kb:.1f} KB, Model={model_size_kb:.1f} KB, Total={total_size_kb:.1f} KB")

    # 7. Compile and save evaluation report
    report_data = {
        "evaluation_name": "KAVACH-AI TF-IDF v3 Held-Out Test Evaluation",
        "dataset": "data/kavach_synthetic_v3/splits/test.jsonl",
        "dataset_sample_count": total_samples,
        "evaluation_timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "model_version": "tfidf_v3.0",
        "test_metrics": {
            "accuracy": round(float(acc), 4),
            "macro_precision": round(float(p_macro), 4),
            "macro_recall": round(float(r_macro), 4),
            "macro_f1": round(float(f1_macro), 4),
            "weighted_f1": round(float(f1_weighted), 4),
            "per_class": {
                name: {
                    "precision": round(clf_rep[name]["precision"], 4),
                    "recall": round(clf_rep[name]["recall"], 4),
                    "f1_score": round(clf_rep[name]["f1-score"], 4),
                    "support": clf_rep[name]["support"]
                } for name in TARGET_NAMES
            },
            "confusion_matrix": cm,
            "per_language_metrics": lang_metrics
        },
        "rule_engine_benchmark": rule_results,
        "cpu_latency_benchmark_ms": {
            "iterations": 200,
            "mean": round(mean_lat, 2),
            "p50": round(p50_lat, 2),
            "p95": round(p95_lat, 2),
            "throughput_inferences_per_sec": round(throughput, 1)
        },
        "disk_footprint_kb": {
            "vectorizer": round(vec_size_kb, 2),
            "model": round(model_size_kb, 2),
            "total": round(total_size_kb, 2)
        },
        "honest_disclosures": {
            "synthetic_corpus_scope": "Benchmark metrics reflect performance on synthetic domain scenarios; wild telephony calls with 8kHz codec compression and background noise require field validation.",
            "annotation_status": "All 450 test records carry annotation_status: pending_review.",
            "baseline_comparability": "Historical TF-IDF v2 evaluated on 75 samples (v2 test) is non-comparable to v3 (450 samples)."
        }
    }

    out_file = REPORTS_DIR / "tfidf_v3_evaluation_report.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)

    print(f"\n[DONE] Full evaluation results written to: {out_file}")
    return report_data

if __name__ == "__main__":
    run_evaluation()

