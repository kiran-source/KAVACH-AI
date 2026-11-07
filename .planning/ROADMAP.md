# Phased Implementation Roadmap: KAVACH AI

## 1. Roadmap Architecture Overview
The roadmap is structured into **14 sequential phases**, organized into 4 strategic milestones.

```
MILESTONE 1: Core Foundation & Vertical MVP Slice (Phases 1 - 7)
  └── Working end-to-end tracer: Audio Ingest ➔ Prisma STT ➔ Threat Engine ➔ Risk Scoring ➔ DB ➔ Minimal UI

MILESTONE 2: Acoustic Defense & Incident Response (Phases 8 - 11)
  └── Timbre TTS Voice Warnings ➔ Incident Lifecycle ➔ SOC Dashboard ➔ PDF Forensics

MILESTONE 3: Synthetic Evaluation & Hardening (Phases 12 - 13)
  └── 20-Scenario Dataset ➔ Benchmarking Pipeline (F1/Precision/Recall) ➔ Security & Code Quality

MILESTONE 4: Competition Packaging & Operational Delivery (Phase 14)
  └── PowerShell Automation ➔ Video Script ➔ Documentation ➔ Readiness Audit
```

---

## 2. Detailed Phase Breakdown

### PHASE 1 — Project Foundation, Environment & Scaffolding
- **Objective**: Establish development environment, directory hierarchy, git repository, configuration, and security baselines.
- **Dependencies**: None.
- **Key Tasks**:
  - Initialize Git repository with `.gitignore` guarding against `.env`, `.db`, `uploads/`, `node_modules/`.
  - Configure `.env.example` with fallback defaults for Gnani AI endpoints and demo settings.
  - Establish Python logging framework in `backend/app/core/logging.py`.
- **Acceptance Criteria**:
  - `git status` clean and tracking repository root.
  - Python 3.12+ virtual environment verified.
- **Technical Risks**:
  - Environment drift on Windows PowerShell. *Mitigation: Standardize on relative paths and explicit environment exports.*

---

### PHASE 2 — Backend Architecture, Database & Session Management
- **Objective**: Implement SQLAlchemy relational models, SQLite session management, and health endpoints.
- **Dependencies**: Phase 1.
- **Key Tasks**:
  - Build `backend/app/database/models.py` covering all 10 core entities.
  - Implement `backend/app/database/session.py` with automatic schema generation (`init_db()`).
  - Implement `/api/v1/health` and `/api/v1/health/providers` endpoints.
- **Acceptance Criteria**:
  - SQLite database creates tables without errors.
  - Health check returns `200 OK` with JSON telemetry.
- **Technical Risks**:
  - SQLite concurrency on simultaneous uploads. *Mitigation: `connect_args={"check_same_thread": False}` and scoped sessions.*

---

### PHASE 3 — Frontend Architecture & SOC Design System
- **Objective**: Scaffold React 18, TypeScript, Vite, Tailwind CSS, Recharts, and routing hierarchy.
- **Dependencies**: Phase 1.
- **Key Tasks**:
  - Configure `vite.config.ts` with API proxying to `http://127.0.0.1:8000`.
  - Implement dark-theme SOC operations layout (`AppLayout.tsx`) with brand logo, provider health pills, and emergency helpline routing (1930).
  - Configure TypeScript types (`types/index.ts`) matching backend Pydantic schemas.
- **Acceptance Criteria**:
  - `npm run build --prefix frontend` compiles with 0 type errors.
  - Responsive SOC dashboard layout loads on `http://localhost:5173`.
- **Technical Risks**:
  - Tailwind styling conflicts. *Mitigation: Explicit dark theme color palette and utility classes.*

---

### PHASE 4 — Audio Ingestion & Acoustic Validation Engine
- **Objective**: Implement secure file upload, MIME validation, format checking, and metadata extraction.
- **Dependencies**: Phase 2.
- **Key Tasks**:
  - Implement `validator.py` with extension whitelist (`.wav`, `.mp3`, `.m4a`, `.flac`, `.ogg`, `.webm`) and 25 MB payload ceiling.
  - Implement path traversal protection via `sanitize_filename()`.
  - Implement `processor.py` utilizing `soundfile` and `wave` to extract sample rate, channels, and duration.
  - Build endpoints: `POST /api/v1/audio/upload`, `POST /api/v1/audio/recording`, `GET /api/v1/audio/{id}`, `DELETE /api/v1/audio/{id}`.
- **Acceptance Criteria**:
  - Upload of valid WAV/MP3 succeeds and returns metadata.
  - Malicious files (`.exe`, traversal `../../`) rejected with HTTP 400.
  - Oversized payloads rejected with HTTP 413.
