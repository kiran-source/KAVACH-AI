import os
import json
from typing import Dict, Any, List
from app.detection.engine import analyze_transcript
from app.core.logging import logger

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../data"))
LABELS_FILE = os.path.join(DATA_DIR, "labels", "scenarios.json")
EVAL_DIR = os.path.join(DATA_DIR, "evaluation")
os.makedirs(EVAL_DIR, exist_ok=True)

def run_evaluation_pipeline() -> Dict[str, Any]:
    """
    Executes the reproducible evaluation pipeline on the synthetic dataset.
    Calculates TP, TN, FP, FN, Precision, Recall, F1 score, Confusion Matrix,
    per-language performance, and saves results to data/evaluation/.
    """
    if not os.path.exists(LABELS_FILE):
        logger.error(f"Labels file not found at {LABELS_FILE}")
        return {"error": "Scenarios file not found"}

    with open(LABELS_FILE, "r", encoding="utf-8") as f:
        scenarios: List[Dict[str, Any]] = json.load(f)

    tp, tn, fp, fn = 0, 0, 0, 0
    language_stats: Dict[str, Dict[str, int]] = {}
    category_stats: Dict[str, Dict[str, int]] = {}
    detailed_results = []

    for sc in scenarios:
        sid = sc["scenario_id"]
        lang = sc.get("language", "en")
        script = sc["script"]
        expected_class = sc["expected_classification"]
        expected_threats = set(sc.get("expected_threat_categories", []))

        # Model inference without ground-truth labels
        analysis = analyze_transcript(script, language_hint=lang)
        predicted_score = analysis["risk_score"]
        predicted_severity = analysis["severity"]
        detected_categories = set(analysis["categories"])

        # Operational threshold: Risk Score >= 40 is classified as Scam/Suspicious
        predicted_class = "scam" if predicted_score >= 40.0 else "legitimate"

        # Classification outcome mapping
        is_ground_scam = (expected_class == "scam")
        is_pred_scam = (predicted_class == "scam")

        if is_ground_scam and is_pred_scam:
            tp += 1
            outcome = "TP"
        elif not is_ground_scam and not is_pred_scam:
            tn += 1
            outcome = "TN"
        elif not is_ground_scam and is_pred_scam:
            fp += 1
            outcome = "FP"
        else: # is_ground_scam and not is_pred_scam
            fn += 1
            outcome = "FN"

        # Update language statistics
        if lang not in language_stats:
            language_stats[lang] = {"total": 0, "correct": 0}
        language_stats[lang]["total"] += 1
        if (is_ground_scam and is_pred_scam) or (not is_ground_scam and not is_pred_scam):
            language_stats[lang]["correct"] += 1

        # Update category coverage
        for cat in expected_threats:
            if cat not in category_stats:
                category_stats[cat] = {"expected": 0, "detected": 0}
            category_stats[cat]["expected"] += 1
            if cat in detected_categories:
                category_stats[cat]["detected"] += 1

        detailed_results.append({
            "scenario_id": sid,
            "title": sc["title"],
            "language": lang,
            "expected_classification": expected_class,
            "predicted_score": predicted_score,
            "predicted_severity": predicted_severity,
            "detected_categories": list(detected_categories),
            "outcome": outcome
        })

    # Summary metrics calculation
    total_samples = len(scenarios)
    precision = round(tp / (tp + fp), 4) if (tp + fp) > 0 else 0.0
    recall = round(tp / (tp + fn), 4) if (tp + fn) > 0 else 0.0
    f1 = round(2 * (precision * recall) / (precision + recall), 4) if (precision + recall) > 0 else 0.0
    accuracy = round((tp + tn) / total_samples, 4) if total_samples > 0 else 0.0

    per_language_accuracy = {
        lang: round(stats["correct"] / stats["total"], 4) if stats["total"] > 0 else 0.0
        for lang, stats in language_stats.items()
    }

    per_category_coverage = {
        cat: round(stats["detected"] / stats["expected"], 4) if stats["expected"] > 0 else 0.0
        for cat, stats in category_stats.items()
    }

    metrics_payload = {
        "dataset_size": total_samples,
        "confusion_matrix": {
            "true_positives": tp,
            "true_negatives": tn,
            "false_positives": fp,
            "false_negatives": fn
        },
        "metrics": {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1_score": f1
        },
        "per_language_accuracy": per_language_accuracy,
        "per_category_coverage": per_category_coverage,
        "detailed_results": detailed_results
    }

    # Persist JSON report
    metrics_path = os.path.join(EVAL_DIR, "metrics.json")
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics_payload, f, indent=2)

    logger.info(f"Evaluation complete. F1: {f1}, Precision: {precision}, Recall: {recall}")
    return metrics_payload

