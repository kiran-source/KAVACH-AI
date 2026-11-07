# KAVACH AI — System Architecture & Technical Specification

## 1. Executive Summary
**KAVACH AI** (కవచ్ / कवच) is a specialized, privacy-preserving, AI-assisted security decision-support platform designed to protect Indian citizens and institutions against phone-based voice social-engineering attacks (vishing, digital arrest, and financial fraud). 

The platform accepts uploaded audio and consent-based microphone recordings, utilizes **Gnani Prisma v3.0** for multilingual speech-to-text transcription across Indian languages, evaluates transcripts using a **Hybrid Risk Engine** fusing an explainable 8-pillar deterministic threat engine with a **Calibrated Multilingual Machine Learning Classifier**, synthesizes immediate defensive voice warnings using **Gnani Timbre v2.5**, and powers a comprehensive SOC incident management dashboard with ReportLab PDF audit export.

---

## 2. Target Deployment & Hardware Profile
KAVACH AI is optimized to execute reliably on standard consumer or enterprise developer workstations without requiring local GPUs:
- **Host OS**: Windows 10/11 (64-bit), macOS, or Linux
- **Python Runtime**: Python 3.10–3.13 (FastAPI, scikit-learn, SQLAlchemy, ReportLab)
- **Node.js Runtime**: Node.js 18+ LTS (React, TypeScript, Vite, Tailwind CSS)
- **Local Storage**: Zero-configuration SQLite (`kavach.db`), total local memory footprint < 600 MB
- **Network**: Bound to `127.0.0.1` localhost; outbound HTTPS to Gnani AI endpoints (`api.vachana.ai`) for speech inference.

---

## 3. High-Level Architectural Diagram

```
       +-----------------------------------------------------------+
       |                     REACT FRONTEND                        |
       |  Vite + TypeScript + Tailwind CSS + Lucide + Recharts    |
       |  - Audio Upload & Near-Realtime Microphone Recording      |
       |  - Real-time Threat Badges & Severity Gauge               |
       |  - SOC Incident Workbench & Timeline Audit                |
       +-----------------------------+-----------------------------+
                                     |
                                     | REST API (HTTP/JSON + Multipart)
                                     v
+--------------------------------------------------------------------------+
|                          FASTAPI BACKEND SERVICE                         |
|                                                                          |
|  +--------------------------+          +------------------------------+  |
|  |  AUDIO INGESTION ENGINE  |          |    GNANI PRISMA v3.0 STT     |  |
|  |  - Magic-Byte Validation | -------> |   - Multilingual ASR (v3)    |  |
|  |  - Audio Conversion      |          |   - Language Identification  |  |
|  |  - Wave/SoundFile Meta   |          |   - Timestamped Segments     |  |
|  |  - Path Traversal Guard  |          |   - Bounded Exponential Retry|  |
|  +--------------------------+          +--------------+---------------+  |
|                                                       |                  |
|                                                       v                  |
|  +--------------------------------------------------------------------+  |
|  |                       HYBRID RISK FUSION ENGINE                    |  |
|  |                                                                    |  |
|  |  +-----------------------------+    +---------------------------+  |  |
|  |  |  8-PILLAR RULE ENGINE       |    | CALIBRATED ML CLASSIFIER  |  |  |
|  |  |  - Authority Impersonation  |    | - TF-IDF (1-2 word ngrams)|  |  |
|  |  |  - Digital Arrest Patterns  |    | - Platt Scaled LogReg     |  |  |
|  |  |  - Credential Theft (OTP)   |    | - Uncertainty & Abstain   |  |  |
|  |  |  - Remote Control (AnyDesk) |    | - Measured CPU (~10ms)    |  |  |
|  |  |  - Negative Context Guard   |    +-------------+-------------+  |  |
|  |  +--------------+--------------+                  |                |  |
|  |                 |                                 |                |  |
|  |                 +----------------+----------------+                |  |
|  |                                  v                                 |  |
|  |                 +--------------------------------+                 |  |
|  |                 |      RULE-PRIORITY SHIELD      |                 |  |
|  |                 |  - Disallow ML false negatives |                 |  |
|  |                 |  - Conflict & Divergence Flag  |                 |  |
|  |                 |  - Graceful RULE_ONLY Fallback |                 |  |
|  |                 +----------------+---------------+                 |  |
|  +----------------------------------+---------------------------------+  |
|                                     |                                    |
|                                     v                                    |
|  +--------------------------+          +------------------------------+  |
|  |  GNANI TIMBRE v2.5 TTS   |          |     INCIDENT MANAGEMENT      |  |
|  |  - Multilingual Advisory | <------- |     - State Transitions      |  |
|  |  - Telugu, Hindi, English|          |     - Audit Timeline Log     |  |
|  |  - SAPI / WAV Fallback   |          |     - SOC Analyst Notes      |  |
|  +--------------------------+          +--------------+---------------+  |
|                                                       |                  |
|                                                       v                  |
|  +--------------------------+          +------------------------------+  |
|  |   SOC PDF GENERATOR      |          |     SQLITE DB (SQLAlchemy)   |  |
|  |   - ReportLab Engine     | <------- |     - Audio, Transcripts     |  |
|  |   - Hybrid Decision Data |          |     - Hybrid Results         |  |
|  |   - Forensic Dossiers    |          |     - Incidents & Audit Log  |  |
|  +--------------------------+          +------------------------------+  |
+--------------------------------------------------------------------------+
```