- **Technical Risks**:
  - Missing native audio codecs on Windows. *Mitigation: Pure-Python fallback using `soundfile` + standard library `wave`.*

---

### PHASE 5 — Gnani Prisma v3 Speech-to-Text Integration
- **Objective**: Integrate genuine Gnani Prisma v3 ASR for multilingual transcription and language identification.
- **Dependencies**: Phase 4.
- **Key Tasks**:
  - Implement `backend/app/gnani/prisma_client.py` with bearer authentication, timeouts, and bounded backoff.
  - Build response normalization converting vendor output into standard internal `TranscriptResponse`.
  - Provide a deterministic, unforgeable simulated demo transcription mode for offline testing.
  - Build endpoint: `POST /api/v1/transcription/{audio_id}`.
- **Acceptance Criteria**:
  - Audio files transcribed into Telugu, Hindi, and English with segment timestamps.
  - Offline demo mode clearly returns `is_mock: true` without faking API success.
- **Technical Risks**:
  - Cloud API timeout during network instability. *Mitigation: 30-second timeout with bounded retry and transparent fallback.*

---

### PHASE 6 — Multilingual Threat Detection & Heuristics Engine
- **Objective**: Implement explainable regex and keyword detection covering 8 social-engineering threat categories.
- **Dependencies**: Phase 5.
- **Key Tasks**:
  - Implement `rules.py` with patterns for Telugu, Hindi, English, and code-mixed vernacular across 8 categories:
    Authority Impersonation, Urgency, Credential Theft, Remote Access, Financial Fraud, Isolation, Courier Fraud, Digital Arrest.
  - Implement negative context analysis (`NEGATIVE_CONTEXT_PATTERNS`) to suppress false positives on security advisories.
  - Capture matched snippets, character offsets, and tactic explanations.
- **Acceptance Criteria**:
  - Detects digital arrest, CBI impersonation, OTP requests, and AnyDesk sideloading.
  - Bank educational advisories mentioning "OTP" are suppressed as benign/low risk.
- **Technical Risks**:
  - Substring false matches (e.g. "spin" matching "pin"). *Mitigation: Regex word boundaries `\b`.*

---

### PHASE 7 — Explainable Risk Scoring & Severity Mapping [MVP Completion Milestone]
- **Objective**: Implement 0–100 risk scoring algorithm, multi-tactic synergy modifiers, and severity classification.
- **Dependencies**: Phase 6.
- **Key Tasks**:
  - Implement weighted scoring model in `engine.py` capped strictly at 100.
  - Add synergy bonuses (+8 to +15 pts) for multi-tactic attacks.
  - Map scores to severity: Low (0–19), Guarded (20–39), Medium (40–59), High (60–79), Critical (80–100).
  - Build endpoint: `POST /api/v1/analysis/{transcript_id}`.
- **Acceptance Criteria**:
  - Full vertical MVP slice operational: Audio Ingest ➔ Prisma STT ➔ Detection ➔ Risk Score.
  - Point breakdown and triggered rules returned in API response.
- **Technical Risks**:
  - Uncalibrated arbitrary scoring. *Mitigation: Strict rule weight tables and versioned algorithm.*

---

### PHASE 8 — Gnani Timbre v2.5 Voice Advisory Integration
- **Objective**: Implement localized acoustic safety voice warnings in native Indian languages.
- **Dependencies**: Phase 7.
- **Key Tasks**:
  - Implement `backend/app/gnani/timbre_client.py` for cloud TTS synthesis.
  - Build multilingual warning copy in Telugu, Hindi, and English directing targets to hang up and call 1930.
  - Implement offline local TTS fallback via `pyttsx3` / valid audio wave generation.
  - Build endpoint: `POST /api/v1/warnings/generate`.
- **Acceptance Criteria**:
  - High-risk detection triggers valid playable WAV audio in browser.
  - Telugu, Hindi, and English audio warnings generated accurately.
- **Technical Risks**:
  - Missing Windows audio device. *Mitigation: Synthesize file-backed WAV served over HTTP.*

---

### PHASE 9 — Security Incident Management & Lifecycle
- **Objective**: Build SOC incident queue, status state machine, audit timelines, and analyst journals.
- **Dependencies**: Phase 7.
- **Key Tasks**:
  - Automatic ticket generation on `risk_score >= 40.0`.
  - Implement status transitions: `New` ➔ `Under Review` ➔ `Confirmed Suspicious` / `False Positive` ➔ `Resolved`.
  - Immutable timeline logging for every investigation event.
  - Build endpoints: `GET /api/v1/incidents`, `GET /api/v1/incidents/{id}`, `PATCH /api/v1/incidents/{id}`, `POST /api/v1/incidents/{id}/notes`.
