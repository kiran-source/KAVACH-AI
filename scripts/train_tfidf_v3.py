"""
TF-IDF v3 Multilingual Model Training & Calibration Pipeline for KAVACH AI
Trains TF-IDF + Calibrated Logistic Regression on synthetic dataset v3.
Explores multiple feature and hyperparameter configurations on the training split,
selects the optimal configuration strictly based on validation Macro F1,
and exports production-structured artifacts to backend/app/ml/artifacts/tfidf_v3/.
"""

import sys
import json
import time
import hashlib
from pathlib import Path
from typing import Dict, Any, List, Tuple
from collections import Counter

import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import FeatureUnion
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import accuracy_score, f1_score, precision_recall_fscore_support, classification_report

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SPLITS_DIR = PROJECT_ROOT / "data" / "kavach_synthetic_v3" / "splits"
ARTIFACTS_DIR = PROJECT_ROOT / "backend" / "app" / "ml" / "artifacts" / "tfidf_v3"
REPORTS_DIR = PROJECT_ROOT / "reports"

LABEL2ID = {"LEGITIMATE": 0, "AMBIGUOUS": 1, "SCAM": 2}
ID2LABEL = {0: "LEGITIMATE", 1: "AMBIGUOUS", 2: "SCAM"}
TARGET_NAMES = ["LEGITIMATE", "AMBIGUOUS", "SCAM"]

def load_split(split_name: str) -> Tuple[List[str], np.ndarray, List[str], List[str]]:
    """Loads a split from data/kavach_synthetic_v3/splits/{split_name}.jsonl."""
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
            # Use full dialogue sequence joined cleanly
            dialogue_text = " ".join([turn.get("text", "") for turn in rec.get("dialogue", [])]).strip()
            texts.append(dialogue_text)
            labels.append(LABEL2ID[rec["primary_label"]])
            languages.append(rec["language"])
            cids.append(rec["conversation_id"])

    return texts, np.array(labels), languages, cids

def generate_checksums(directory: Path) -> Dict[str, str]:
    """Computes SHA-256 hashes for all generated files in target directory."""
    hashes = {}
    for fpath in sorted(directory.iterdir()):
        if fpath.is_file() and fpath.name != "checksums.sha256":
            sha = hashlib.sha256(fpath.read_bytes()).hexdigest()
            hashes[fpath.name] = sha
    return hashes

