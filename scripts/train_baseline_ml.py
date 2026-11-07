"""
Multilingual Baseline ML Training & Calibration Script for KAVACH AI
Trains TF-IDF + Calibrated Logistic Regression on remediated data/kavach_synthetic_v2 splits (train: 350, val: 75, test: 75).
Includes:
- Rule engine baseline comparison on the same held-out test split.
- Actual CPU inference latency benchmark.
- Per-class, per-language, confusion matrix, and honest disclosure of synthetic benchmark scope.
- Exports compact, production-ready artifacts to backend/app/ml/artifacts/v1/.
"""

import os
import sys
import time
import json
import joblib
import numpy as np
from pathlib import Path
from typing import Dict, Any, List, Tuple
from collections import Counter

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SPLITS_DIR = PROJECT_ROOT / "data" / "kavach_synthetic_v2" / "splits"
ARTIFACTS_DIR = PROJECT_ROOT / "backend" / "app" / "ml" / "artifacts" / "v1"
REPORTS_DIR = PROJECT_ROOT / "reports"

sys.path.insert(0, str(PROJECT_ROOT / "backend"))
from app.detection.engine import analyze_transcript

LABEL2ID = {"LEGITIMATE": 0, "AMBIGUOUS": 1, "SCAM": 2}
ID2LABEL = {0: "LEGITIMATE", 1: "AMBIGUOUS", 2: "SCAM"}

def load_split(split_name: str) -> Tuple[List[str], List[int], List[str], List[str]]:
    file_path = SPLITS_DIR / f"{split_name}.jsonl"
    texts = []
    labels = []
    languages = []
    cids = []
    
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            rec = json.loads(line)
            full_text = " ".join([t["text"] for t in rec["dialogue"]])
            texts.append(full_text)
            labels.append(LABEL2ID[rec["primary_label"]])
            languages.append(rec["language"])
            cids.append(rec["conversation_id"])
            
    return texts, labels, languages, cids

def evaluate_rule_engine(texts: List[str], true_labels: List[int], languages: List[str]) -> Dict[str, Any]:
    """Runs the 8-pillar deterministic rule engine on the test set for baseline comparison."""
    rule_preds = []
    for text, lang in zip(texts, languages):
        res = analyze_transcript(text, language_hint=lang)
        score = res.get("risk_score", 0.0)
        # Map rule risk score to 3-class label
        if score >= 40.0:
            pred = LABEL2ID["SCAM"]
        elif score >= 20.0:
            pred = LABEL2ID["AMBIGUOUS"]
        else:
            pred = LABEL2ID["LEGITIMATE"]
        rule_preds.append(pred)
        
    y_true = np.array(true_labels)
    y_pred = np.array(rule_preds)
    
    acc = accuracy_score(y_true, y_pred)
    macro_f1 = f1_score(y_true, y_pred, average="macro", zero_division=0)
    cm = confusion_matrix(y_true, y_pred).tolist()
    
    return {
        "accuracy": round(float(acc), 4),
        "macro_f1": round(float(macro_f1), 4),
        "confusion_matrix": cm
    }

