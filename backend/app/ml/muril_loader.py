"""
Artifact loader and state manager for fine-tuned MuRIL classifier.
Separated from the production baseline artifacts (backend/app/ml/artifacts/v1/).
Handles missing PyTorch / HuggingFace dependencies, CPU/CUDA selection, and un-downloaded weights gracefully.
"""

import os
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any, Tuple

logger = logging.getLogger("kavach.ml.muril_loader")

MURIL_ARTIFACTS_DIR = Path(__file__).resolve().parent / "artifacts" / "muril_v1"

_CACHED_MURIL_MODEL = None
_CACHED_MURIL_TOKENIZER = None
_CACHED_MURIL_METADATA = None
_CACHED_MURIL_LABELS = None
_CACHED_DEVICE = "cpu"
_MURIL_LOAD_ATTEMPTED = False

def is_muril_available() -> bool:
    """Checks if fine-tuned MuRIL model weights and tokenizer exist on disk."""
    if not MURIL_ARTIFACTS_DIR.exists():
        return False

    has_weights = (
        (MURIL_ARTIFACTS_DIR / "model.safetensors").exists() or
        (MURIL_ARTIFACTS_DIR / "pytorch_model.bin").exists()
    )
    has_tokenizer = (
        (MURIL_ARTIFACTS_DIR / "tokenizer_config.json").exists() or
        (MURIL_ARTIFACTS_DIR / "tokenizer.json").exists() or
        (MURIL_ARTIFACTS_DIR / "vocab.txt").exists()
    )
    has_config = (MURIL_ARTIFACTS_DIR / "config.json").exists()
    return has_weights and has_tokenizer and has_config

def get_device() -> str:
    """Returns 'cuda' if CUDA is available, else 'cpu'."""
    global _CACHED_DEVICE
    try:
        import torch
        if torch.cuda.is_available():
            _CACHED_DEVICE = "cuda"
        else:
            _CACHED_DEVICE = "cpu"
    except Exception:
        _CACHED_DEVICE = "cpu"
    return _CACHED_DEVICE

def load_muril_artifacts() -> Tuple[Optional[Any], Optional[Any], Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
    """
    Safely loads fine-tuned MuRIL model and tokenizer if present.
    Returns (model, tokenizer, metadata, label_mapping) or (None, None, metadata, label_mapping).
    """
    global _CACHED_MURIL_MODEL, _CACHED_MURIL_TOKENIZER, _CACHED_MURIL_METADATA, _CACHED_MURIL_LABELS, _MURIL_LOAD_ATTEMPTED

    if _MURIL_LOAD_ATTEMPTED:
        return _CACHED_MURIL_MODEL, _CACHED_MURIL_TOKENIZER, _CACHED_MURIL_METADATA, _CACHED_MURIL_LABELS

    _MURIL_LOAD_ATTEMPTED = True

    # 1. Load metadata and label mapping
    meta_path = MURIL_ARTIFACTS_DIR / "metadata.json"
    label_path = MURIL_ARTIFACTS_DIR / "label_mapping.json"

    if meta_path.exists():
        try:
            with open(meta_path, "r", encoding="utf-8") as f:
                _CACHED_MURIL_METADATA = json.load(f)
        except Exception:
            _CACHED_MURIL_METADATA = {}
    else:
        _CACHED_MURIL_METADATA = {"model_name": "muril_v1", "status": "pending_import"}

    if label_path.exists():
        try:
            with open(label_path, "r", encoding="utf-8") as f:
                _CACHED_MURIL_LABELS = json.load(f)
        except Exception:
            _CACHED_MURIL_LABELS = {
                "label2id": {"LEGITIMATE": 0, "AMBIGUOUS": 1, "SCAM": 2},
                "id2label": {"0": "LEGITIMATE", "1": "AMBIGUOUS", "2": "SCAM"}
            }
    else:
        _CACHED_MURIL_LABELS = {
            "label2id": {"LEGITIMATE": 0, "AMBIGUOUS": 1, "SCAM": 2},
            "id2label": {"0": "LEGITIMATE", "1": "AMBIGUOUS", "2": "SCAM"}
        }

    # 2. Check if model files exist
    if not is_muril_available():
        logger.warning(f"MuRIL artifacts not found in {MURIL_ARTIFACTS_DIR}.")
        return None, None, _CACHED_MURIL_METADATA, _CACHED_MURIL_LABELS

    # 3. Attempt loading with transformers and torch
    try:
        import torch
        from transformers import AutoModelForSequenceClassification, AutoTokenizer

        device = get_device()
        logger.info(f"Loading fine-tuned MuRIL transformer from {MURIL_ARTIFACTS_DIR} on device '{device}'...")

        _CACHED_MURIL_TOKENIZER = AutoTokenizer.from_pretrained(str(MURIL_ARTIFACTS_DIR))
        _CACHED_MURIL_MODEL = AutoModelForSequenceClassification.from_pretrained(str(MURIL_ARTIFACTS_DIR))
        _CACHED_MURIL_MODEL.to(device)
        _CACHED_MURIL_MODEL.eval()

        logger.info(f"Successfully loaded fine-tuned MuRIL transformer on device '{device}'.")
        return _CACHED_MURIL_MODEL, _CACHED_MURIL_TOKENIZER, _CACHED_MURIL_METADATA, _CACHED_MURIL_LABELS
    except ImportError:
        logger.warning("PyTorch or Transformers not installed in current Python environment. MuRIL inference disabled.")
        return None, None, _CACHED_MURIL_METADATA, _CACHED_MURIL_LABELS
    except Exception as e:
        logger.error(f"Error loading MuRIL transformer: {e}")
        return None, None, _CACHED_MURIL_METADATA, _CACHED_MURIL_LABELS
