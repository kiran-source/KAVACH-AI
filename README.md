# 🛡️ KAVACH AI — Multilingual Voice Scam Detection & Incident Response Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-cyan.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-teal.svg)](https://fastapi.tiangolo.com/)
[![React 18](https://img.shields.io/badge/React-18-61dafb.svg)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.2-blue.svg)](https://www.typescriptlang.org/)
[![Vite](https://img.shields.io/badge/Vite-5.1-purple.svg)](https://vitejs.dev/)
[![Gnani AI](https://img.shields.io/badge/Gnani%20AI-Prisma%20v3.0%20%26%20Timbre%20v2.5-orange.svg)](https://www.gnani.ai/)

**KAVACH AI** (కవచ్ / कवच) is a specialized, privacy-preserving, AI-assisted security decision-support platform engineered for the **Great Indian AI Internship Challenge (organised by Gnani AI)**.

It protects Indian citizens and enterprise SOCs against advanced voice social-engineering attacks—including **Digital Arrest rackets**, **CBI/Police impersonation**, **Bank KYC & OTP theft**, **Remote Access APK sideloading**, and **Customs contraband extortion**—with native support for **Telugu**, **Hindi**, **English**, and code-mixed conversations (**Telugu-English** and **Hindi-English**).

> 📄 **Executive Summary & Submission Pitch**:
> - 📖 **[Read the 1-Page Solution Pitch (Markdown)](SOLUTION_PITCH.md)**
> - 📥 **[Download the Official 1-Page Pitch (PDF)](submission/ONE_PAGE_SOLUTION_PITCH.pdf)**
> - 📦 **[Submission Verification & Package Dossier](submission/SUBMISSION_DOSSIER.md)**

---

## 🌟 Key Highlights & System Capabilities

1. **Official Gnani AI Integration**:
   - **Gnani Prisma v3.0 STT** (`POST https://api.vachana.ai/stt/v3`): High-fidelity Speech-to-Text with automatic Language Identification (LID) and timestamped segment extraction. Authenticated via `X-API-Key-ID` header.
   - **Gnani Timbre v2.5 TTS** (`POST https://api.vachana.ai/api/v1/tts/inference`): Localized acoustic voice safety warning synthesis using official voices (`Nalini` for Hindi/English and `Chitra` for Telugu/Tenglish), providing victim guidance in the detected conversation language.
   - **Evon Status & Text Generation**: Hosted Evon text generation was probed via `https://api.vachana.ai/v1/chat/completions` and returned `403 SCOPE_NOT_ALLOWED` (Gnani Evon v3.3 is an open-weights 30B foundation model whose hosted inference scope is not provisioned on standard challenge API keys). To ensure 100% reliable challenge compliance without unauthorized third-party LLMs, text generation was executed via the **Domain-Curated Multilingual Scenario Engine**.

2. **Explainable 8-Pillar Threat Detection Engine**:
   - Deterministic, explainable rule-based scoring engine analyzing:
     1. *Authority Impersonation* (Police, CBI, Customs, Supreme Court, TRAI, ED)
     2. *Urgency & Coercive Threats* (Arrest threats, account freeze, electricity cutoff)
     3. *Credential Theft* (OTP, UPI PIN, CVV, ATM passwords, net banking credentials)
     4. *Remote Access Manipulation* (AnyDesk, TeamViewer, QuickSupport, APK downloads)
     5. *Financial Redirection Fraud* (Safe government accounts, security deposits, fee advancement)
     6. *Psychological Isolation* (Commands to isolate from family, lock room doors)
     7. *Courier & Customs Contraband Fraud* (FedEx/DHL narcotics and customs allegations)
     8. *Digital Arrest Patterns* (Continuous Skype/Zoom video surveillance)

3. **Hybrid Intelligence Threat Detection Engine & Machine Learning Architecture**:
   - **Production Baseline v1.0** (`backend/app/ml/artifacts/v1/`): Platt-calibrated Logistic Regression baseline trained locally on the 350-sample training split of Dataset v2. Serves as active default. Measured CPU latency: Mean: 11.68 ms, P50: 10.27 ms, P95: 23.06 ms.
   - **TF-IDF v3 Fast-Path Classifier** (`backend/app/ml/artifacts/tfidf_v3/`): Subword and character n-gram calibrated classifier trained on the 2,100-sample training partition of Dataset v3. Resolves standard calls in **4.29 ms** mean CPU latency (~42 MB footprint).
   - **Google MuRIL v1 Transformer** (`backend/app/ml/artifacts/muril_v1/`): Fine-tuned `google/muril-base-cased` transformer (237M parameters) for deep contextual and code-mixed threat comprehension across 17 Indian languages. CPU latency: ~1,543 ms.
   - **Cascaded Selective Escalation Pipeline** (`POST /api/v1/hybrid/analyze`):
     $$\text{Stage 0: Rule Shield} \longrightarrow \text{Stage 1: TF-IDF v3 (Fast Path)} \longrightarrow \text{Stage 2: Selective MuRIL v1 (Deep Path)}$$
     Under the validation-calibrated threshold ($\tau = 0.85$), TF-IDF handles ~68% of calls in <5 ms, invoking MuRIL for only ~32% of ambiguous or code-mixed calls. Reduces transformer compute overhead by **68%** while achieving 100% accuracy and 0 false negatives on the held-out test partition.
   - **Rule-Priority Shield**: Guarantees that critical social-engineering indicators (OTP theft, Digital Arrest, AnyDesk remote control, rule score $\ge 50$) can never be downgraded by statistical machine learning predictions. Enforces a permanent risk floor of $\ge 85.0$ and severity `Critical`.
   - **Educational Precedence Shield**: Public security advisories (e.g. Bank/RBI warnings) take precedence when no active demands are made, preventing false alarms on educational materials.
   - **Resilience & Fallback**: Automatically falls back to Stage 1 TF-IDF and deterministic rules if transformer weights are unavailable or if a forward pass exception occurs.

4. **Negative Context False-Positive Guard**:
   - Contextual heuristics distinguish genuine scam coercion from **bank security awareness broadcasts** and legitimate telecom warnings (e.g., "RBI never asks for your OTP").

5. **Consent-Based Audio Ingestion & Microphone Analysis**:
   - **File Upload Workflow**: Validates WAV, MP3, M4A, FLAC, and WebM files up to 25 MB.
   - **Consent-Based Microphone Workflow**: User explicitly grants microphone permissions in browser. Audio is recorded and transmitted in chunked batches for near-real-time transcription. **Does NOT intercept cellular phone calls** (strictly compliant with Indian telecom privacy regulations).

6. **SOC Incident Response & ReportLab PDF Generation**:
   - SQLite persistent storage via SQLAlchemy.
   - Full incident status lifecycle (`New` → `Under Review` → `Confirmed Suspicious` / `False Positive` → `Resolved`).
   - Incident timeline tracking, case notes, evidence linking, and downloadable forensic PDF dossiers generated via ReportLab.

---

## 💻 System Architecture

```
                          ┌─────────────────────────────────────┐
                          │     REACT FRONTEND (Vite + TS)      │
                          │   SOC Dashboard · Audio Analysis   │
                          │   Live Chunk Scan · Incidents · PDF │
                          └──────────────────┬──────────────────┘
                                             │ REST API (localhost:8000)
                                             ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                FASTAPI BACKEND (Python 3.12+)                          │
│                                                                                        │
│  ┌───────────────────────┐      ┌─────────────────────────┐      ┌──────────────────┐  │
│  │ Audio Ingestion Module│ ───► │ Gnani Prisma v3.0 STT   │ ───► │ Threat Detection │  │
│  │ MIME & Chunk Safety   │      │ Multilingual ASR & LID  │      │ 8 Threat Pillars │  │
│  │ Canonical WAV Headers │      │ Timestamped Segments    │      │ Context Guard    │  │
│  └───────────────────────┘      └─────────────────────────┘      └────────┬─────────┘  │
│                                                                           │            │
│  ┌───────────────────────┐      ┌─────────────────────────┐               │            │
│  │ Gnani Timbre v2.5 TTS │ ◄─── │ Explainable Risk Engine │ ◄─────────────┘            │
│  │ Nalini / Chitra Voice │      │ 0-100 Score & Synergy   │                            │
│  │ 16kHz Mono RIFF/WAVE  │      │ Severity Classification │                            │
│  └───────────────────────┘      └────────────┬────────────┘                            │
│                                              │                                         │
│  ┌───────────────────────┐      ┌────────────▼────────────┐      ┌──────────────────┐  │
│  │ SOC PDF Report Engine │ ◄─── │ Incident Management     │ ───► │ SQLite Database  │  │
│  │ ReportLab Dossiers    │      │ Timeline & Case Journal │      │ SQLAlchemy ORM   │  │
│  └───────────────────────┘      └─────────────────────────┘      └──────────────────┘  │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 Synthetic Multilingual Datasets (`v1` & `v2`)

The repository includes two distinct, domain-curated synthetic datasets designed for multilingual scam research under Indian telecom constraints:

### 1. Acoustic Benchmark Dataset (`data/kavach_synthetic_v1/`)
- **Total Conversations**: Exactly 100 domain-curated conversations.
- **Classification Balance**:
  - `SCAM`: 40 (40%)
  - `LEGITIMATE`: 35 (35%)
  - `AMBIGUOUS`: 25 (25%)
- **Language Balance**: Exactly 20 conversations per language category (English, Hindi, Telugu, Telugu-English, Hindi-English).
- **Stratified Balance**: Exactly 8 SCAM, 7 LEGITIMATE, and 5 AMBIGUOUS in every language category.
- **Dialogue Structure**: Exactly 8 alternating turns per conversation (caller / recipient).
- **Speech Audio Inventory**: Exactly 20 canonical WAV audio files (4 per language category):
  - 5 Stage 2 Pilot files (4.00s duration each, baseline benchmark).
  - 15 Stage 3 Bulk files synthesized live via **Gnani Timbre v2.5** (17.92s to 24.16s each, speech RMS energy 0.073 to 0.178).
  - **Total Measured Audio Duration**: **331.84 seconds** (all valid 16,000 Hz 16-bit mono canonical RIFF/WAVE headers; zero streaming chunk defects).
- **Scenario-Grouped Splits (70 / 15 / 15)**: `splits/train.jsonl` (70 records), `splits/validation.jsonl` (15 records), `splits/test.jsonl` (15 records).

### 2. Expanded ML Training & Evaluation Corpus (`data/kavach_synthetic_v2/`)
- **Total Conversations**: Exactly 500 domain-curated conversations across 5 language categories (100 per language).
- **Purpose**: Powering local TF-IDF classifier training, cross-validation, and held-out benchmark evaluation.
- **Strict Scenario-Family Splits (70 / 15 / 15)**:
  - `splits/train.jsonl`: 350 conversations (140 Scam, 120 Legit, 90 Ambig; 70 per language).
  - `splits/validation.jsonl`: 75 conversations (30 Scam, 25 Legit, 20 Ambig; 15 per language).
  - `splits/test.jsonl`: 75 conversations (30 Scam, 30 Legit, 15 Ambig; 15 per language).
- **Zero Leakage**: Exactly **0% CID leakage, 0% scenario family overlap, and 0% exact dialogue text hash overlap** across splits.
- **Dialogue Diversity**: Variable lengths (4, 6, 8, 10 turns), 5 recipient personas (Skeptic, Anxious, Executive, Senior, Security-Aware), 4 caller tones, subtle scams, and realistic legitimate inquiries discussing OTPs and security.
- **Truthful Status**: All 500 records are labeled `review_status: "pending_review"` with zero fabricated human-review claims.
- **Automated PII Scanning**: Automated regex pattern scans confirm zero valid credit card numbers, Aadhaar numbers, or personal caller identities across both datasets.

### 3. Production Benchmark & Transformer Corpus (`data/kavach_synthetic_v3/`)
- **Total Conversations**: Exactly 3,000 domain-curated conversations across 5 language categories (600 per language).
- **Purpose**: Powering TF-IDF v3 training, MuRIL transformer fine-tuning, threshold calibration, and fair head-to-head benchmarking.
- **Scenario-Family Splits (70 / 15 / 15)**:
  - `splits/train.jsonl`: 2,100 conversations (840 Scam, 630 Legit, 630 Ambig; 420 per language).
  - `splits/validation.jsonl`: 450 conversations (180 Scam, 135 Legit, 135 Ambig; 90 per language).
  - `splits/test.jsonl`: 450 conversations (180 Scam, 135 Legit, 135 Ambig; 90 per language).
- **Zero Leakage**: 0% conversation ID overlap, 0% scenario family overlap, 0% dialogue text hash overlap.
- **Limitation Disclosure**: All 3,000 records carry `annotation_status: "pending_review"` (synthetic). High benchmark accuracy does not establish wild telephony accuracy.

---

## ⚙️ Configuration & Environment Variables

Local configuration is managed canonically via `backend/.env` (excluded from version control). An example template is provided in `backend/.env.example`:

| Variable | Default Value | Description |
|---|---|---|
| `GNANI_API_KEY` | `""` | Official Gnani API Key for Prisma & Timbre. Must be kept confidential. |
| `DEMO_MODE` | `"false"` | When `false` (Real Mode), application makes authenticated calls to Gnani APIs and fails at startup if key is missing. When `true` (Demo Mode), application uses deterministic local simulation. |
| `GNANI_PRISMA_ENDPOINT` | `https://api.vachana.ai/stt/v3` | Official endpoint for Gnani Prisma STT v3.0. |
| `GNANI_TIMBRE_ENDPOINT` | `https://api.vachana.ai/api/v1/tts/inference` | Official endpoint for Gnani Timbre TTS v2.5. |
| `DATABASE_URL` | `sqlite:///./kavach.db` | SQLite database file location. |
| `HOST` | `127.0.0.1` | Local bind address (enforces localhost security). |
| `PORT` | `8000` | FastAPI server port. |
| `MAX_UPLOAD_SIZE_MB` | `25` | Maximum permissible audio upload size. |
| `RETENTION_DAYS` | `7` | Retention schedule for uploaded audio files. |

> **Security Rule**: The application strictly refuses to start silently in Demo Mode if `DEMO_MODE=false` is configured without a valid `GNANI_API_KEY`. Secrets are never hardcoded or logged.

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.12+ (Python 3.13 tested and verified)
- Node.js 20+ (Node.js 24 LTS verified)
- Windows 10/11 or Linux host

### 1. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate  # On Windows

# Install Python dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and insert your GNANI_API_KEY (or set DEMO_MODE=true for simulation)
```

### 2. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install Node dependencies
npm install

# Verify TypeScript compilation and production build
npm run build
```

### 3. Running the Application
```bash
# In Terminal 1 (Backend):
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

# In Terminal 2 (Frontend):
cd frontend
npm run dev
```

- **Frontend Application**: [`http://localhost:5173`](http://localhost:5173)
- **FastAPI Interactive Docs**: [`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs)
- **API Health Check**: [`http://127.0.0.1:8000/api/v1/health`](http://127.0.0.1:8000/api/v1/health)

---

## 🧪 Testing & Verification

The backend test suite is located in `backend/tests/` and runs with standard Pytest.

### Running Pytest
```bash
# Run all tests
pytest backend/tests/ -v
```

### Verified Test Passes
- **Test Run (Full Backend & Hybrid Engine Regression Suite)**:
  - **78 passed in 39.28s** (Exit Code: 0, 100% pass rate)
  - Covers API health, Gnani Prisma STT v3, Gnani Timbre TTS v2.5, 8-pillar rule engine, calibrated ML classifiers (v1 and v3), MuRIL v1 transformer loading and CPU inference, dynamic selective escalation, uncertainty estimation, rule-priority shield (enforcing zero downgrades for critical threats), educational context precedence, adversarial disclaimer override, abstention fallback, and recording format validation.

### Dataset & Audio Verification Scripts
```bash
# Verify Audio Integrity and RIFF headers
python scripts/repair_audio_integrity.py

# Verify 70/15/15 Dataset Splits & Zero Leakage
python scripts/verify_splits.py

# Reconcile API Usage Ledger
python scripts/reconcile_api_ledger.py

# Validate 100 Conversations and Generate Reports
python scripts/generate_fresh_dataset_reports.py
```

---

## 🔒 Security & Local Prototype Boundaries

- **Local Prototype Scope**: This platform is designed as an evaluation prototype and proof-of-concept. It is NOT hardened for multi-tenant public deployment without SSO/OAuth2, rate limiting, and managed KMS secret storage.
- **Localhost Binding**: Binds strictly to `127.0.0.1` to prevent unauthorized external network access.
- **Sanitized Uploads**: Filenames are sanitized, paths are resolved strictly within upload directories to prevent path traversal attacks, and uploaded files are validated for valid MIME/WAV headers.
- **Zero API Key Exposure**: Secrets are isolated to `backend/.env` and never transmitted to frontend clients or committed to git archives.

---

## ⚖️ Legal Disclaimer
**KAVACH AI is an AI-assisted decision-support system, not an autonomous legal or telecom interceptor.** Threat scores and scam tactic classifications are algorithmic recommendations based on speech transcription and heuristics. In case of active fraud, contact the National Cybercrime Helpline at **1930** or visit **https://cybercrime.gov.in**.

---

**Developed for the Great Indian AI Internship Challenge — Gnani AI.**
