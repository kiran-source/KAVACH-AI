# Requirements Specification: KAVACH AI

## 1. Functional Requirements (FR)

### FR-1: Audio Ingestion & Acoustic Validation
- **FR-1.1**: The system MUST accept file uploads in `.wav`, `.mp3`, `.m4a`, `.flac`, and `.ogg` formats.
- **FR-1.2**: The system MUST enforce a configurable upload size limit (default 25 MB) and reject oversized payloads with HTTP 413.
- **FR-1.3**: The system MUST support live microphone audio recording with mandatory explicit operator consent verification.
- **FR-1.4**: Filenames MUST be sanitized against path traversal (`../`, null bytes, illegal characters) and stored on disk under non-sequential UUID4 identifiers.
- **FR-1.5**: Acoustic metadata (sample rate, channel count, duration, format) MUST be extracted and stored in the database.

### FR-2: Gnani Prisma v3 Multilingual Transcription
- **FR-2.1**: The system MUST integrate the genuine Gnani Prisma v3 Speech-to-Text API.
- **FR-2.2**: The STT module MUST support Telugu (`te`), Hindi (`hi`), English (`en`), and code-mixed speech.
- **FR-2.3**: Provider responses MUST be normalized into an internal schema preserving verbatim transcripts and timestamped segments.
- **FR-2.4**: The system MUST implement bounded retries with exponential backoff on transient network and rate-limit errors.
- **FR-2.5**: The system MUST provide an unforgeable, clearly labeled simulated demo transcription mode when live API credentials are unconfigured or when offline.

### FR-3: Multilingual Threat Detection & Heuristics
- **FR-3.1**: The engine MUST evaluate incoming speech against 8 distinct social-engineering threat categories:
  1. Authority Impersonation
  2. Urgency and Threats
  3. Credential Theft
  4. Remote Access Manipulation
  5. Financial Fraud
  6. Psychological Manipulation & Isolation
  7. Courier and Customs Fraud
  8. Digital Arrest Patterns
- **FR-3.2**: Pattern matching MUST be conducted using case-insensitive regular expressions with word boundary guards and multilingual keyword sets.
- **FR-3.3**: The engine MUST evaluate negative security context (e.g. bank advisories, RBI educational campaigns) to suppress false positives on legitimate communications.
- **FR-3.4**: Multi-vector synergy bonuses MUST be awarded when multiple independent coercive tactics appear in the same dialogue.

### FR-4: Explainable Risk Scoring Engine
- **FR-4.1**: The system MUST calculate an explainable risk score strictly within the 0 to 100 range.
- **FR-4.2**: The risk score MUST NOT be described as a statistical probability of guilt, but as an auditable rule-weighted threat score.
- **FR-4.3**: Scores MUST map directly to 5 cybersecurity severity levels:
  - 0–19: `Low`
  - 20–39: `Guarded`
  - 40–59: `Medium`
  - 60–79: `High`
  - 80–100: `Critical`
- **FR-4.4**: The response MUST return a full breakdown of every triggered rule, matched text excerpt, character offsets, and point contribution.

### FR-5: Gnani Timbre v2.5 Acoustic Voice Warnings
- **FR-5.1**: The system MUST integrate Gnani Timbre v2.5 Text-to-Speech to synthesize localized voice warnings.
- **FR-5.2**: Spoken warnings MUST be available in Telugu, Hindi, and English matching the detected language.
- **FR-5.3**: Warnings MUST provide immediate, actionable defense (disconnect call, protect OTP/PIN, call 1930).
- **FR-5.4**: The system MUST include an offline speech synthesis fallback (`pyttsx3` / valid audio wave synthesis) when the cloud API is unreachable.

### FR-6: Security Incident Lifecycle & Case Management
- **FR-6.1**: The system MUST automatically initiate a security incident ticket for any call with `risk_score >= 40.0`.
- **FR-6.2**: Incidents MUST follow a strict state transition model: `New` ➔ `Under Review` ➔ `Confirmed Suspicious` / `False Positive` ➔ `Resolved`.
- **FR-6.3**: Every incident MUST record an immutable chronological timeline log of all detection, review, status, and note-taking events.
- **FR-6.4**: SOC analysts MUST be able to append notes to an investigation journal.

### FR-7: Forensic SOC PDF Reporting
- **FR-7.1**: The system MUST generate official cybersecurity incident reports in downloadable PDF format via ReportLab.
- **FR-7.2**: The PDF MUST display KAVACH AI branding, incident identifiers, severity, risk score, audio metadata, full transcript, detected tactics table, mitigation recommendations, and legal disclaimers.

### FR-8: SOC Operations Dashboard
- **FR-8.1**: All metrics on the dashboard MUST be calculated directly from live SQLite database tables. Hardcoded fake metrics are strictly prohibited.
- **FR-8.2**: The dashboard MUST display Total Calls, High/Medium/Low-Risk Incidents, Safe Calls, Detection Rate, False-Positive Rate, Average Risk Score, Risk Distribution, Language Breakdown, and Recent Incidents.

---

## 2. Non-Functional & Operational Requirements (NFR)

### NFR-1: Performance & Resource Footprint
- **NFR-1.1**: The entire backend, frontend, and database must operate within 16 GB RAM without swapping.
- **NFR-1.2**: Audio analysis pipelines must complete within 2 seconds in demo mode and under 15 seconds with cloud ASR.

### NFR-2: Security & Privacy Protection
- **NFR-2.1**: Filenames MUST be sanitized against path traversal (`../`) and stored using UUID4 names.
- **NFR-2.2**: Zero sensitive credential logging (OTPs, PINs, passwords must never be written to server logs).
- **NFR-2.3**: Raw audio recordings MUST be subject to a configurable data retention window (default 7 days) and support instant on-demand deletion (`DELETE /api/v1/audio/{id}`).
- **NFR-2.4**: No direct telecommunications interception is claimed or executed.

### NFR-3: Reliability & Testability
- **NFR-3.1**: The codebase MUST provide automated Pytest integration tests with 100% pass rate.
- **NFR-3.2**: A synthetic benchmark dataset of 20 scenarios (Telugu, Hindi, English, code-mixed) MUST evaluate precision, recall, F1, and confusion matrix.

