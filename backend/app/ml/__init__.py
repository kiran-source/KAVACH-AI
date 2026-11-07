"""
KAVACH AI Machine Learning and Hybrid Detection Module
"""

from app.ml.schemas import MLPredictionResult, HybridAnalysisResult
from app.ml.model_loader import load_ml_artifacts, is_model_available
from app.ml.classifier import get_classifier, MultilingualScamClassifier
from app.ml.fusion import perform_hybrid_analysis

__all__ = [
    "MLPredictionResult",
    "HybridAnalysisResult",
    "load_ml_artifacts",
    "is_model_available",
    "get_classifier",
    "MultilingualScamClassifier",
    "perform_hybrid_analysis"
]