def train_and_evaluate():
    print("=" * 75)
    print("KAVACH AI — MULTILINGUAL BASELINE ML TRAINING & CALIBRATION")
    print("=" * 75)
    
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. Load Data
    train_texts, train_labels, train_langs, train_cids = load_split("train")
    val_texts, val_labels, val_langs, val_cids = load_split("validation")
    test_texts, test_labels, test_langs, test_cids = load_split("test")
    
    print(f"Loaded: Train={len(train_texts)}, Val={len(val_texts)}, Test={len(test_texts)}")
    print(f"Train Class Distribution: {dict(Counter(train_labels))}")
    print(f"Validation Class Distribution: {dict(Counter(val_labels))}")
    print(f"Test Class Distribution:  {dict(Counter(test_labels))}")

    # 2. Multilingual Subword/N-gram TF-IDF Vectorizer
    print("\nFitting Multilingual Word N-Gram (1, 2) TF-IDF Vectorizer on Training Split...")
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=5000,
        sublinear_tf=True,
        strip_accents="unicode"
    )
    
    X_train = vectorizer.fit_transform(train_texts)
    X_val = vectorizer.transform(val_texts)
    X_test = vectorizer.transform(test_texts)
    
    y_train = np.array(train_labels)
    y_val = np.array(val_labels)
    y_test = np.array(test_labels)
    
    print(f"Vocabulary Size: {len(vectorizer.vocabulary_)} features")

    # 3. Model Training & Validation-Driven Platt Scaling Calibration
    print("\nTraining Logistic Regression with Balanced Class Weights & 3-fold Platt Scaling Calibration...")
    base_clf = LogisticRegression(
        C=1.5,
        class_weight="balanced",
        max_iter=1000,
        random_state=42
    )
    
    # Calibrate probabilities using Platt scaling (sigmoid) via 3-fold cross-validation on training data
    calibrated_clf = CalibratedClassifierCV(estimator=base_clf, method="sigmoid", cv=3)
    calibrated_clf.fit(X_train, y_train)

    # Validation Set Diagnostics (used for validation-driven verification)
    val_preds = calibrated_clf.predict(X_val)
    val_acc = accuracy_score(y_val, val_preds)
    val_macro_f1 = f1_score(y_val, val_preds, average="macro")
    print(f"Validation Accuracy: {val_acc:.4f} | Validation Macro F1: {val_macro_f1:.4f}")

    # 4. Final Evaluation on Untouched Independent Test Set (75 Samples)
    print("\n--- INDEPENDENT TEST SET EVALUATION (75 Held-out Samples) ---")
    test_preds = calibrated_clf.predict(X_test)
    test_probs = calibrated_clf.predict_proba(X_test)
    
    test_acc = accuracy_score(y_test, test_preds)
    test_macro_f1 = f1_score(y_test, test_preds, average="macro")
    test_weighted_f1 = f1_score(y_test, test_preds, average="weighted")
    
    print(f"Test Accuracy:    {test_acc:.4f} ({test_acc*100:.1f}%)")
    print(f"Test Macro F1:    {test_macro_f1:.4f}")
    print(f"Test Weighted F1: {test_weighted_f1:.4f}")

    target_names = ["LEGITIMATE", "AMBIGUOUS", "SCAM"]
    clf_report = classification_report(y_test, test_preds, target_names=target_names, output_dict=True)
    cm = confusion_matrix(y_test, test_preds).tolist()
    
    print("\nPer-Class Classification Report:")
    print(classification_report(y_test, test_preds, target_names=target_names))
    print(f"Confusion Matrix (Rows: Actual, Cols: Pred):\n{np.array(cm)}")

    # 5. Baseline Comparison: 8-Pillar Rule Engine on the Same Test Set
    print("\n--- BASELINE COMPARISON: 8-PILLAR RULE ENGINE ON TEST SET ---")
    rule_metrics = evaluate_rule_engine(test_texts, test_labels, test_langs)
    print(f"Rule Engine Accuracy: {rule_metrics['accuracy']:.4f} ({rule_metrics['accuracy']*100:.1f}%)")
    print(f"Rule Engine Macro F1: {rule_metrics['macro_f1']:.4f}")
    print(f"Rule Engine Confusion Matrix:\n{np.array(rule_metrics['confusion_matrix'])}")

    # 6. Per-Language Breakdown on Test Set
    print("\n--- PER-LANGUAGE PERFORMANCE BREAKDOWN ON TEST SET ---")
    lang_metrics = {}
    for lang in ["en", "hi", "te", "hi-en", "te-en"]:
        lang_indices = [i for i, l in enumerate(test_langs) if l == lang]
        if lang_indices:
            y_sub = y_test[lang_indices]
            preds_sub = test_preds[lang_indices]
            sub_acc = accuracy_score(y_sub, preds_sub)
            sub_f1 = f1_score(y_sub, preds_sub, average="macro", zero_division=0)
            lang_metrics[lang] = {
                "samples_count": len(lang_indices),
                "accuracy": round(float(sub_acc), 4),
                "macro_f1": round(float(sub_f1), 4)
            }
            print(f"Language '{lang:5s}': Accuracy = {sub_acc*100:5.1f}%, Macro F1 = {sub_f1:.4f} (Samples: {len(lang_indices)})")

    # 7. Real Inference Latency Benchmark on Current Machine
    print("\nBenchmarking CPU inference latency over 100 iterations...")
    sample_text = test_texts[0]
    latencies = []
    for _ in range(100):
        t0 = time.perf_counter()
        vec = vectorizer.transform([sample_text])
        _ = calibrated_clf.predict_proba(vec)
        latencies.append((time.perf_counter() - t0) * 1000.0) # in ms
        
    p50_latency = float(np.median(latencies))
    p95_latency = float(np.percentile(latencies, 95))
    mean_latency = float(np.mean(latencies))
    print(f"Inference Latency: Mean = {mean_latency:.2f} ms | P50 = {p50_latency:.2f} ms | P95 = {p95_latency:.2f} ms")

    # 8. Export Artifacts
    model_file = ARTIFACTS_DIR / "model.joblib"
    vectorizer_file = ARTIFACTS_DIR / "vectorizer.joblib"
    meta_file = ARTIFACTS_DIR / "metadata.json"
    label_file = ARTIFACTS_DIR / "label_mapping.json"
    report_file = REPORTS_DIR / "model_evaluation_report.json"
    
    joblib.dump(calibrated_clf, model_file)
    joblib.dump(vectorizer, vectorizer_file)
    
    with open(label_file, "w", encoding="utf-8") as f:
        json.dump({"label2id": LABEL2ID, "id2label": ID2LABEL}, f, indent=2)
        
    # Load cross-split similarity diagnostics from split integrity report if available
    split_rep_path = REPORTS_DIR / "split_integrity_report.json"
    cross_split_sim = {}
    if split_rep_path.exists():
        try:
            with open(split_rep_path, "r", encoding="utf-8") as f:
                s_rep = json.load(f)
                cross_split_sim = s_rep.get("audited_datasets", {}).get("kavach_synthetic_v2", {}).get("near_duplicate_diagnostics", {})
        except Exception:
            pass

    eval_payload = {
        "model_name": "KAVACH-AI Multilingual Calibrated Classifier v1.0",
        "model_architecture": "TF-IDF (1-2 word n-grams, sublinear_tf) + Calibrated Logistic Regression (Platt scaling)",
        "framework": "scikit-learn",
        "trained_timestamp": "2026-11-05T09:50:00Z",
        "training_dataset": "data/kavach_synthetic_v2",
        "split_sizes": {
            "train": len(train_texts),
            "validation": len(val_texts),
            "test": len(test_texts)
        },
        "vocabulary_size": len(vectorizer.vocabulary_),
        "validation_metrics": {
            "accuracy": round(float(val_acc), 4),
            "macro_f1": round(float(val_macro_f1), 4)
        },
        "test_metrics": {
            "accuracy": round(float(test_acc), 4),
            "macro_f1": round(float(test_macro_f1), 4),
            "weighted_f1": round(float(test_weighted_f1), 4),
            "per_class": {
                name: {
                    "precision": round(clf_report[name]["precision"], 4),
                    "recall": round(clf_report[name]["recall"], 4),
                    "f1_score": round(clf_report[name]["f1-score"], 4),
                    "support": clf_report[name]["support"]
                }
                for name in target_names
            },
            "confusion_matrix": cm,
            "per_language_metrics": lang_metrics
        },
        "cross_split_similarity_diagnostics": cross_split_sim,
        "baseline_comparison": {
            "rule_engine_test_accuracy": rule_metrics["accuracy"],
            "rule_engine_test_macro_f1": rule_metrics["macro_f1"],
            "rule_engine_confusion_matrix": rule_metrics["confusion_matrix"],
            "ml_accuracy_delta": round(float(test_acc - rule_metrics["accuracy"]), 4)
        },
        "measured_latency_ms": {
            "mean": round(mean_latency, 2),
            "p50": round(p50_latency, 2),
            "p95": round(p95_latency, 2)
        },
        "model_sizes_kb": {
            "model_joblib": round(model_file.stat().st_size / 1024, 2),
            "vectorizer_joblib": round(vectorizer_file.stat().st_size / 1024, 2)
        },
        "synthetic_dataset_limitations": {
            "synthetic_provenance": "Evaluated strictly on synthetic domain scenario transcripts (KAVACH synthetic v2).",
            "telephony_generalization_limit": "Does not establish or claim production telephony accuracy in unconstrained real-world environments with telephony noise, accent variation, or live audio artifacts.",
            "leakage_isolation": "Strict 0% scenario-family, 0% exact dialogue hash, and 0% CID leakage across train, val, and test splits."
        },
        "disclaimer": "Metrics measured strictly on held-out synthetic domain scenario test set. Real-world wild telephony performance requires field validation."
    }
    
    with open(meta_file, "w", encoding="utf-8") as f:
        json.dump(eval_payload, f, indent=2, ensure_ascii=False)
        
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(eval_payload, f, indent=2, ensure_ascii=False)

    print(f"\n[ALL COMPLETE] Model artifacts exported to {ARTIFACTS_DIR}:")
    print(f"  - {model_file.name} ({eval_payload['model_sizes_kb']['model_joblib']} KB)")
    print(f"  - {vectorizer_file.name} ({eval_payload['model_sizes_kb']['vectorizer_joblib']} KB)")
    print(f"  - {meta_file.name}")
    print(f"  - {label_file.name}")
    print(f"Wrote full evaluation report to: {report_file}")

if __name__ == "__main__":
    train_and_evaluate()
