# Project Specification: KAVACH AI

## 1. Executive Summary & Problem Context
**KAVACH AI** (Multilingual AI-Powered Voice Scam Detection and Security Incident Response Platform) is designed for the **Great Indian AI Internship Challenge (organized by Gnani AI)**.

India faces aggressive and highly organized voice social-engineering operations that bypass conventional phone-number spam filters by exploiting psychological manipulation:
1. **Digital Arrest Scams**: Victims coerced onto fake continuous video calls under simulated police/CBI custody.
2. **Authority Impersonation**: Fraudulent callers posing as CBI officers, Cyber Crime Police, Supreme Court magistrates, or Customs officers.
3. **Banking KYC & Credential Extortion**: Urgent ultimatums threatening account deactivation to elicit OTPs, UPI PINs, and CVVs.
4. **Remote Access Exploitation**: Demands to install AnyDesk, TeamViewer, QuickSupport, or malicious sideloaded APKs.
5. **Courier & Customs Contraband Fraud**: Claims that illegal parcels containing narcotics or fake passports have been seized in the victim's name.
6. **Linguistic Vulnerability**: Targeted exploitation of elderly and non-English speakers using **code-mixed vernacular** (Telugu-English, Hindi-English).

**Crucial Position**: KAVACH AI is an **AI-assisted decision-support system**, not an automated law enforcement agent or guaranteed fraud detector.

---

## 2. Technical Stack & Execution Constraints

| Layer | Selected Technology | Justification & Constraints |
| :--- | :--- | :--- |
| **Frontend** | React 18, TypeScript, Vite, Tailwind CSS, Recharts, Lucide React, Axios, React Router v6 | High-density dark cybersecurity SOC UI; instant responsiveness; zero bloated desktop runtimes. |
| **Backend** | Python 3.12+, FastAPI, Pydantic v2, SQLAlchemy, SQLite, python logging | Lightweight REST API; local-first; asynchronous I/O; low memory profile (< 250MB RAM). |
| **Speech-to-Text (ASR)** | **Gnani Prisma v2.5** | High accuracy across Telugu, Hindi, and English with Language Identification (LID) and timestamped segments. |
| **Text-to-Speech (TTS)** | **Gnani Timbre v2.5** | Immediate acoustic safety warnings in native Indian languages; local speech fallback. |
| **Reasoning Engine** | **Gnani Evon v3.3** | Optional second-stage reasoning arbiter for ambiguous transcripts. |
| **Audio Processing** | SoundFile, Librosa, Python Wave | Header inspection, duration/sample-rate validation, safe temporary quarantine. |
| **Forensic Reporting** | ReportLab | Pure-Python PDF generation for SOC incident dossiers; zero external binary dependencies. |
| **Verification & Testing** | Pytest, Synthetic Benchmark Pipeline | Reproducible metrics: Precision, Recall, F1, Confusion Matrix across 20 synthetic scenarios. |

### Hardware & Runtime Envelope
- **Operating System**: Windows 10/11 64-bit
- **Memory Footprint**: Strict 16 GB RAM ceiling (entire application uses < 800 MB combined)
- **Processor**: Intel Core i5 / AMD Ryzen 5 class (No GPU acceleration assumed)
- **Local Storage**: Under 1 GB total footprint (SQLite database + quarantined uploads)
- **Network Mode**: Localhost 127.0.0.1 default binding; no direct telephony interception claimed.

---

## 3. High-Level System Architecture
```
[User / Analyst]
       |
       v
[React Vite Frontend (SOC Operations Console)]
       |  HTTP/JSON & Multipart
       v
[FastAPI Backend Engine]
  ├── Audio Ingestion Module (MIME check, 25MB cap, UUID mapping, path-traversal guard)
  ├── Gnani Prisma v2.5 Integration (Multilingual ASR, LID, timestamped segments)
  ├── Threat Detection Rule Engine (8 Threat categories, Negative context guard, Regex)
  ├── Explainable Risk Scoring Engine (0–100 Weighted model, Severity mapping)
  ├── Gnani Timbre v2.5 Integration (Localized acoustic safety voice warnings)
  ├── Security Incident Management (State machine: New -> Under Review -> Confirmed/Resolved)
  ├── Forensic PDF Report Engine (ReportLab SOC incident dossiers)
  └── SQLite Relational Database (SQLAlchemy ORM, parameterized queries)
```
