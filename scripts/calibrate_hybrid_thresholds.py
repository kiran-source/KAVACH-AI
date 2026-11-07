"""
Validation-Based Threshold Calibration for KAVACH AI Hybrid Intelligence Engine.
Evaluates escalation thresholds strictly on data/kavach_synthetic_v3/splits/validation.jsonl (N=450).
Measures escalation percentage, macro F1, per-class recall, and latency trade-offs.
"""

import sys
import json
import time
from pathlib import Path
from typing import Dict, Any, List, Tuple
from collections import Counter

try:
    sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
except Exception:
    pass

import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SPLITS_DIR = PROJECT_ROOT / "data" / "kavach_synthetic_v3" / "splits"
REPORTS_DIR = PROJECT_ROOT / "reports"

sys.path.insert(0, str(PROJECT_ROOT / "backend"))
from app.ml.hybrid_config import HybridEngineConfig, HybridMode
from app.ml.hybrid_engine import HybridIntelligenceEngine
from app.ml.tfidf_v3_loader import get_tfidf_v3_classifier
from app.ml.muril_classifier import get_muril_classifier

LABEL2ID = {"LEGITIMATE": 0, "AMBIGUOUS": 1, "SCAM": 2}
TARGET_NAMES = ["LEGITIMATE", "AMBIGUOUS", "SCAM"]

