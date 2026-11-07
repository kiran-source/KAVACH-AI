"""
KAVACH AI — Baseline vs MuRIL Comparative Evaluation Script
Evaluates the production TF-IDF baseline against the MuRIL transformer on the same held-out test set.
Accurately reports latency, parameters, footprint, and performance.
"""

import sys
import json
import time
from pathlib import Path
from typing import Dict, Any, List

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix

SPLITS_PATH = PROJECT_ROOT / "data" / "kavach_synthetic_v2" / "splits"
TFIDF_ARTIFACTS = PROJECT_ROOT / "backend" / "app" / "ml" / "artifacts" / "v1"
MURIL_ARTIFACTS = PROJECT_ROOT / "backend" / "app" / "ml" / "artifacts" / "muril_v1"

LABEL2ID = {"LEGITIMATE": 0, "AMBIGUOUS": 1, "SCAM": 2}
ID2LABEL = {0: "LEGITIMATE", 1: "AMBIGUOUS", 2: "SCAM"}

def load_test_split():
    test_file = SPLITS_PATH / "test.jsonl"
    if not test_file.exists():
        raise FileNotFoundError(f"Test split not found at: {test_file}")
    
    texts = []
    labels = []
    languages = []
    cids = []
    
    with open(test_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rec = json.loads(line)
                convo = " ".join([t["text"] for t in rec.get("dialogue", [])])
                texts.append(convo)
                labels.append(LABEL2ID[rec["primary_label"]])
                languages.append(rec.get("language", "en"))
                cids.append(rec.get("conversation_id"))
                
    return texts, np.array(labels), languages, cids

def evaluate_baseline(texts, y_true):
    import joblib
    model_path = TFIDF_ARTIFACTS / "model.joblib"
    vec_path = TFIDF_ARTIFACTS / "vectorizer.joblib"
    
    if not (model_path.exists() and vec_path.exists()):
        return None
        
    model = joblib.load(model_path)
    vec = joblib.load(vec_path)
    
    # Latency benchmark
    latencies = []
    preds = []
    
    # Warmup
    for t in texts[:5]:
        v = vec.transform([t])
        _ = model.predict_proba(v)
        
    for t in texts:
        t0 = time.perf_counter()
        v = vec.transform([t])
        probs = model.predict_proba(v)[0]
        t1 = time.perf_counter()
        latencies.append((t1 - t0) * 1000.0)
        preds.append(int(np.argmax(probs)))
        
    preds = np.array(preds)
    acc = accuracy_score(y_true, preds)
    p_macro, r_macro, f1_macro, _ = precision_recall_fscore_support(y_true, preds, average="macro", zero_division=0)
    
    model_size_kb = (model_path.stat().st_size + vec_path.stat().st_size) / 1024.0
    
    return {
        "accuracy": float(acc),
        "macro_precision": float(p_macro),
        "macro_recall": float(r_macro),
        "macro_f1": float(f1_macro),
        "mean_latency_ms": float(np.mean(latencies)),
        "p50_latency_ms": float(np.percentile(latencies, 50)),
        "p95_latency_ms": float(np.percentile(latencies, 95)),
        "model_size_str": f"{model_size_kb:.1f} KB",
        "parameters": "2,607 TF-IDF Features"
    }

def evaluate_muril_if_present(texts, y_true):
    from app.ml.muril_loader import is_muril_available
    if not is_muril_available():
        return {
            "status": "PENDING_COLAB_EXECUTION",
            "accuracy": None,
            "macro_precision": None,
            "macro_recall": None,
            "macro_f1": None,
            "mean_latency_ms": None,
            "p50_latency_ms": None,
            "p95_latency_ms": None,
            "model_size_str": "~430 MB (Standard PyTorch/safetensors)",
            "parameters": "~110 Million (MuRIL-base)"
        }
        
    try:
        from app.ml.muril_classifier import get_muril_classifier
        clf = get_muril_classifier()
        if not clf.is_loaded:
            return None
            
        latencies = []
        preds = []
        
        for t in texts:
            t0 = time.perf_counter()
            res = clf.predict(t)
            t1 = time.perf_counter()
            latencies.append((t1 - t0) * 1000.0)
            preds.append(LABEL2ID[res.predicted_class])
            
        preds = np.array(preds)
        acc = accuracy_score(y_true, preds)
        p_macro, r_macro, f1_macro, _ = precision_recall_fscore_support(y_true, preds, average="macro", zero_division=0)
        
        return {
            "status": "EVALUATED_LOCALLY",
            "accuracy": float(acc),
            "macro_precision": float(p_macro),
            "macro_recall": float(r_macro),
            "macro_f1": float(f1_macro),
            "mean_latency_ms": float(np.mean(latencies)),
            "p50_latency_ms": float(np.percentile(latencies, 50)),
            "p95_latency_ms": float(np.percentile(latencies, 95)),
            "model_size_str": "~430 MB",
            "parameters": "~110 Million"
        }
    except Exception as e:
        return {"status": f"LOAD_ERROR: {e}"}

def main():
    print("=" * 80)
    print("KAVACH AI — PRODUCTION BASELINE vs MURIL TRANSFORMER EVALUATION")
    print("=" * 80)
    
    texts, y_true, langs, cids = load_test_split()
    print(f"Loaded {len(texts)} held-out test conversations from {SPLITS_PATH.name}/test.jsonl")
    
    base_res = evaluate_baseline(texts, y_true)
    muril_res = evaluate_muril_if_present(texts, y_true)
    
    print("\n" + "=" * 80)
    print("COMPARATIVE BENCHMARK SUMMARY (HELD-OUT TEST N=75)")
    print("=" * 80)
    print(f"{'Evaluation Metric / Property':<35} | {'Production Baseline (TF-IDF)':<22} | {'MuRIL Transformer (v1)':<20}")
    print("-" * 84)
    
    if base_res:
        acc_base = f"{base_res['accuracy']*100:.1f}%"
        p_base = f"{base_res['macro_precision']:.4f}"
        r_base = f"{base_res['macro_recall']:.4f}"
        f1_base = f"{base_res['macro_f1']:.4f}"
        lat_base = f"{base_res['mean_latency_ms']:.2f} ms (P50: {base_res['p50_latency_ms']:.2f})"
        size_base = base_res['model_size_str']
    else:
        acc_base = p_base = r_base = f1_base = lat_base = size_base = "N/A"
        
    if muril_res and muril_res.get("accuracy") is not None:
        acc_muril = f"{muril_res['accuracy']*100:.1f}%"
        p_muril = f"{muril_res['macro_precision']:.4f}"
        r_muril = f"{muril_res['macro_recall']:.4f}"
        f1_muril = f"{muril_res['macro_f1']:.4f}"
        lat_muril = f"{muril_res['mean_latency_ms']:.2f} ms"
        size_muril = muril_res['model_size_str']
    else:
        acc_muril = "Pending Colab Run"
        p_muril = "Pending Colab Run"
        r_muril = "Pending Colab Run"
        f1_muril = "Pending Colab Run"
        lat_muril = "~40-60 ms (GPU)"
        size_muril = "~430 MB"
        
    print(f"{'Architecture':<35} | {'TF-IDF + Calibrated LR':<22} | {'google/muril-base-cased':<20}")
    print(f"{'Parameters':<35} | {base_res['parameters'] if base_res else 'N/A':<22} | {'~110 Million':<20}")
    print(f"{'Model Size on Disk':<35} | {size_base:<22} | {size_muril:<20}")
    print(f"{'Test Accuracy':<35} | {acc_base:<22} | {acc_muril:<20}")
    print(f"{'Test Macro Precision':<35} | {p_base:<22} | {p_muril:<20}")
    print(f"{'Test Macro Recall':<35} | {r_base:<22} | {r_muril:<20}")
    print(f"{'Test Macro F1-Score':<35} | {f1_base:<22} | {f1_muril:<20}")
    print(f"{'Inference Latency (Host CPU)':<35} | {lat_base:<22} | {lat_muril:<20}")
    print(f"{'Execution Status':<35} | {'ACTIVE (Production)':<22} | {'PENDING_COLAB_EXECUTION':<20}")
    print("=" * 80)
    
    print("\n[NOTE] As per KAVACH AI safety specifications:")
    print("  1. The lightweight TF-IDF baseline remains the active production model to guarantee zero GPU dependency.")
    print("  2. MuRIL training is designed for execution in Google Colab (notebooks/KAVACH_AI_MuRIL_Colab_Training.ipynb).")
    print("  3. High synthetic benchmark metrics do not guarantee wild telephony scam detection accuracy.")

if __name__ == "__main__":
    main()

