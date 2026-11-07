# KAVACH AI — Project Discovery & Protection Report

**Author**: Senior AI/ML Architect & Security Auditor  
**Date**: 2026-11-07  
**Version**: 1.0.0-final  
**Scope**: Full repository structure, branches, components, model artifacts, API endpoints, and protection invariants.

---

## 1. Repository Structure & Git Status

- **Repository Root**: `c:\Users\kiran\OneDrive\Documents\Desktop\Kavach`
- **Active Git Branch**: `master`
- **Commit History**: 60+ atomic commits documenting development from baseline through Dataset v3 generation, Colab MuRIL training, TF-IDF v3 training, and Hybrid Intelligence Engine integration.
- **Uncommitted Changes**: Safe experimental enhancements, test suites, and documentation files strictly isolated from production baseline.

---

## 2. Inventory of Critical Components

### A. Machine Learning Artifacts
1. **Production Baseline (`backend/app/ml/artifacts/v1/`)**:
   - `model.joblib`: Calibrated Logistic Regression classifier trained on Dataset v2.
   - `vectorizer.joblib`: Subword and word n-gram TF-IDF vectorizer.
   - `metadata.json`: Model version `v1.0.0`, default production classifier.
   - **Status**: **PRESERVED & UNTOUCHED**.
2. **TF-IDF v3 Classifier (`backend/app/ml/artifacts/tfidf_v3/`)**:
   - `model.joblib`: Platt-calibrated Logistic Regression trained on Dataset v3 (2,100 train).
   - `vectorizer.joblib`: Sublinear word and character n-gram TF-IDF pipeline.
   - `checksums.sha256`: Verified SHA-256 hashes.
   - **Status**: **PRESERVED & OPERATIONAL**.
3. **Google MuRIL v1 Transformer (`backend/app/ml/artifacts/muril_v1/`)**:
   - `model.safetensors`: Fine-tuned `google/muril-base-cased` (237,558,531 parameters).
   - `tokenizer.json`, `tokenizer_config.json`, `config.json`: 197,285-token Indic vocabulary.
   - `evaluation_metrics.json`: Colab test evaluation results ($N=450$, 100% test accuracy).
   - `checksums.sha256`: Verified SHA-256 hashes.
   - **Status**: **PRESERVED & OPERATIONAL**.
4. **Original MuRIL Archive**:
   - Path: `C:\Users\kiran\Downloads\muril_v1_artifacts.zip` (884,102,010 bytes, SHA-256: `ADAF064D...`).
   - **Status**: **PRESERVED & UNMODIFIED**.

### B. Security & Safety Subsystems
1. **Rule-Priority Shield (`backend/app/detection/rules.py` & `engine.py`)**:
   - 6 threat categories: Credential Theft, Digital Arrest, Financial Coercion, Urgency/Threats, Phishing, Remote Access.
   - Hardened with active coercion checks (`ACTIVE_CRITICAL_THREAT_PATTERNS`) ensuring fake disclaimers cannot suppress active extortion.
   - Mathematical invariant: Critical rules enforce a risk floor of at least 85.0 and permanently lock status to `SCAM`.

### C. Gnani AI Technologies
1. **Gnani Prisma STT v3 (`backend/app/gnani/prisma_client.py` & `prisma_service.py`)**:
   - Handles multi-format audio uploads (WAV, MP3, WebM, M4A) and streaming chunks.
   - Provides live fallback to mock transcription when API keys are unconfigured.
2. **Gnani Timbre TTS v2.5 (`backend/app/gnani/timbre_client.py` & `prisma_service.py`)**:
   - Multilingual voice advisory synthesis (English, Hindi, Telugu).
   - Provides local TTS fallback when API keys are unconfigured.
3. **Gnani Evon v3.3**:
   - Evaluated; API returned `403 SCOPE_NOT_ALLOWED`. Not integrated. Transparently documented as optional.

### D. Application Interfaces
1. **Production Endpoints (`/api/v1/`)**:
   - `GET /health`, `GET /health/providers`, `GET /dashboard/metrics`.
   - `POST /audio/upload`, `POST /audio/recording`, `POST /transcription/{audio_id}`.
   - `POST /analysis/{transcript_id}`, `POST /analysis/text`.
   - `POST /warnings/generate`, `GET /incidents`, `POST /reports/generate`.
2. **Experimental Endpoint**:
   - `POST /api/v1/hybrid/analyze`: Isolated multi-stage hybrid analysis exposing Stage 0, Stage 1, Stage 2, and fusion telemetry.

---

## 3. Protection Policies & Invariants

1. **No Production Overwrites**: `backend/app/ml/artifacts/v1/` remains the active default.
2. **Zero Scam Downgrade**: If Stage 0 triggers a critical threat, no ML prediction can downgrade the decision.
3. **Transparent Dataset Scope**: All 3,000 Dataset v3 records carry `annotation_status: pending_review` (synthetic).
4. **No Secrets in Source Control**: `.env` is gitignored; `.env.example` provides sanitized placeholders.