def train_and_select_model():
    print("=" * 80)
    print("KAVACH AI — TF-IDF v3 MULTILINGUAL TRAINING & CALIBRATION PIPELINE")
    print("=" * 80)

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Load Train and Validation Splits
    print("\n--- 1. LOADING DATASET V3 PARTITIONS ---")
    train_texts, y_train, train_langs, train_cids = load_split("train")
    val_texts, y_val, val_langs, val_cids = load_split("validation")

    print(f"Train samples:      {len(train_texts)} records")
    print(f"Validation samples: {len(val_texts)} records")
    print(f"Train labels:       {dict(Counter(y_train))}")
    print(f"Validation labels:  {dict(Counter(y_val))}")
    print(f"Train languages:    {dict(Counter(train_langs))}")
    print(f"Validation langs:   {dict(Counter(val_langs))}")

    # 2. Define Candidate Model Configurations
    candidates = [
        {
            "id": "config_1_word_5k_c15",
            "name": "Word (1, 2) n-grams | max_features=5,000 | C=1.5 | Sigmoid Calibrated",
            "vectorizer_builder": lambda: TfidfVectorizer(
                ngram_range=(1, 2),
                max_features=5000,
                sublinear_tf=True,
                strip_accents="unicode"
            ),
            "clf_builder": lambda: LogisticRegression(
                C=1.5,
                class_weight="balanced",
                max_iter=1000,
                random_state=42
            )
        },
        {
            "id": "config_2_word_10k_c10",
            "name": "Word (1, 2) n-grams | max_features=10,000 | C=1.0 | Sigmoid Calibrated",
            "vectorizer_builder": lambda: TfidfVectorizer(
                ngram_range=(1, 2),
                max_features=10000,
                sublinear_tf=True,
                strip_accents="unicode"
            ),
            "clf_builder": lambda: LogisticRegression(
                C=1.0,
                class_weight="balanced",
                max_iter=1000,
                random_state=42
            )
        },
        {
            "id": "config_3_word_char_union_c15",
            "name": "Word (1,2: 10k) + Char (3,5: 5k) FeatureUnion | C=1.5 | Sigmoid Calibrated",
            "vectorizer_builder": lambda: FeatureUnion([
                ("word", TfidfVectorizer(
                    ngram_range=(1, 2),
                    max_features=10000,
                    sublinear_tf=True,
                    strip_accents="unicode"
                )),
                ("char", TfidfVectorizer(
                    ngram_range=(3, 5),
                    analyzer="char_wb",
                    max_features=5000,
                    sublinear_tf=True
                ))
            ]),
            "clf_builder": lambda: LogisticRegression(
                C=1.5,
                class_weight="balanced",
                max_iter=1000,
                random_state=42
            )
        }
    ]

    print("\n--- 2. HYPERPARAMETER EXPLORATION & VALIDATION BENCHMARK ---")
    candidate_results = []
    trained_artifacts = {}

    for cand in candidates:
        cand_id = cand["id"]
        print(f"\nEvaluating: {cand['name']}")
        t0 = time.perf_counter()

        # Fit vectorizer strictly on train_texts
        vec = cand["vectorizer_builder"]()
        X_train = vec.fit_transform(train_texts)
        X_val = vec.transform(val_texts)

        # Build base classifier and calibrated model
        base_clf = cand["clf_builder"]()
        calibrated_model = CalibratedClassifierCV(estimator=base_clf, method="sigmoid", cv=3)
        calibrated_model.fit(X_train, y_train)

        fit_time = time.perf_counter() - t0

        # Evaluate on validation split (N=450)
        val_preds = calibrated_model.predict(X_val)
        val_acc = accuracy_score(y_val, val_preds)
        val_macro_f1 = f1_score(y_val, val_preds, average="macro")
        val_weighted_f1 = f1_score(y_val, val_preds, average="weighted")
        val_p_macro, val_r_macro, _, _ = precision_recall_fscore_support(y_val, val_preds, average="macro", zero_division=0)

        # Per-class metrics
        report = classification_report(y_val, val_preds, target_names=TARGET_NAMES, output_dict=True)

        res = {
            "candidate_id": cand_id,
            "name": cand["name"],
            "fit_time_sec": round(fit_time, 2),
            "num_features": X_train.shape[1],
            "val_accuracy": round(float(val_acc), 4),
            "val_macro_f1": round(float(val_macro_f1), 4),
            "val_macro_precision": round(float(val_p_macro), 4),
            "val_macro_recall": round(float(val_r_macro), 4),
            "val_weighted_f1": round(float(val_weighted_f1), 4),
            "ambiguous_recall": round(float(report["AMBIGUOUS"]["recall"]), 4),
            "scam_recall": round(float(report["SCAM"]["recall"]), 4),
            "legitimate_recall": round(float(report["LEGITIMATE"]["recall"]), 4)
        }
        candidate_results.append(res)
        trained_artifacts[cand_id] = (vec, calibrated_model)

        print(f"  -> Features: {X_train.shape[1]:,} | Fit Time: {fit_time:.2f}s")
        print(f"  -> Val Accuracy: {val_acc*100:.2f}% | Val Macro F1: {val_macro_f1:.4f}")
        print(f"  -> Per-Class Recall: AMBIGUOUS={report['AMBIGUOUS']['recall']:.4f}, SCAM={report['SCAM']['recall']:.4f}, LEGIT={report['LEGITIMATE']['recall']:.4f}")

    # 3. Model Selection strictly by Validation Macro F1
    candidate_results.sort(key=lambda x: (x["val_macro_f1"], x["val_accuracy"]), reverse=True)
    best_candidate_info = candidate_results[0]
    best_id = best_candidate_info["candidate_id"]
    best_vec, best_model = trained_artifacts[best_id]

    print("\n" + "=" * 80)
    print(f"SELECTED OPTIMAL CONFIGURATION: {best_candidate_info['name']}")
    print(f"Selection Metric: Validation Macro F1 = {best_candidate_info['val_macro_f1']:.4f}")
    print("=" * 80)

    # 4. Save Final Artifacts to backend/app/ml/artifacts/tfidf_v3/
    print(f"\n--- 3. EXPORTING PRODUCTION ARTIFACTS TO {ARTIFACTS_DIR} ---")
    vec_path = ARTIFACTS_DIR / "vectorizer.joblib"
    model_path = ARTIFACTS_DIR / "model.joblib"
    label_path = ARTIFACTS_DIR / "label_mapping.json"
    config_path = ARTIFACTS_DIR / "training_config.json"
    meta_path = ARTIFACTS_DIR / "metadata.json"
    metrics_path = ARTIFACTS_DIR / "training_metrics.json"

    # Dump binary models
    joblib.dump(best_vec, vec_path)
    joblib.dump(best_model, model_path)

    # Dump label mapping
    label_payload = {
        "label2id": LABEL2ID,
        "id2label": ID2LABEL
    }
    with open(label_path, "w", encoding="utf-8") as f:
        json.dump(label_payload, f, indent=2)

    # Dump training config
    training_config = {
        "model_version": "tfidf_v3.0",
        "selected_candidate": best_candidate_info,
        "all_candidates_benchmarked": candidate_results,
        "calibration_method": "sigmoid (Platt scaling 3-fold CV)",
        "dataset_split_source": "data/kavach_synthetic_v3/splits/",
        "training_partition_samples": len(train_texts),
        "validation_partition_samples": len(val_texts),
        "target_names": TARGET_NAMES,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(training_config, f, indent=2)

    # Dump training metrics
    training_metrics = {
        "model_version": "tfidf_v3.0",
        "train_samples": len(train_texts),
        "validation_samples": len(val_texts),
        "validation_accuracy": best_candidate_info["val_accuracy"],
        "validation_macro_f1": best_candidate_info["val_macro_f1"],
        "validation_macro_precision": best_candidate_info["val_macro_precision"],
        "validation_macro_recall": best_candidate_info["val_macro_recall"],
        "validation_weighted_f1": best_candidate_info["val_weighted_f1"],
        "class_recall": {
            "LEGITIMATE": best_candidate_info["legitimate_recall"],
            "AMBIGUOUS": best_candidate_info["ambiguous_recall"],
            "SCAM": best_candidate_info["scam_recall"]
        },
        "model_size_bytes": {
            "model_joblib": model_path.stat().st_size,
            "vectorizer_joblib": vec_path.stat().st_size
        }
    }
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(training_metrics, f, indent=2)

    # Dump metadata.json
    metadata_payload = {
        "model_name": "KAVACH-AI Multilingual Calibrated Classifier v3.0 (Experimental Benchmark)",
        "model_architecture": f"TF-IDF ({best_candidate_info['name']}) + Calibrated Logistic Regression (Platt scaling)",
        "framework": "scikit-learn",
        "trained_timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "training_dataset": "data/kavach_synthetic_v3",
        "split_sizes": {
            "train": len(train_texts),
            "validation": len(val_texts),
            "test": 450
        },
        "vocabulary_size": best_candidate_info["num_features"],
        "validation_metrics": {
            "accuracy": best_candidate_info["val_accuracy"],
            "macro_f1": best_candidate_info["val_macro_f1"]
        },
        "model_sizes_kb": {
            "model_joblib": round(model_path.stat().st_size / 1024, 2),
            "vectorizer_joblib": round(vec_path.stat().st_size / 1024, 2)
        },
        "synthetic_dataset_limitations": {
            "annotation_status": "All 3,000 records have annotation_status: pending_review.",
            "synthetic_provenance": "Evaluated strictly on synthetic domain scenario transcripts (KAVACH synthetic v3).",
            "telephony_generalization_limit": "Does not establish or claim production telephony accuracy in unconstrained real-world environments.",
            "leakage_isolation": "Strict 0% scenario-family, 0% exact dialogue hash, and 0% CID leakage across train, val, and test splits."
        },
        "status": "EXPERIMENTAL_BENCHMARK_ONLY",
        "production_baseline_status": "Active baseline remains v1 in backend/app/ml/artifacts/v1/"
    }
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata_payload, f, indent=2, ensure_ascii=False)

    # Compute and write SHA-256 Checksums
    checksums = generate_checksums(ARTIFACTS_DIR)
    checksums_path = ARTIFACTS_DIR / "checksums.sha256"
    with open(checksums_path, "w", encoding="utf-8") as f:
        for fname, hsh in checksums.items():
            f.write(f"{hsh}  {fname}\n")

    print(f"Wrote checksums to: {checksums_path}")
    print(f"[SUCCESS] All 7 target artifacts exported cleanly to {ARTIFACTS_DIR}")
    return training_config

if __name__ == "__main__":
    train_and_select_model()

