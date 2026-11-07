"""
TF-IDF v3 Artifact Loader and Classifier Wrapper for KAVACH AI.
Loads trained artifacts from backend/app/ml/artifacts/tfidf_v3/
and exposes a standard prediction interface.
"""

import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any, Tuple
import numpy as np

logger = logging.getLogger("kavach.ml.tfidf_v3")

ARTIFACTS_DIR = Path(__file__).resolve().parent / "artifacts" / "tfidf_v3"

_CACHED_MODEL = None
_CACHED_VECTORIZER = None
_CACHED_METADATA = None
_CACHED_LABELS = None
_LOAD_ATTEMPTED = False

def is_tfidf_v3_available() -> bool:
    """Checks if TF-IDF v3 model artifacts are present on disk."""
    model_path = ARTIFACTS_DIR / "model.joblib"
    vectorizer_path = ARTIFACTS_DIR / "vectorizer.joblib"
    meta_path = ARTIFACTS_DIR / "metadata.json"
    label_path = ARTIFACTS_DIR / "label_mapping.json"
    return model_path.exists() and vectorizer_path.exists() and meta_path.exists() and label_path.exists()

def load_tfidf_v3_artifacts() -> Tuple[Optional[Any], Optional[Any], Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
    """
    Loads and caches TF-IDF v3 model, vectorizer, metadata, and label mapping.
    Returns (model, vectorizer, metadata, label_mapping) or (None, None, None, None).
    """
    global _CACHED_MODEL, _CACHED_VECTORIZER, _CACHED_METADATA, _CACHED_LABELS, _LOAD_ATTEMPTED

    if _LOAD_ATTEMPTED:
        return _CACHED_MODEL, _CACHED_VECTORIZER, _CACHED_METADATA, _CACHED_LABELS

    _LOAD_ATTEMPTED = True

    if not is_tfidf_v3_available():
        logger.warning(f"TF-IDF v3 artifacts not found in {ARTIFACTS_DIR}.")
        return None, None, None, None

    try:
        import joblib
        model_path = ARTIFACTS_DIR / "model.joblib"
        vectorizer_path = ARTIFACTS_DIR / "vectorizer.joblib"
        meta_path = ARTIFACTS_DIR / "metadata.json"
        label_path = ARTIFACTS_DIR / "label_mapping.json"

        _CACHED_MODEL = joblib.load(model_path)
        _CACHED_VECTORIZER = joblib.load(vectorizer_path)

        with open(meta_path, "r", encoding="utf-8") as f:
            _CACHED_METADATA = json.load(f)

        with open(label_path, "r", encoding="utf-8") as f:
            _CACHED_LABELS = json.load(f)

        logger.info(f"Successfully loaded TF-IDF v3 classifier from {ARTIFACTS_DIR}.")
        return _CACHED_MODEL, _CACHED_VECTORIZER, _CACHED_METADATA, _CACHED_LABELS
    except Exception as e:
        logger.error(f"Failed to load TF-IDF v3 artifacts: {e}")
        _CACHED_MODEL = None
        _CACHED_VECTORIZER = None
        _CACHED_METADATA = None
        _CACHED_LABELS = None
        return None, None, None, None

class TFIDFV3Classifier:
    """
    Standardized inference wrapper for the TF-IDF v3 model.
    Provides predict, predict_proba, model_metadata, and health_check methods.
    """
    def __init__(self):
        self.model, self.vectorizer, self.metadata, self.labels = load_tfidf_v3_artifacts()
        self.is_loaded = (self.model is not None and self.vectorizer is not None)
        self.id2label = {
            0: "LEGITIMATE",
            1: "AMBIGUOUS",
            2: "SCAM"
        }
        if self.labels and "id2label" in self.labels:
            raw = self.labels["id2label"]
            self.id2label = {int(k): v for k, v in raw.items()}

    def predict_proba(self, text: str) -> Dict[str, float]:
        """Returns calibrated probability distribution across the three classes."""
        if not self.is_loaded:
            return {"LEGITIMATE": 0.3333, "AMBIGUOUS": 0.3334, "SCAM": 0.3333}

        clean = text.strip() if text else ""
        if not clean:
            return {"LEGITIMATE": 0.3333, "AMBIGUOUS": 0.3334, "SCAM": 0.3333}

        feat = self.vectorizer.transform([clean])
        probs = self.model.predict_proba(feat)[0]

        res = {}
        for idx in range(len(probs)):
            name = self.id2label.get(idx, f"CLASS_{idx}")
            res[name] = float(probs[idx])
        return res

    def predict(self, text: str) -> Dict[str, Any]:
        """
        Executes inference on transcript text and returns standard prediction response:
        {
            "predicted_label": "SCAM",
            "probabilities": { "LEGITIMATE": 0.05, "AMBIGUOUS": 0.10, "SCAM": 0.85 },
            "confidence": 0.85,
            "model_name": "tfidf_v3"
        }
        """
        if not self.is_loaded:
            return {
                "predicted_label": "AMBIGUOUS",
                "probabilities": {"LEGITIMATE": 0.3333, "AMBIGUOUS": 0.3334, "SCAM": 0.3333},
                "confidence": 0.3334,
                "model_name": "tfidf_v3",
                "error": "Model not loaded"
            }

        clean = text.strip() if text else ""
        if not clean:
            return {
                "predicted_label": "AMBIGUOUS",
                "probabilities": {"LEGITIMATE": 0.3333, "AMBIGUOUS": 0.3334, "SCAM": 0.3333},
                "confidence": 0.3334,
                "model_name": "tfidf_v3"
            }

        probs_dict = self.predict_proba(clean)
        top_label = max(probs_dict.items(), key=lambda x: x[1])[0]
        top_conf = round(float(probs_dict[top_label]), 4)

        # Formatted output with rounded probabilities
        formatted_probs = {k: round(v, 4) for k, v in probs_dict.items()}

        return {
            "predicted_label": top_label,
            "probabilities": formatted_probs,
            "confidence": top_conf,
            "model_name": "tfidf_v3"
        }

    def predict_batch(self, texts: list) -> list:
        """High-throughput batched inference for TF-IDF v3."""
        if not self.is_loaded:
            return [self.predict(t) for t in texts]

        clean_texts = [t.strip() if t else "" for t in texts]
        feat = self.vectorizer.transform(clean_texts)
        all_probs = self.model.predict_proba(feat)

        results = []
        for probs in all_probs:
            probs_dict = {
                self.id2label.get(idx, f"CLASS_{idx}"): float(probs[idx])
                for idx in range(len(probs))
            }
            top_label = max(probs_dict.items(), key=lambda x: x[1])[0]
            top_conf = round(float(probs_dict[top_label]), 4)
            results.append({
                "predicted_label": top_label,
                "probabilities": {k: round(v, 4) for k, v in probs_dict.items()},
                "confidence": top_conf,
                "model_name": "tfidf_v3"
            })
        return results

    def model_metadata(self) -> Dict[str, Any]:
        """Returns metadata regarding model provenance and training configuration."""
        if not self.is_loaded:
            return {"status": "UNAVAILABLE", "model_name": "tfidf_v3"}
        return {
            "model_name": "tfidf_v3",
            "architecture": self.metadata.get("model_architecture", "TF-IDF + Calibrated Logistic Regression"),
            "training_dataset": self.metadata.get("training_dataset", "data/kavach_synthetic_v3"),
            "vocabulary_size": self.metadata.get("vocabulary_size", 5000),
            "status": "LOADED"
        }

    def health_check(self) -> Dict[str, Any]:
        """Performs smoke test on sample text to verify operational readiness."""
        if not self.is_loaded:
            return {"healthy": False, "reason": "Artifacts not loaded"}
        try:
            sample_res = self.predict("Health check verification test")
            is_valid = (
                isinstance(sample_res.get("predicted_label"), str) and
                len(sample_res.get("probabilities", {})) == 3
            )
            return {"healthy": is_valid, "model_name": "tfidf_v3"}
        except Exception as e:
            return {"healthy": False, "reason": str(e)}

_GLOBAL_TFIDF_V3: Optional[TFIDFV3Classifier] = None

def get_tfidf_v3_classifier() -> TFIDFV3Classifier:
    """Singleton getter for TF-IDF v3 classifier."""
    global _GLOBAL_TFIDF_V3
    if _GLOBAL_TFIDF_V3 is None:
        _GLOBAL_TFIDF_V3 = TFIDFV3Classifier()
    return _GLOBAL_TFIDF_V3

