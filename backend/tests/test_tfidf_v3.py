"""
Unit Tests for TF-IDF v3 Artifacts, Model Loading, Calibration, and Multilingual Inference.
Tests experimental TF-IDF v3 model artifacts without altering production v1 baseline.
"""

import json
import hashlib
import pytest
import numpy as np
import joblib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
TFIDF_V3_DIR = PROJECT_ROOT / "backend" / "app" / "ml" / "artifacts" / "tfidf_v3"
TFIDF_V1_DIR = PROJECT_ROOT / "backend" / "app" / "ml" / "artifacts" / "v1"

@pytest.fixture(scope="module")
def v3_artifacts():
    """Loads all TF-IDF v3 artifacts."""
    assert TFIDF_V3_DIR.exists(), f"Directory not found: {TFIDF_V3_DIR}"
    
    vec_path = TFIDF_V3_DIR / "vectorizer.joblib"
    model_path = TFIDF_V3_DIR / "model.joblib"
    label_path = TFIDF_V3_DIR / "label_mapping.json"
    meta_path = TFIDF_V3_DIR / "metadata.json"
    config_path = TFIDF_V3_DIR / "training_config.json"
    metrics_path = TFIDF_V3_DIR / "training_metrics.json"
    checksum_path = TFIDF_V3_DIR / "checksums.sha256"

    for p in [vec_path, model_path, label_path, meta_path, config_path, metrics_path, checksum_path]:
        assert p.exists(), f"Missing required v3 artifact: {p.name}"

    vectorizer = joblib.load(vec_path)
    model = joblib.load(model_path)
    
    with open(label_path, "r", encoding="utf-8") as f:
        labels = json.load(f)
    with open(meta_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    with open(metrics_path, "r", encoding="utf-8") as f:
        metrics = json.load(f)

    return {
        "vectorizer": vectorizer,
        "model": model,
        "labels": labels,
        "metadata": metadata,
        "config": config,
        "metrics": metrics,
        "checksum_path": checksum_path
    }

def test_v3_checksums_integrity(v3_artifacts):
    """Verifies SHA-256 checksums match the actual disk artifacts."""
    checksum_path = v3_artifacts["checksum_path"]
    with open(checksum_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    assert len(lines) >= 6
    for line in lines:
        if not line.strip():
            continue
        sha, fname = line.strip().split(maxsplit=1)
        fpath = TFIDF_V3_DIR / fname
        assert fpath.exists(), f"File in checksums does not exist: {fname}"
        actual_sha = hashlib.sha256(fpath.read_bytes()).hexdigest()
        assert actual_sha == sha, f"Checksum mismatch for {fname}"

def test_v3_label_mapping(v3_artifacts):
    """Verifies label mapping adheres to the 3-class standard schema."""
    labels = v3_artifacts["labels"]
    assert "label2id" in labels
    assert "id2label" in labels
    assert labels["label2id"] == {"LEGITIMATE": 0, "AMBIGUOUS": 1, "SCAM": 2}
    assert labels["id2label"]["0"] == "LEGITIMATE"
    assert labels["id2label"]["1"] == "AMBIGUOUS"
    assert labels["id2label"]["2"] == "SCAM"

def test_v3_model_metadata(v3_artifacts):
    """Verifies metadata reflects dataset v3 and experimental status."""
    meta = v3_artifacts["metadata"]
    assert "v3.0" in meta.get("model_name", "")
    assert meta.get("training_dataset") == "data/kavach_synthetic_v3"
    assert meta.get("status") == "EXPERIMENTAL_BENCHMARK_ONLY"
    assert meta.get("split_sizes", {}).get("train") == 2100
    assert meta.get("split_sizes", {}).get("validation") == 450
    assert meta.get("split_sizes", {}).get("test") == 450

def test_v3_calibrated_probabilities(v3_artifacts):
    """Verifies calibrated model returns valid probability distributions."""
    vec = v3_artifacts["vectorizer"]
    model = v3_artifacts["model"]

    sample_scam = "This is Inspector Sharma from CBI headquarters. You are under digital arrest. Pay fee immediately."
    features = vec.transform([sample_scam])
    probs = model.predict_proba(features)[0]

    assert len(probs) == 3
    assert np.all(probs >= 0.0) and np.all(probs <= 1.0)
    assert abs(np.sum(probs) - 1.0) < 1e-4
    predicted_class = int(np.argmax(probs))
    assert predicted_class == 2  # SCAM

def test_v3_multilingual_inference(v3_artifacts):
    """Tests inference across all 5 supported languages."""
    vec = v3_artifacts["vectorizer"]
    model = v3_artifacts["model"]

    test_inputs = {
        "en": "Hello this is a routine verification call from the security department.",
        "hi": "नमस्ते, यह सुरक्षा विभाग से नियमित खाता सत्यापन कॉल है।",
        "te": "నమస్కారం, ఇది సెక్యూరిటీ డిపార్ట్‌మెంట్ నుండి రొటీన్ ఖాతా వెరిఫికేషన్ కాల్.",
        "hi-en": "Hello sir, aapke account ka routine verification complete karna hai.",
        "te-en": "Hello sir, mee account routine verification kosam call chestunnam."
    }

    for lang, text in test_inputs.items():
        feat = vec.transform([text])
        probs = model.predict_proba(feat)[0]
        assert len(probs) == 3
        assert np.isfinite(probs).all()
        assert abs(np.sum(probs) - 1.0) < 1e-4

def test_v3_empty_and_whitespace_input(v3_artifacts):
    """Ensures empty strings and whitespace are handled gracefully without exceptions."""
    vec = v3_artifacts["vectorizer"]
    model = v3_artifacts["model"]

    for empty_val in ["", "   ", "\n\t"]:
        feat = vec.transform([empty_val])
        probs = model.predict_proba(feat)[0]
        assert len(probs) == 3
        assert np.isfinite(probs).all()

def test_production_baseline_v1_isolation():
    """Verifies that production baseline artifacts (v1) remain completely untouched."""
    assert TFIDF_V1_DIR.exists()
    assert (TFIDF_V1_DIR / "model.joblib").exists()
    assert (TFIDF_V1_DIR / "vectorizer.joblib").exists()
    assert (TFIDF_V1_DIR / "metadata.json").exists()
    assert (TFIDF_V1_DIR / "label_mapping.json").exists()

    with open(TFIDF_V1_DIR / "metadata.json", "r", encoding="utf-8") as f:
        meta_v1 = json.load(f)
    assert meta_v1.get("training_dataset") == "data/kavach_synthetic_v2"
    assert meta_v1.get("split_sizes", {}).get("train") == 350
    assert meta_v1.get("split_sizes", {}).get("test") == 75

