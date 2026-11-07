"""
MuRIL Multilingual Sequence Classification Wrapper for KAVACH AI.
Provides clean inference interface with predict, predict_proba, model_metadata, and health_check.
Operates seamlessly on CPU or CUDA.
"""

import logging
from typing import Optional, Dict, Any
import numpy as np

from app.ml.muril_loader import load_muril_artifacts, is_muril_available, get_device

logger = logging.getLogger("kavach.ml.muril_classifier")

class MuRILClassifier:
    """
    Production-ready wrapper around fine-tuned Google MuRIL sequence classification model.
    Evaluates multilingual/code-mixed conversational transcripts.
    """
    def __init__(self):
        self.model, self.tokenizer, self.metadata, self.labels = load_muril_artifacts()
        self.is_loaded = (self.model is not None and self.tokenizer is not None)
        self.device = get_device()
        self.id2label = {
            0: "LEGITIMATE",
            1: "AMBIGUOUS",
            2: "SCAM"
        }
        if self.labels and "id2label" in self.labels:
            raw = self.labels["id2label"]
            self.id2label = {int(k): v for k, v in raw.items()}

    def predict_proba(self, text: str) -> Dict[str, float]:
        """
        Runs tokenizer and forward pass through MuRIL, returning normalized softmax probabilities.
        """
        if not self.is_loaded:
            return {"LEGITIMATE": 0.3333, "AMBIGUOUS": 0.3334, "SCAM": 0.3333}

        clean = text.strip() if text else ""
        if not clean:
            return {"LEGITIMATE": 0.3333, "AMBIGUOUS": 0.3334, "SCAM": 0.3333}

        try:
            import torch
            inputs = self.tokenizer(
                clean,
                truncation=True,
                max_length=256,
                padding=True,
                return_tensors="pt"
            )
            inputs = {k: v.to(self.device) for k, v in inputs.items()}

            with torch.no_grad():
                outputs = self.model(**inputs)
                logits = outputs.logits
                probs = torch.softmax(logits, dim=-1)[0].cpu().numpy()

            res = {}
            for idx in range(len(probs)):
                name = self.id2label.get(idx, f"CLASS_{idx}")
                res[name] = float(probs[idx])
            return res
        except Exception as e:
            logger.error(f"MuRIL predict_proba error: {e}")
            return {"LEGITIMATE": 0.3333, "AMBIGUOUS": 0.3334, "SCAM": 0.3333}

    def predict(self, text: str) -> Dict[str, Any]:
        """
        Runs MuRIL inference on transcript text. Returns standardized prediction dictionary:
        {
            "predicted_label": "SCAM",
            "probabilities": { "LEGITIMATE": 0.05, "AMBIGUOUS": 0.10, "SCAM": 0.85 },
            "confidence": 0.85,
            "model_name": "muril_v1"
        }
        """
        if not self.is_loaded:
            return {
                "predicted_label": "AMBIGUOUS",
                "probabilities": {"LEGITIMATE": 0.3333, "AMBIGUOUS": 0.3334, "SCAM": 0.3333},
                "confidence": 0.3334,
                "model_name": "muril_v1",
                "status": "UNAVAILABLE"
            }

        clean = text.strip() if text else ""
        if not clean:
            return {
                "predicted_label": "AMBIGUOUS",
                "probabilities": {"LEGITIMATE": 0.3333, "AMBIGUOUS": 0.3334, "SCAM": 0.3333},
                "confidence": 0.3334,
                "model_name": "muril_v1"
            }

        probs_dict = self.predict_proba(clean)
        top_label = max(probs_dict.items(), key=lambda x: x[1])[0]
        top_conf = round(float(probs_dict[top_label]), 4)

        formatted_probs = {k: round(v, 4) for k, v in probs_dict.items()}

        return {
            "predicted_label": top_label,
            "probabilities": formatted_probs,
            "confidence": top_conf,
            "model_name": "muril_v1"
        }

    def predict_batch(self, texts: list, batch_size: int = 32) -> list:
        """High-throughput batched inference across multiple transcripts."""
        if not self.is_loaded:
            return [self.predict(t) for t in texts]

        results = []
        try:
            import torch
            for i in range(0, len(texts), batch_size):
                chunk = [t.strip() if t else "" for t in texts[i:i + batch_size]]
                inputs = self.tokenizer(
                    chunk,
                    truncation=True,
                    max_length=256,
                    padding=True,
                    return_tensors="pt"
                )
                inputs = {k: v.to(self.device) for k, v in inputs.items()}

                with torch.no_grad():
                    logits = self.model(**inputs).logits
                    probs = torch.softmax(logits, dim=-1).cpu().numpy()

                for p in probs:
                    probs_dict = {
                        self.id2label.get(idx, f"CLASS_{idx}"): float(p[idx])
                        for idx in range(len(p))
                    }
                    top_label = max(probs_dict.items(), key=lambda x: x[1])[0]
                    top_conf = round(float(probs_dict[top_label]), 4)
                    results.append({
                        "predicted_label": top_label,
                        "probabilities": {k: round(v, 4) for k, v in probs_dict.items()},
                        "confidence": top_conf,
                        "model_name": "muril_v1"
                    })
            return results
        except Exception as e:
            logger.error(f"MuRIL predict_batch error: {e}")
            return [self.predict(t) for t in texts]

    def model_metadata(self) -> Dict[str, Any]:
        """Returns metadata regarding fine-tuned MuRIL transformer."""
        if not self.is_loaded:
            return {
                "status": "UNAVAILABLE",
                "model_name": "muril_v1",
                "reason": "Weights or PyTorch runtime not loaded"
            }
        return {
            "model_name": "muril_v1",
            "base_checkpoint": self.metadata.get("base_checkpoint", "google/muril-base-cased"),
            "architecture": self.metadata.get("architecture", "BertForSequenceClassification"),
            "num_parameters": self.metadata.get("num_parameters", 237558531),
            "device": self.device,
            "status": "LOADED"
        }

    def health_check(self) -> Dict[str, Any]:
        """Executes a smoke test to verify operational readiness."""
        if not self.is_loaded:
            return {"healthy": False, "reason": "Model weights or runtime not loaded"}
        try:
            sample_res = self.predict("Health check verification test")
            is_valid = (
                isinstance(sample_res.get("predicted_label"), str) and
                len(sample_res.get("probabilities", {})) == 3
            )
            return {"healthy": is_valid, "model_name": "muril_v1", "device": self.device}
        except Exception as e:
            return {"healthy": False, "reason": str(e)}

_GLOBAL_MURIL: Optional[MuRILClassifier] = None

def get_muril_classifier() -> MuRILClassifier:
    """Singleton getter for MuRIL classifier."""
    global _GLOBAL_MURIL
    if _GLOBAL_MURIL is None:
        _GLOBAL_MURIL = MuRILClassifier()
    return _GLOBAL_MURIL
