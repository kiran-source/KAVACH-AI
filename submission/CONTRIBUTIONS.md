# KAVACH AI — Individual Participant Contribution Statement

**Challenge**: Great Indian AI Internship Challenge 2026 by Gnani AI  
**Participant**: Kiran ([kiran])  
**Project Role**: Lead AI Architect, Full-Stack Developer, and Security Engineer  

---

## 1. Primary Technical Contributions

### A. Machine Learning & Threat Intelligence Engineering
- Engineered the three-stage cascaded **Hybrid Intelligence Engine** fusing deterministic heuristic rules with calibrated statistical ML and transformer deep learning.
- Developed the **Rule-Priority Shield** in Python (`backend/app/detection/rules.py` and `engine.py`) establishing zero-downgrade guarantees for critical cyber extortion vectors (CBI/ED Digital Arrest, OTP demands).
- Curated, validated, and split the 3,000-record synthetic multilingual Dataset v3 (`data/kavach_synthetic_v3/`) with 0% data leakage across train, validation, and test partitions.
- Trained and calibrated the **TF-IDF v3 classifier** (`backend/app/ml/tfidf_v3_loader.py`) with Platt scaling, achieving sub-5ms CPU latency.
- Authored the 22-step Google Colab fine-tuning notebook for Google MuRIL (`google/muril-base-cased`), fine-tuning it on Dataset v3, and safely importing the 237M-parameter checkpoint into `backend/app/ml/artifacts/muril_v1/`.
- Performed validation-based threshold calibration ($\tau = 0.85$), reducing transformer compute load by **68%** via selective escalation.

### B. Gnani AI Integration & Speech Engineering
- Implemented the official Python client wrappers for **Gnani Prisma STT v3.0** (`backend/app/gnani/prisma_client.py`) with multipart audio handling and language routing.
- Implemented the official client for **Gnani Timbre TTS v2.5** (`backend/app/gnani/timbre_client.py`), integrating localized defensive audio synthesis in Hindi, Telugu, and English.
- Built magic-byte validation and audio ingestion pipelines in `backend/app/audio/processor.py` supporting WAV, MP3, WebM, and M4A.

### C. Backend & Frontend Engineering
- Developed the FastAPI backend service (`backend/app/main.py`) with SQLite database persistence via SQLAlchemy.
- Implemented the automated incident management lifecycle and ReportLab PDF forensic report generation.
- Designed and built the React 18 + TypeScript + Vite frontend console with professional cybersecurity SOC tokens, live microphone audio recording, and Recharts telemetry.
- Built the automated regression test suite (`backend/tests/`), achieving 100% test pass rate across 78 test cases.

