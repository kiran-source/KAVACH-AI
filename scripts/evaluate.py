import os
import json
from app.detection.engine import analyze_transcript

def run_evaluation():
    manifest_path = "data/labels/dataset_manifest.json"
    if not os.path.exists(manifest_path):
        print("Dataset manifest not found. Please run scripts/create_dataset.py first.")
        return
        
    with open(manifest_path, "r", encoding="utf-8") as f:
        dataset = json.load(f)
        
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    
    results = []
    
    for item in dataset:
        script = item["script"]
        expected = item["expected_classification"] # scam or safe
        
        analysis = analyze_transcript(script)
        risk_score = analysis["risk_score"]
        
        predicted = "scam" if risk_score >= 40 else "safe"
        
        if expected == "scam" and predicted == "scam":
            tp += 1
        elif expected == "safe" and predicted == "safe":
            tn += 1
        elif expected == "safe" and predicted == "scam":
            fp += 1
        elif expected == "scam" and predicted == "safe":
            fn += 1
            
        results.append({
            "scenario_id": item["scenario_id"],
            "title": item["title"],
            "expected": expected,
            "predicted": predicted,
            "risk_score": risk_score,
            "match": expected == predicted
        })
        
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    
    report = {
        "total_scenarios": len(dataset),
        "true_positives": tp,
        "true_negatives": tn,
        "false_positives": fp,
        "false_negatives": fn,
        "precision": round(precision, 2),
        "recall": round(recall, 2),
        "f1_score": round(f1, 2),
        "detailed_results": results
    }
    
    os.makedirs("reports", exist_ok=True)
    report_path = "reports/evaluation_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
        
    print("=== KAVACH AI EVALUATION REPORT ===")
    print(f"Total Scenarios: {len(dataset)}")
    print(f"Precision: {precision:.2f}")
    print(f"Recall: {recall:.2f}")
    print(f"F1 Score: {f1:.2f}")
    print(f"Detailed evaluation report saved to {report_path}")

if __name__ == "__main__":
    run_evaluation()
