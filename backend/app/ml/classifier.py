"""
Inference engine and classifier wrapper for KAVACH AI.
"""

import numpy as np
import logging
from typing import Optional, Dict, Any

from app.ml.model_loader import load_ml_artifacts
from app.ml.preprocessing import normalize_transcript
from app.ml.schemas import MLPredictionResult

logger = logging.getLogger("kavach.ml.classifier")

class MultilingualScamClassifier:
    """
    Production-ready wrapper around the trained multilingual calibrated classifier.
    Operates on transcripts and outputs calibrated probability distributions.
    """
    def __init__(self):
        self.model, self.vectorizer, self.metadata, self.labels = load_ml_artifacts()
        self.is_loaded = (self.model is not None and self.vectorizer is not None)

    def predict(self, text: str) -> Optional[MLPredictionResult]:
        """
        Runs inference on transcript text. Returns MLPredictionResult or None if model unavailable.
        """
        if not self.is_loaded:
            return None

        clean_text = normalize_transcript(text)
        if not clean_text:
            return MLPredictionResult(
                predicted_class="AMBIGUOUS",
                confidence=0.34,
                probabilities={"LEGITIMATE": 0.33, "AMBIGUOUS": 0.34, "SCAM": 0.33},
                model_version=self.metadata.get("model_name", "v1.0"),
                model_name=self.metadata.get("model_architecture", "TF-IDF + Calibrated Logistic"),
                uncertainty=1.0,
                is_abstaining=True
            )

        try:
            vec = self.vectorizer.transform([clean_text])
            probs = self.model.predict_proba(vec)[0]
            
            # Map probabilities to class names
            id2label = self.labels.get("id2label", {})
            class_probs = {}
            for idx, p in enumerate(probs):
                name = id2label.get(str(idx), id2label.get(idx, f"CLASS_{idx}"))
                class_probs[name] = round(float(p), 4)

            top_idx = int(np.argmax(probs))
            top_label = id2label.get(str(top_idx), id2label.get(top_idx, "AMBIGUOUS"))
            top_conf = float(probs[top_idx])

            # Calculate uncertainty using difference between top 2 probabilities
            sorted_probs = np.sort(probs)[::-1]
            margin = sorted_probs[0] - sorted_probs[1] if len(sorted_probs) > 1 else 1.0
            uncertainty = round(float(1.0 - margin), 4)

            # Abstain if top confidence is too low or margin is negligible (< 0.10)
            is_abstaining = bool(top_conf < 0.45 or margin < 0.08)

            return MLPredictionResult(
                predicted_class=top_label,
                confidence=round(top_conf, 4),
                probabilities=class_probs,
                model_version=self.metadata.get("model_name", "v1.0"),
                model_name=self.metadata.get("model_architecture", "TF-IDF + Calibrated Logistic"),
                uncertainty=uncertainty,
                is_abstaining=is_abstaining
            )
        except Exception as e:
            logger.error(f"ML inference error: {str(e)}")
            return None

_GLOBAL_CLASSIFIER: Optional[MultilingualScamClassifier] = None

def get_classifier() -> MultilingualScamClassifier:
    global _GLOBAL_CLASSIFIER
    if _GLOBAL_CLASSIFIER is None:
        _GLOBAL_CLASSIFIER = MultilingualScamClassifier()
    return _GLOBAL_CLASSIFIER
