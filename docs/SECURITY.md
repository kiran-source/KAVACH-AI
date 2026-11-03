# KAVACH AI — Security, Privacy & DevSecOps Architecture

## 1. Threat Model & Security Posture
KAVACH AI operates in a zero-trust, privacy-first cybersecurity operations environment. Voice recordings frequently contain sensitive personal identifiers, account references, or coerced utterances. The platform is architected to guarantee confidentiality, evidence integrity, and strict data containment.

---

## 2. Secure File Ingestion & Path Traversal Mitigations
- **Strict Whitelist Validation**: Only approved audio extensions (`.wav`, `.mp3`, `.m4a`, `.flac`, `.ogg`, `.webm`) are accepted.
- **Filename Sanitization**: Uploaded filenames are stripped of non-alphanumeric characters, backslashes, null bytes, and traversal syntax (`../`) via `sanitize_filename()`.
- **UUID Renaming**: Audio files on disk are stored strictly with UUID4 names (`<uuid>.wav`) in an isolated `uploads/` directory, completely decoupling user input from filesystem identifiers.
- **Payload Size Enforcement**: Uploads exceeding 25 MB are blocked at the HTTP layer with status `413 Request Entity Too Large` to prevent memory exhaustion and DoS attacks.

---

## 3. SQL Injection & Database Protection
- All database operations are conducted via **SQLAlchemy ORM** using parameterized bindings.
- No dynamic SQL strings or concatenated queries are used anywhere in the codebase.
- User feedback and analyst notes are safely escaped and stored in SQLite.

---

## 4. Privacy & Data Retention Policy
- **Configurable Retention Window**: Audio files and temporary analysis artifacts are marked with an expiration date (default 7 days).
- **Explicit User Consent**: Microphone recordings require the operator to actively check a consent disclosure acknowledging that voice data is captured for threat analysis.
- **On-Demand Purging**: The `DELETE /api/v1/audio/{audio_id}` endpoint allows instant, permanent erasure of raw audio files.
- **Zero Sensitive Credential Logging**: Passwords, full credit card numbers, OTPs, and biometric credentials are never written to server logs.

---

## 5. Network & Deployment Boundaries
- **Localhost Default Binding**: Services bind strictly to `127.0.0.1` and `localhost` by default, preventing unintended exposure to the local network or public internet.
- **CORS Restrictions**: Frontend API communication is proxied through Vite, with backend CORS configured for local origin validation.
- **Credential Segregation**: Gnani API keys are read from environment variables (`.env`) and are never exposed to the frontend bundle or client-side storage.

---

## 6. Code Quality & CodeRabbit Review Verification
- **Exception Boundaries**: All API routes and background operations feature bounded try-catch blocks returning standardized RFC 7807 JSON error schemas.
- **Static Analysis Compliance**: Fully typed Python with Pydantic v2 schemas and strict TypeScript compiler settings (`tsc` with zero errors).
- **Audit Logging**: All status transitions, case notes, and PDF generation events create immutable, timestamped entries in `IncidentTimelineDB`.
