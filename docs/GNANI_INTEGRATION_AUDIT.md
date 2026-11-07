# KAVACH AI — Gnani AI Integration Audit

**Date**: 2026-11-07  
**Auditor**: Senior AI Systems Architect  
**Scope**: In-depth inspection of Gnani Prisma STT v3.0, Gnani Timbre TTS v2.5, and Evon v3.3 evaluation.

---

## 1. Gnani Prisma STT v3.0

- **Integrated Version**: Gnani Prisma V3.0 (`indic-auto`, `hi-IN`, `te-IN`, `en-IN`, `hi-en`, `te-en`).
- **Endpoint**: `https://api.vachana.ai/stt/v3`
- **Authentication**: `X-API-Key-ID: <GNANI_API_KEY>` (injected server-side; zero exposure to browser).
- **Supported Audio Formats**: WAV (PCM), MP3, WebM (Opus), M4A. Magic-byte verification protects against malicious uploads.
- **Request Mechanism**: Multipart form-data with language hint, diarization flags, and chunk buffering.
- **Error Handling**: Graceful degradation to labeled simulated transcription when credentials are unconfigured or in `DEMO_MODE=true`. Live API mode raises structured exceptions on invalid credentials or timeouts.
- **Verification Evidence**:
  - `backend/tests/test_gnani_integration.py` (Tests for configuration, request construction, real vs demo separation, and auth failure handling).
  - Version Reference: The application correctly uses and references Prisma V3.0 (Vachana platform standard).

---

## 2. Gnani Timbre TTS v2.5 (Beta)

- **Integrated Version**: Gnani Timbre V2.5.
- **Endpoint**: `https://api.vachana.ai/api/v1/tts/inference`
- **Authentication**: `X-API-Key-ID: <GNANI_API_KEY>`
- **Request Format**: JSON payload with `text`, `language`, and voice profile configuration.
- **Response Format**: Binary audio / base64 payload. Saved to `uploads/warnings/` with static asset routing for frontend playback.
- **Operational Mode**: Request-Response audio synthesis (non-streaming). Transparently documented as standard non-streaming batch synthesis.
- **Fallback**: Local synthetic audio synthesizer generates audible advisory tones and wave files if credentials are absent.

---

## 3. Gnani Evon v3.3 (Evaluation Only)

- **Model Type**: 30B parameter reasoning model.
- **Evaluation Status**: **UNINTEGRATED (OPTIONAL)**.
- **Technical Rationale**: Direct API probing returned `403 SCOPE_NOT_ALLOWED` for the current evaluation key. In strict compliance with guidelines, no unauthorized access was attempted, and no fake integration was simulated.
- **Competition Compliance**: The challenge requires using at least one Gnani AI model. KAVACH AI fully satisfies this through Prisma STT and Timbre TTS. Evon is purely optional.