- **Acceptance Criteria**:
  - Incident tickets created and queryable with status and severity filters.
  - Analyst notes persisted with UTC timestamps.
- **Technical Risks**:
  - Timeline desynchronization. *Mitigation: Centralized ORM relationship cascades.*

---

### PHASE 10 — SOC Operations Dashboard & Dynamic Telemetry
- **Objective**: Implement real-time dashboard reflecting actual database records and interactive charts.
- **Dependencies**: Phase 9, Phase 3.
- **Key Tasks**:
  - Build `GET /api/v1/dashboard/metrics` calculating live counts, detection rates, false-positive ratios, and distributions.
  - Render Recharts visualizations: Risk Distribution Bar Chart, Language Breakdown, Top Tactics.
  - Connect Recent Incidents table with direct links to Incident Detail dossiers.
- **Acceptance Criteria**:
  - Dashboard updates dynamically when calls are analyzed or statuses change.
  - Zero hardcoded mock metrics. Empty state displayed gracefully when database is clear.
- **Technical Risks**:
  - Recharts layout jumping during initial render. *Mitigation: Fixed height ResponsiveContainer wrappers.*

---

### PHASE 11 — Forensic SOC Incident Report Generation (PDF Export)
- **Objective**: Generate formal cybersecurity incident PDF dossiers using ReportLab.
- **Dependencies**: Phase 9.
- **Key Tasks**:
  - Build `backend/app/reports/pdf_generator.py` with custom styles, headers, and metadata tables.
  - Embed full transcript, evidence excerpts, point contributions, timeline, and compliance disclaimers.
  - Build endpoints: `POST /api/v1/reports/{incident_id}` and `GET /api/v1/reports/{report_id}/download`.
- **Acceptance Criteria**:
  - Downloadable PDF renders cleanly in any PDF viewer.
  - Long transcripts wrap cleanly without text clipping.
- **Technical Risks**:
  - Text overflow on multi-page transcripts. *Mitigation: Wrap text in Platypus `Paragraph` flowables inside table cells.*

---

### PHASE 12 — Synthetic Evaluation Dataset & Benchmarking Pipeline
- **Objective**: Build 20 pre-recorded synthetic scenarios and automated evaluation pipeline.
- **Dependencies**: Phase 7.
- **Key Tasks**:
  - Script 20 scenarios (10 scam, 5 legit, 5 ambiguous) across Telugu, Hindi, English, and code-mixed.
  - Generate synthetic 16kHz audio files under multiple acoustic conditions (clean, low noise, telephone bandpass).
  - Implement `backend/app/services/evaluation.py` computing Confusion Matrix, Precision, Recall, and F1.
  - Build endpoint: `POST /api/v1/evaluation/run`.
- **Acceptance Criteria**:
  - Evaluation pipeline executes without ground-truth label leakage.
  - F1-score >= 0.90, Precision >= 0.90, Recall >= 0.90 verified on dataset.
- **Technical Risks**:
  - Overfitting to synthetic phrases. *Mitigation: Test varied grammatical structures and code-mixed vernacular.*

---

### PHASE 13 — Security Hardening, Automated Tests & DevSecOps
- **Objective**: Implement automated Pytest suite, sanitization checks, and DevSecOps verification.
- **Dependencies**: All preceding phases.
- **Key Tasks**:
  - Implement `backend/tests/test_api.py` covering all core modules, services, and endpoints.
  - Validate CORS configuration, input sanitization, and path traversal guards.
  - Execute CodeRabbit security review checklist.
- **Acceptance Criteria**:
  - 100% of Pytest tests pass in < 5 seconds.
  - Zero high/critical vulnerabilities or hardcoded secrets.
- **Technical Risks**:
  - Windows socket permission locks during test execution. *Mitigation: Direct function & ORM integration testing.*

---

### PHASE 14 — Competition Demo Packaging & Operational Delivery
- **Objective**: Package turn-key startup scripts, demo video script, user documentation, and final review.
- **Dependencies**: All preceding phases.
- **Key Tasks**:
  - Create PowerShell scripts: `setup.ps1`, `start.ps1`, `stop.ps1`, `test.ps1`.
  - Author comprehensive documentation: `README.md`, `ARCHITECTURE.md`, `API_DOCUMENTATION.md`, `SECURITY.md`, `DATASET.md`, `LIMITATIONS.md`, `USER_GUIDE.md`, `DEMO_VIDEO_SCRIPT.md`, `COMPETITION_CHECKLIST.md`.
  - Final readiness audit against the master prompt acceptance criteria.
- **Acceptance Criteria**:
  - Another developer can clone the repo and run `.\scripts\setup.ps1` followed by `.\scripts\start.ps1` to launch the full platform.
  - 75–90 second demo script aligned with challenge criteria.

