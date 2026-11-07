# KAVACH AI — Application Security & Security Review Report

## 1. Executive Summary & Security Posture
KAVACH AI operates in a zero-trust, privacy-first cybersecurity operations environment. Voice recordings and transcripts frequently contain sensitive personal identifiers, account references, or coerced utterances. The platform is engineered to guarantee strict data containment, evidence integrity, credential isolation, and memory-safe processing.

This document details the security controls implemented across the architecture, verified through rigorous unit testing (52 passing automated tests) and static inspection.

---

## 2. API Key Management & Secret Isolation
- **Canonical Environment Path**: Backend configurations strictly load `GNANI_API_KEY` from `backend/.env` using path-independent resolution in `app/core/config.py`.
- **Zero Frontend Exposure**: No API keys, tokens, or external vendor secrets are embedded in React frontend bundles, local storage, session storage, or client cookies.
- **Log Masking**: Sensitive keys and authorization headers are masked in loggers and terminal outputs (`sk-****...`).
- **Archive Exclusion**: Distribution scripts (`package_submission.py`) strictly enforce `.env` exclusion to prevent accidental credential leakage in review archives.
- **Explicit Mode Enforcement**: If real API mode (`DEMO_MODE=false`) is configured but credentials are missing or invalid, the backend halts with an explicit configuration error rather than silently degrading.

---

## 3. Audio Ingestion & File Security
- **Magic-Byte Integrity Verification**: Initial header bytes are inspected to prevent MIME-spoofing attacks (e.g. executable `.exe` or shell script disguised as `.wav`).
- **Strict Format Whitelist**: Only authenticated container formats (`RIFF/WAVE`, `ID3/Sync MP3`, `ftyp M4A`, `OggS`, `Matroska/WebM`) are permitted.
- **Path Traversal Defense**: All uploaded filenames are stripped of directory traversal sequences (`../`, `..\`), null bytes, and non-whitelisted characters via `sanitize_filename()`.
- **UUID Renaming**: Stored files are written with cryptographically secure UUID4 filenames inside an isolated `uploads/` directory, completely isolating user-supplied filenames from the filesystem.
- **Payload Size Limits**: Strict 25 MB payload caps prevent heap exhaustion and denial-of-service (DoS) attacks.

---

## 4. Privacy, PII Redaction & User Consent
- **Explicit Informed Consent**: Live microphone recording requires active user agreement to a clear consent disclosure before audio streams are captured.
- **Synthetic Data Scrubbing**: Synthetic datasets (`kavach_synthetic_v1` and `v2`) contain zero real citizen records, bank accounts, or telephone numbers, using standardized redaction masks (`XXXXXXXX4321`, `98765XXXXX`).
- **Credential Suppression**: Passwords, full debit/credit card numbers, and OTP tokens captured in transcripts are never echoed in server debug logs.
- **Configurable Data Retention**: Data retention policies (default 7 days) and on-demand purge APIs (`DELETE /api/v1/audio/{audio_id}`) ensure compliance with privacy regulations.

---

## 5. Network & Deployment Boundaries
- **Localhost Binding**: Backend and frontend development servers default strictly to `127.0.0.1` and `localhost`, preventing inadvertent LAN exposure.
- **Strict CORS Origin Restrictions**: Backend API endpoints explicitly restrict origins to `http://localhost:5173`, `http://127.0.0.1:5173`, and the host port.
- **Secure Outbound HTTPS**: All communications with Gnani AI endpoints utilize TLS 1.3 encrypted HTTPS channels.

---

## 6. Machine Learning Safety: The Rule-Priority Shield
- **Adversarial Mitigation**: Statistical machine learning classifiers are susceptible to out-of-distribution bypasses or prompt perturbations.
- **Non-Downgradable Protection**: High-threat indicators detected by deterministic rules (OTP theft, AnyDesk remote control, Digital Arrest, active coercion, or raw rule score $\ge 50$) can never be suppressed by a statistical model predicting `LEGITIMATE` or `AMBIGUOUS`.
- **Divergence Auditing**: Conflicting predictions between deterministic rules and machine learning models are explicitly logged with `conflict_detected=True` for SOC human triage.

---

## 7. Audit Logging & Non-Repudiation
- **Immutable Timeline**: All incident state transitions, analyst notes, and forensic PDF generation requests are immutably logged with UTC timestamps in `IncidentTimelineDB`.
- **Forensic PDF Dossiers**: Exported PDF reports provide verifiable audit trails including detection engine version, exact rule contributions, and ML confidence metrics.

