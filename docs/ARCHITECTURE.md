# KAVACH AI — System Architecture & Technical Specification

## 1. Executive Summary
**KAVACH AI** (కవచ్ / कवच) is a specialized, privacy-preserving, AI-assisted security decision-support platform designed to protect Indian citizens and institutions against phone-based voice social-engineering attacks. It ingests voice conversations, utilizes **Gnani Prisma v2.5** for multilingual speech-to-text transcription, runs a deterministic and explainable multi-factor threat detection engine, computes a transparent 0–100 risk score, generates actionable safety voice advisories using **Gnani Timbre v2.5**, and manages security incidents with SOC-grade auditing and ReportLab PDF reporting.

---

## 2. Target Deployment & Hardware Profile
KAVACH AI is optimized to execute entirely on a standard consumer/enterprise workstation without requiring dedicated GPUs:
- **Host OS**: Windows 10/11 (64-bit)
- **CPU**: Intel Core i5 (8th Gen+) / AMD Ryzen 5 class
- **Memory**: 16 GB RAM (Application uses < 600 MB total)
- **Local Storage**: SQLite zero-configuration database, under 1 GB footprint
- **Network**: Localhost 127.0.0.1 default binding; secure outbound HTTPS to Gnani AI endpoints for cloud inference.

---

## 3. High-Level Architectural Diagram

```
       +-----------------------------------------------------------+
       |                     REACT FRONTEND                        |
       |  Vite + TypeScript + Tailwind CSS + Lucide + Recharts    |
       +-----------------------------+-----------------------------+
                                     |
                                     | REST API (HTTP/JSON + Multipart)
                                     v
+--------------------------------------------------------------------------+
|                          FASTAPI BACKEND SERVICE                         |
|                                                                          |
|  +--------------------------+          +------------------------------+  |
|  |  AUDIO INGESTION ENGINE  |          |   GNANI PRISMA v2.5 STT      |  |
|  |  - Format Validation     | -------> |   - Multilingual ASR         |  |
|  |  - Magic-byte integrity  |          |   - Language Identification  |  |
|  |  - Wave/SoundFile Meta   |          |   - Timestamped Segments     |  |
|  |  - Path Traversal Guard  |          |   - Bounded Exponential Retry|  |
|  +--------------------------+          +--------------+---------------+  |
|                                                       |                  |
|                                                       v                  |
|  +--------------------------+          +------------------------------+  |
|  |  GNANI TIMBRE v2.5 TTS   |          |    THREAT DETECTION ENGINE   |  |
|  |  - Multilingual Advisory | <------- |    - 8 Threat Category Rules |  |
|  |  - Telugu, Hindi, English|          |    - Negative Context Guard  |  |
|  |  - SAPI / WAV Fallback   |          |    - Multi-tactic Synergy    |  |
|  +--------------------------+          +--------------+---------------+  |
|                                                       |                  |
|                                                       v                  |
|  +--------------------------+          +------------------------------+  |
|  |   SOC PDF GENERATOR      |          |     INCIDENT MANAGEMENT      |  |
|  |   - ReportLab Engine     | <------- |     - State Transitions      |  |
|  |   - Forensic Dossiers    |          |     - Audit Timeline Log     |  |
|  +--------------------------+          |     - Analyst Case Journal   |  |
|                                        +--------------+---------------+  |
|                                                       |                  |
|                                                       v                  |
|                               +-------------------------------+          |
|                               |     SQLITE DB (SQLAlchemy)    |          |
|                               +-------------------------------+          |
+--------------------------------------------------------------------------+
```

---

## 4. Subsystem Modules

### 4.1 Audio Ingestion & Processing Module (`app/audio/`)
- **File Integrity & Format Validation**: Ensures extension belongs to whitelist (`.wav`, `.mp3`, `.m4a`, `.flac`, `.ogg`, `.webm`) and matches payload size constraints (default 25 MB max).
- **Security Sanitization**: Strips path traversal sequences (`../`, null bytes, illegal characters) via `sanitize_filename()`.
- **Acoustic Metadata Extraction**: Utilizes `soundfile` and standard library `wave` to extract exact sample rate, channel count, duration, and encoding frames.

### 4.2 Gnani Prisma v2.5 Speech-to-Text Module (`app/gnani/prisma_client.py`)
- **Language Identification**: Detects whether incoming speech is in Telugu (`te`), Hindi (`hi`), or English (`en`), including code-mixed patterns.
- **Normalization Engine**: Converts vendor responses into a standardized application schema:
  - `transcript_id`: Unique identifier
  - `language`: Primary language tag
  - `detected_languages`: Multilingual token distribution
  - `segments`: Start time, end time, segment text, segment language
  - `full_text`: Verbatim transcript preserving unredacted evidence
- **Resilience**: Features bounded retries with exponential backoff on HTTP 429 / 5xx errors and transparent simulated demo mode when credentials are not configured.

### 4.3 Multilingual Threat Detection & Risk Scoring (`app/detection/`)
- Evaluates 8 distinct cyber social-engineering threat categories:
  1. **Authority Impersonation** (Police, CBI, Customs, Supreme Court, TRAI, ED)
  2. **Urgency & Coercive Threats** (Immediate arrest, account blocking, electricity termination)
  3. **Credential Theft** (OTP, UPI PIN, CVV, ATM passwords, net banking credentials)
  4. **Remote Access Manipulation** (AnyDesk, TeamViewer, QuickSupport, APK sideloading)
  5. **Financial Redirection Fraud** (Safe accounts, verification deposits, tax refund fees)
  6. **Psychological Manipulation & Secrecy** (Commands to isolate, lock doors, conceal from family)
  7. **Courier & Customs Parcel Fraud** (FedEx narcotics confiscation, fake passport seizures)
  8. **Digital Arrest Patterns** (Continuous video surveillance, Zoom/Skype interrogation)
- **Negative Context Analysis**: Automatically detects security awareness campaigns, bank advisories, and educational reminders to eliminate false positives on legitimate safety notices.
- **Explainable Scoring**: Calculates weighted contributions capped at 100 with dynamic synergy modifiers for coordinated multi-vector attacks.

### 4.4 Gnani Timbre v2.5 Voice Advisory Module (`app/gnani/timbre_client.py`)
- Synthesizes immediate, localized safety instructions in Telugu, Hindi, and English.
- Dispatches emergency defensive advisories directing victims to end the call, contact their bank branch, and dial **1930** (Indian Cybercrime Helpline).
- Provides offline SAPI5 speech synthesis fallback when cloud APIs are unconfigured.

### 4.5 Security Incident Response & Forensics (`app/incidents/` & `app/reports/`)
- Automatically opens security incidents when risk scores cross the Medium threshold (>= 40.0).
- Tracks status transitions through a strict lifecycle: `New` -> `Under Review` -> `Confirmed Suspicious` / `False Positive` -> `Resolved`.
- Generates professional forensic incident dossiers in PDF format utilizing ReportLab.
