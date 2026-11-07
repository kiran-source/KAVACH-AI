"""
Model loader and artifact manager for KAVACH AI ML Classifier.
Safely loads serialized models and handles missing artifacts gracefully with fallback.
"""

import os
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any, Tuple

logger = logging.getLogger("kavach.ml.loader")

ARTIFACTS_DIR = Path(__file__).resolve().parent / "artifacts" / "v1"

_CACHED_MODEL = None
_CACHED_VECTORIZER = None
_CACHED_METADATA = None
_CACHED_LABELS = None
_LOAD_ATTEMPTED = False

def is_model_available() -> bool:
    """Checks if model artifacts are present on disk."""
    model_path = ARTIFACTS_DIR / "model.joblib"
    vectorizer_path = ARTIFACTS_DIR / "vectorizer.joblib"
    meta_path = ARTIFACTS_DIR / "metadata.json"
    return model_path.exists() and vectorizer_path.exists() and meta_path.exists()

def load_ml_artifacts() -> Tuple[Optional[Any], Optional[Any], Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
    """
    Loads and caches model, vectorizer, and metadata.
    Returns (model, vectorizer, metadata, label_mapping) or (None, None, None, None).
    """
    global _CACHED_MODEL, _CACHED_VECTORIZER, _CACHED_METADATA, _CACHED_LABELS, _LOAD_ATTEMPTED

    if _LOAD_ATTEMPTED:
        return _CACHED_MODEL, _CACHED_VECTORIZER, _CACHED_METADATA, _CACHED_LABELS

    _LOAD_ATTEMPTED = True

    if not is_model_available():
        logger.info(f"ML artifacts not found in {ARTIFACTS_DIR}. Operating in RULE_ONLY mode.")
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

        if label_path.exists():
            with open(label_path, "r", encoding="utf-8") as f:
                _CACHED_LABELS = json.load(f)
        else:
            _CACHED_LABELS = {
                "label2id": {"LEGITIMATE": 0, "AMBIGUOUS": 1, "SCAM": 2},
                "id2label": {"0": "LEGITIMATE", "1": "AMBIGUOUS", "2": "SCAM"}
            }

        logger.info(f"Successfully loaded ML model '{_CACHED_METADATA.get('model_name')}' into memory.")
        return _CACHED_MODEL, _CACHED_VECTORIZER, _CACHED_METADATA, _CACHED_LABELS
    except Exception as e:
        logger.warning(f"Failed to load ML artifacts: {str(e)}. Operating in RULE_ONLY mode.")
        _CACHED_MODEL = None
        _CACHED_VECTORIZER = None
        _CACHED_METADATA = None
        _CACHED_LABELS = None
        return None, None, None, None

