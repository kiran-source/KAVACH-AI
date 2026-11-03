# 🛡️ KAVACH AI — Multilingual Voice Scam Detection & Incident Response Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-cyan.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-teal.svg)](https://fastapi.tiangolo.com/)
[![React 18](https://img.shields.io/badge/React-18-61dafb.svg)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.2-blue.svg)](https://www.typescriptlang.org/)
[![Vite](https://img.shields.io/badge/Vite-5.1-purple.svg)](https://vitejs.dev/)
[![Gnani AI](https://img.shields.io/badge/Gnani%20AI-Prisma%20%26%20Timbre%20v2.5-orange.svg)](https://www.gnani.ai/)

**KAVACH AI** (కవచ్ / कवच) is a specialized, privacy-preserving, AI-assisted security decision-support platform engineered for the **Great Indian AI Internship Challenge (organised by Gnani AI)**.

It protects Indian citizens and enterprise SOCs against advanced voice social-engineering attacks—including **Digital Arrest rackets**, **CBI/Police impersonation**, **Bank KYC & OTP theft**, **Remote Access APK sideloading**, and **Electricity disconnection threats**—with native support for **Telugu**, **Hindi**, and **English** code-mixed conversations.

---

## 🌟 Key Highlights & Innovations

1. **Genuine Gnani AI Ecosystem Integration**:
   - **Gnani Prisma v2.5**: High-fidelity Speech-to-Text with automatic Language Identification (LID) and timestamped segment extraction for Telugu, Hindi, and English.
   - **Gnani Timbre v2.5**: Localized acoustic voice safety warning synthesis, intervening with immediate spoken instructions in the victim's language.
   - **Gnani Evon v3.3**: Architecture prepared for contextual reasoning on ambiguous dialogue turns.

2. **Explainable 8-Pillar Threat Detection Engine**:
   - Deterministic, auditable regex and keyword pattern matching covering:
     1. *Authority Impersonation* (Police, CBI, Customs, Supreme Court, TRAI, ED)
     2. *Urgency & Coercive Threats* (Arrest threats, account freeze, electricity cutoff)
     3. *Credential Theft* (OTP, UPI PIN, CVV, ATM passwords, net banking credentials)
     4. *Remote Access Manipulation* (AnyDesk, TeamViewer, QuickSupport, APK downloads)
     5. *Financial Redirection Fraud* (Safe government accounts, investigation fees)
     6. *Psychological Isolation* (Commands to conceal from family and lock doors)
     7. *Courier & Customs Fraud* (FedEx/DHL narcotics and contraband allegations)
     8. *Digital Arrest Patterns* (Continuous Skype/Zoom video surveillance)

3. **Negative Context False-Positive Guard**:
   - Advanced contextual heuristics distinguish actual scam coercion from **security awareness campaigns** and bank educational advisories, preventing false alerts.

4. **Transparent 0–100 Risk Scoring & Multi-Tactic Synergy**:
   - Every flagged tactic contributes distinct, explainable points with synergy bonuses for coordinated multi-vector attacks.

5. **SOC Incident Response & ReportLab PDF Export**:
   - Complete incident management with status lifecycles (`New` -> `Under Review` -> `Confirmed Suspicious` / `False Positive` -> `Resolved`), chronological audit timelines, analyst journals, and downloadable forensic PDF reports.

6. **Reproducible Synthetic Benchmark**:
   - Includes 20 balanced, pre-recorded synthetic audio scenarios across multiple acoustic environments (clean, background noise, telephone bandpass) achieving **100% Precision, Recall, and F1-score**.

---

## 💻 System Architecture

```
                          ┌─────────────────────────────────────┐
                          │     REACT FRONTEND (Vite + TS)      │
                          │   SOC Dashboard · Audio Analysis   │
                          │   Live Chunk Scan · Incidents · PDF │
                          └──────────────────┬──────────────────┘
                                             │ REST API
                                             ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                FASTAPI BACKEND (Python 3.12+)                          │
│                                                                                        │
│  ┌───────────────────────┐      ┌─────────────────────────┐      ┌──────────────────┐  │
│  │ Audio Ingestion Module│ ───► │ Gnani Prisma v2.5 STT   │ ───► │ Threat Detection │  │
│  │ Format & Traversal    │      │ Multilingual ASR & LID  │      │ 8 Threat Rules   │  │
│  │ SoundFile Metadata    │      │ Segments & Timestamps   │      │ Context Guard    │  │
│  └───────────────────────┘      └─────────────────────────┘      └────────┬─────────┘  │
│                                                                           │            │
│  ┌───────────────────────┐      ┌─────────────────────────┐               │            │
│  │ Gnani Timbre v2.5 TTS │ ◄─── │ Explainable Risk Engine │ ◄─────────────┘            │
│  │ Telugu, Hindi, English│      │ 0-100 Score & Synergy   │                            │
│  │ Local TTS Fallback    │      │ Severity Classification │                            │
│  └───────────────────────┘      └────────────┬────────────┘                            │
│                                              │                                         │
│  ┌───────────────────────┐      ┌────────────▼────────────┐      ┌──────────────────┐  │
│  │ SOC PDF Report Engine │ ◄─── │ Incident Management     │ ───► │ SQLite Database  │  │
│  │ ReportLab Dossiers    │      │ Timeline & Case Journal │      │ SQLAlchemy ORM   │  │
│  └───────────────────────┘      └─────────────────────────┘      └──────────────────┘  │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start (Windows 10/11)

### Prerequisites
- Python 3.12+ (Python 3.13 supported)
- Node.js 20+ (Node.js 24 LTS verified)
- Windows 10/11 (16 GB RAM, no dedicated GPU needed)

### 1. Automated Setup
Open PowerShell in the project directory and run:
```powershell
.\scripts\setup.ps1
```
*This verifies Python and Node environments, creates the SQLite schema, generates the 20-scenario synthetic dataset, and installs frontend dependencies.*

### 2. Launch Platform
```powershell
.\scripts\start.ps1
```
- **Web Application**: [`http://localhost:5173`](http://localhost:5173)
- **FastAPI Documentation**: [`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs)
- **API Health Check**: [`http://127.0.0.1:8000/api/v1/health`](http://127.0.0.1:8000/api/v1/health)

### 3. Graceful Shutdown
```powershell
.\scripts\stop.ps1
```

---

## 🧪 Testing & Verification

Run the full automated test suite (Pytest + Synthetic Benchmark):
```powershell
.\scripts\test.ps1
```

### Pytest Results (100% Pass)
```
backend/tests/test_api.py::test_health_check PASSED                      [ 11%]
backend/tests/test_api.py::test_provider_health PASSED                   [ 22%]
backend/tests/test_api.py::test_threat_detection_engine_credential_theft PASSED [ 33%]
backend/tests/test_api.py::test_threat_detection_engine_digital_arrest PASSED [ 44%]
backend/tests/test_api.py::test_threat_detection_engine_negative_context PASSED [ 55%]
backend/tests/test_api.py::test_multilingual_safety_warnings PASSED      [ 66%]
backend/tests/test_api.py::test_audio_metadata_extraction PASSED         [ 77%]
backend/tests/test_api.py::test_end_to_end_incident_and_report_flow PASSED [ 88%]
backend/tests/test_api.py::test_evaluation_pipeline_metrics PASSED       [100%]
======================= 9 passed in 1.57s ========================
```

### Synthetic Benchmark Performance
- **Dataset Size**: 20 Scenarios (Telugu, Hindi, English, Code-mixed)
- **Accuracy**: 100.0%
- **Precision**: 100.0% (Zero false positives on bank awareness notices)
- **Recall**: 100.0%
- **F1-Score**: 100.0%
- **Confusion Matrix**: `{'true_positives': 10, 'true_negatives': 10, 'false_positives': 0, 'false_negatives': 0}`

---

## 📂 Repository Structure

```
KAVACH-AI/
├── backend/
│   ├── app/
│   │   ├── audio/           # Audio validation, soundfile metadata & safe storage
│   │   ├── core/            # Configuration, logging & settings
│   │   ├── database/        # SQLAlchemy models & SQLite session
│   │   ├── detection/       # 8-tactic scam rules, negative context & risk scoring
│   │   ├── gnani/           # Gnani Prisma v2.5 STT & Timbre v2.5 TTS clients
│   │   ├── reports/         # ReportLab SOC PDF incident report generator
│   │   ├── schemas/         # Pydantic v2 data contracts
│   │   ├── services/        # Synthetic evaluation benchmark service
│   │   └── main.py          # FastAPI application & 30 REST endpoints
│   ├── tests/
│   │   └── test_api.py      # Automated Pytest suite
│   ├── requirements.txt     # Python backend dependencies
│   └── .env.example         # Environment template
├── frontend/
│   ├── src/
│   │   ├── layouts/         # SOC sidebar, brand header & emergency helpline banner
│   │   ├── pages/           # Dashboard, Audio Scan, Live Scan, Incidents, Reports, Evaluation, Settings
│   │   ├── services/        # Axios API client
│   │   ├── types/           # TypeScript interfaces
│   │   ├── App.tsx          # React Router v6 routes
│   │   └── main.tsx         # React root
│   ├── package.json         # Node dependencies
│   └── vite.config.ts       # Vite proxy & build configuration
├── data/
│   ├── synthetic_audio/     # 20 generated synthetic .wav scenario files
│   ├── transcripts/         # Scenario verbatim transcripts
│   ├── labels/              # Ground-truth scenario classifications (JSON)
│   └── evaluation/          # Benchmark outputs (metrics.json)
├── reports/                 # Generated SOC Incident PDF reports
├── docs/                    # Architectural, security, API & user documentation
├── scripts/                 # PowerShell lifecycle scripts (setup, start, stop, test)
└── README.md                # Project documentation
```

---

## 🔒 Security, Privacy & Compliance
- **No Direct Telephony Interception**: Complies with Indian IT laws; only processes consented audio uploads or microphone recordings.
- **Path Traversal Shielding**: Filenames sanitized via regex and mapped to random UUIDs on disk.
- **Zero Credential Exposure**: Sensitive OTPs, PINs, and passwords are never permanently retained in logs.
- **National Cybercrime Integration**: Features prominent emergency routing to **Helpline 1930** and **https://cybercrime.gov.in**.

---

## ⚖️ Legal Disclaimer
**KAVACH AI is an AI-assisted decision-support system, not a guaranteed fraud detector.** Threat scores and tactic classifications are algorithmic recommendations based on speech transcription and heuristics. In emergencies, contact the National Cybercrime Helpline at 1930 or your local police station.

---

**Developed for the Great Indian AI Internship Challenge — Gnani AI.**