---

## 4. Subsystem Modules

### 4.1 Audio Ingestion & Acoustic Verification (`app/audio/`)
- **Magic-Byte Integrity**: Verifies true container format via initial header bytes (RIFF/WAVE, ID3/Sync MP3, ftyp M4A, OggS, Matroska/WebM). Rejects mislabeled files (e.g. WebM renamed as `.wav`).
- **Path Traversal Protection**: Strips relative paths, null bytes, and non-whitelisted characters via strict sanitization.
- **Acoustic Profiling**: Extracts channels, sample rate, bit depth, and duration via `soundfile` and `wave`.

### 4.2 Gnani Prisma v3.0 STT Client (`app/gnani/prisma_client.py`)
- **Endpoint**: `POST https://api.vachana.ai/stt/v3`
- **Authentication**: Sent via `token: {GNANI_API_KEY}` header.
- **Format Delivery**: Multipart form with `audio` binary stream and JSON config payload.
- **Timestamp Integrity**: Preserves verbatim vendor segment timestamps; never fabricates dummy timestamps.
- **Resilience**: Backoff retries on rate limits; falls back gracefully to simulated mode in development if keys are absent.

### 4.3 Machine Learning Pipeline & Hybrid Intelligence Engine (`app/ml/`)
- **Production Baseline v1.0** (`backend/app/ml/artifacts/v1/`): Platt-calibrated Logistic Regression baseline trained locally on Dataset v2 (350 train). Active production default. Measured CPU latency: Mean: 11.68 ms, P50: 10.27 ms, P95: 23.06 ms.
- **TF-IDF v3 Fast-Path Classifier** (`backend/app/ml/artifacts/tfidf_v3/`): Subword and character n-gram calibrated classifier trained on Dataset v3 (2,100 train). Measured CPU latency: **4.29 ms** (~42 MB footprint).
- **Google MuRIL v1 Transformer** (`backend/app/ml/artifacts/muril_v1/`): Fine-tuned `google/muril-base-cased` transformer (237M parameters) for deep contextual and code-mixed threat comprehension across 17 Indian languages. CPU latency: ~1,543 ms.
- **Cascaded Three-Stage Pipeline** (`POST /api/v1/hybrid/analyze`):
  $$\text{Stage 0: Rule Shield} \longrightarrow \text{Stage 1: TF-IDF v3 (Fast Path)} \longrightarrow \text{Stage 2: Selective MuRIL v1 (Deep Path)}$$
  Under validation-calibrated operating threshold ($\tau = 0.85$), TF-IDF resolves ~68% of calls in <5 ms, invoking MuRIL for only ~32% of ambiguous or code-mixed calls. Reduces transformer compute overhead by **68%** while achieving 100% accuracy and 0 false negatives on the held-out test partition.

### 4.4 Rule-Priority Shield & Safety Decision Fusion (`app/detection/` & `app/ml/hybrid_engine.py`)
- **Rule-Priority Shield**: Enforces domain safety: if deterministic rules detect critical indicators (CBI/ED Digital Arrest, OTP extraction, active extortion), statistical models cannot downgrade risk. Enforces a permanent risk floor of $\ge 85.0$ and severity `Critical`.
- **Conservative Disagreement Resolution**: If TF-IDF and MuRIL diverge (e.g. TF-IDF predicts `LEGITIMATE`, MuRIL detects `SCAM`), the conservative safety policy routes to `NEEDS_REVIEW` or `SCAM`, never `LEGITIMATE`.
- **Fallback Guarantee**: In the absence of transformer model weights or upon forward-pass exceptions, transitions smoothly to Stage 1 TF-IDF and deterministic rules without throwing runtime errors.

### 4.5 SOC Incident Management & Forensic Reporting (`app/incidents/` & `app/reports/`)
- **Automated Incident Creation**: Escalates high-risk transcripts into actionable SOC cases.
- **Audit Logging**: Maintains chronological event timelines for analyst review and forensic reconstruction.
- **ReportLab PDF Generator**: Dynamically renders formal incident dossiers with detection mode breakdown (`HYBRID` vs `RULE_ONLY`), rule/ML scores, category badges, and actionable guidance.