def load_val_split() -> Tuple[List[str], np.ndarray, List[str], List[str]]:
    val_file = SPLITS_DIR / "validation.jsonl"
    texts = []
    labels = []
    languages = []
    cids = []

    with open(val_file, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            rec = json.loads(line)
            convo = " ".join([t.get("text", "") for t in rec.get("dialogue", [])]).strip()
            texts.append(convo)
            labels.append(LABEL2ID[rec["primary_label"]])
            languages.append(rec["language"])
            cids.append(rec["conversation_id"])

    return texts, np.array(labels), languages, cids

def run_threshold_calibration():
    print("=" * 80, flush=True)
    print("KAVACH AI — VALIDATION-BASED THRESHOLD CALIBRATION (N=450)", flush=True)
    print("=" * 80, flush=True)

    texts, y_true, languages, cids = load_val_split()
    total_val = len(texts)
    print(f"Loaded validation split: {total_val} records", flush=True)
    print(f"Class distribution: {dict(Counter(y_true))}", flush=True)
    print(f"Language distribution: {dict(Counter(languages))}", flush=True)

    # Pre-compute TF-IDF inferences on validation set
    print("\nPre-computing TF-IDF v3 inferences on validation split...", flush=True)
    t0 = time.perf_counter()
    tfidf_clf = get_tfidf_v3_classifier()
    tfidf_preds = tfidf_clf.predict_batch(texts)
    t_tfidf = time.perf_counter() - t0
    print(f"TF-IDF inferences completed in {t_tfidf:.2f}s ({len(tfidf_preds)} samples)", flush=True)

    # Pre-compute MuRIL inferences with batch size 32
    print("\nPre-computing MuRIL v1 inferences on validation split (batched)...", flush=True)
    t0 = time.perf_counter()
    muril_clf = get_muril_classifier()
    muril_preds = muril_clf.predict_batch(texts, batch_size=32)
    t_muril = time.perf_counter() - t0
    print(f"MuRIL inferences completed in {t_muril:.2f}s ({len(muril_preds)} samples)", flush=True)

    # Test candidate confidence thresholds
    candidate_thresholds = [0.60, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95]
    results = []

    print("\n--- GRID SEARCH: CONFIDENCE ESCALATION THRESHOLDS ---", flush=True)
    for conf_th in candidate_thresholds:
        cfg = HybridEngineConfig(
            mode=HybridMode.HYBRID_SELECTIVE,
            escalation_confidence_threshold=conf_th,
            escalation_margin_threshold=0.15,
            escalate_on_ambiguous=True,
            escalate_on_codemixed=True
        )

        escalated_count = 0
        final_preds = []

        for i, t in enumerate(texts):
            tf_res = tfidf_preds[i]
            lang = languages[i]

            should_escalate = False
            tf_label = tf_res.get("predicted_label")
            conf = tf_res.get("confidence", 1.0)
            probs = tf_res.get("probabilities", {})
            sorted_p = sorted(probs.values(), reverse=True)
            margin = (sorted_p[0] - sorted_p[1]) if len(sorted_p) > 1 else 1.0

            if cfg.escalate_on_ambiguous and tf_label == "AMBIGUOUS":
                should_escalate = True
            elif conf < conf_th:
                should_escalate = True
            elif margin < cfg.escalation_margin_threshold:
                should_escalate = True
            elif cfg.escalate_on_codemixed and lang in ["hi-en", "te-en"] and conf < 0.90:
                should_escalate = True

            if should_escalate:
                escalated_count += 1
                m_res = muril_preds[i]
                m_label = m_res.get("predicted_label")
                if tf_label == m_label:
                    pred_label = tf_label
                elif "SCAM" in [tf_label, m_label]:
                    pred_label = "SCAM"
                elif "AMBIGUOUS" in [tf_label, m_label]:
                    pred_label = "AMBIGUOUS"
                else:
                    pred_label = "AMBIGUOUS"
            else:
                pred_label = tf_label

            final_preds.append(LABEL2ID.get(pred_label, 1))

        y_pred = np.array(final_preds)
        acc = accuracy_score(y_true, y_pred)
        p_m, r_m, f1_m, _ = precision_recall_fscore_support(y_true, y_pred, average="macro", zero_division=0)
        rep = classification_report(y_true, y_pred, target_names=TARGET_NAMES, output_dict=True)

        scam_fn = sum(1 for yt, yp in zip(y_true, y_pred) if yt == LABEL2ID["SCAM"] and yp != LABEL2ID["SCAM"])
        esc_pct = (escalated_count / total_val) * 100.0

        res_item = {
            "confidence_threshold": conf_th,
            "escalated_count": escalated_count,
            "escalation_percentage": round(esc_pct, 2),
            "accuracy": round(float(acc), 4),
            "macro_f1": round(float(f1_m), 4),
            "scam_recall": round(float(rep["SCAM"]["recall"]), 4),
            "ambiguous_recall": round(float(rep["AMBIGUOUS"]["recall"]), 4),
            "legitimate_recall": round(float(rep["LEGITIMATE"]["recall"]), 4),
            "scam_false_negatives": scam_fn
        }
        results.append(res_item)
        print(f"Thresh={conf_th:.2f} | Escalated: {esc_pct:5.1f}% ({escalated_count:3d}/{total_val}) | Macro F1: {f1_m:.4f} | SCAM Rec: {rep['SCAM']['recall']:.4f} | FN: {scam_fn}", flush=True)

    # Optimal threshold selection: Maximize F1 with lowest escalation overhead
    best_res = max(results, key=lambda x: (x["macro_f1"], x["scam_recall"], -x["escalation_percentage"]))
    print("\n" + "=" * 80, flush=True)
    print(f"OPTIMAL OPERATING POINT SELECTED: Confidence Threshold = {best_res['confidence_threshold']}", flush=True)
    print(f"Escalation Rate: {best_res['escalation_percentage']}% | Macro F1: {best_res['macro_f1']:.4f} | SCAM FN: {best_res['scam_false_negatives']}", flush=True)
    print("=" * 80, flush=True)

    calibration_output = {
        "calibration_dataset": "data/kavach_synthetic_v3/splits/validation.jsonl",
        "validation_samples": total_val,
        "selected_operating_point": best_res,
        "all_threshold_experiments": results,
        "precompute_timings_sec": {
            "tfidf_v3": round(t_tfidf, 2),
            "muril_v1": round(t_muril, 2)
        },
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }

    out_file = REPORTS_DIR / "hybrid_threshold_calibration.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(calibration_output, f, indent=2)
    print(f"Saved calibration results to: {out_file}", flush=True)
    return calibration_output

if __name__ == "__main__":
    run_threshold_calibration()
