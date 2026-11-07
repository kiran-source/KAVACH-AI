# KAVACH AI — REST API Documentation (v1)

Base URL: `http://127.0.0.1:8000/api/v1`  
Interactive Swagger UI: `http://127.0.0.1:8000/docs`

---

## 1. System Health & Diagnostics

### `GET /health`
Returns system status, service name, version, and demo mode flag.
- **Response**:
  ```json
  {
    "status": "healthy",
    "service": "KAVACH AI Backend",
    "version": "1.0.0",
    "demo_mode": true,
    "environment": "development"
  }
  ```

### `GET /health/providers`
Returns connection status and supported languages for Gnani AI modules (Prisma v3, Timbre v2.5, Evon v3.3).

---

## 2. Audio Ingestion & Storage

### `POST /audio/upload`
Uploads an audio file for validation and analysis.
- **Form Data**:
  - `file`: Binary audio file (`.wav`, `.mp3`, `.m4a`, `.flac`, `.ogg`, `.webm`)
- **Response (200 OK)**:
  ```json
  {
    "success": true,
    "audio_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
    "filename": "call_recording.wav",
    "duration": 14.5,
    "size": 460800,
    "format": "wav"
  }
  ```

### `POST /audio/recording`
Uploads live microphone recording blob from browser with optional duration estimate.

### `GET /audio/{audio_id}`
Streams the binary audio file for in-browser playback or returns metadata.

### `DELETE /audio/{audio_id}`
Permanently purges audio file from disk to comply with user privacy and data retention policies.

---

## 3. Speech Transcription (Gnani Prisma V3.0)

### `POST /transcription/{audio_id}`
Transcribes stored audio using the official Gnani Prisma V3.0 STT engine on Vachana (`https://api.vachana.ai/stt/v3`).
- **Form Data**:
  - `language`: Target language hint (`auto` / `indic-auto`, `te`, `hi`, `en`)
- **Authentication Header**: `X-API-Key-ID: <GNANI_API_KEY>`
- **Response (200 OK)**:
  ```json
  {
    "transcript_id": "01a1a288-780e-7037-bbcf-8e280334aaba",
    "language": "en-IN",
    "detected_languages": ["en", "hi"],
    "segments": [
      {
        "start": 0.0,
        "end": 6.4,
        "text": "Namaste, your State Bank of India account KYC verification is pending, please update your details.",
        "language": "en-IN"
      }
    ],
    "full_text": "Namaste, your State Bank of India account KYC verification is pending, please update your details.",
    "provider": "gnani_prisma_v3.0",
    "is_mock": false
  }
  ```

### `GET /transcription/{transcript_id}`
Retrieves existing transcript record with segment timestamps.

---

## 4. Threat Detection & Risk Scoring

### `POST /analysis/{transcript_id}`
Executes deterministic rule matching, negative context detection, and multi-factor risk scoring.
- **Response (200 OK)**:
  ```json
  {
    "analysis_id": "AN-9102A8C4",
    "transcript_id": "TR-4F9A2B1C",
    "risk_score": 88.0,
    "severity": "Critical",
    "threats": [
      {
        "rule_id": "AUTH_001",
        "category": "Authority Impersonation",
        "matched_text": "cbi headquarters",
        "contribution": 20.0,
        "explanation": "Caller claims to represent law enforcement or intelligence agencies."
      }
    ],
    "categories": ["Authority Impersonation", "Digital Arrest Patterns"],
    "recommendations": [
      "Government agencies never interrogate or threaten arrest via video calls.",
      "Call 1930 Cyber Fraud Helpline immediately."
    ],
    "context_suppressed": false,
    "incident_id": "3b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d"
  }
  ```

---

## 5. Voice Safety Warnings (Gnani Timbre v2.5)

### `POST /warnings/generate`
Synthesizes targeted acoustic warning in Telugu, Hindi, or English.
- **Form Data**:
  - `language`: `te` | `hi` | `en`
  - `categories`: Comma-separated threat categories
  - `custom_text`: Optional override text
- **Response**:
  ```json
  {
    "success": true,
    "language": "te",
    "warning_text": "ఈ కాల్‌లో తీవ్రమైన మోసపూరిత సంకేతాలు ఉన్నాయి...",
    "audio_url": "/static/warnings/warning_49a2bc1d.wav",
    "provider": "gnani_timbre_v2.5",
    "is_fallback": false
  }
  ```

---

## 6. Incident Management & SOC Reporting

### `GET /incidents`
Lists incidents with optional `?status=New` and `?severity=High` filters.

### `GET /incidents/{incident_id}`
Returns complete incident dossier including audio metadata, transcript, forensic evidence, and chronological audit timeline.

### `PATCH /incidents/{incident_id}`
Updates incident status (`New`, `Under Review`, `Confirmed Suspicious`, `False Positive`, `Resolved`), analyst assignment, or case notes.

### `POST /incidents/{incident_id}/notes`
Appends timestamped analyst observation to the investigation journal.

### `POST /reports/{incident_id}`
Generates official SOC Incident Report PDF and returns download link.

### `GET /reports/{report_id}/download`
Downloads generated PDF file.

---

## 7. Metrics & Synthetic Benchmark

### `GET /dashboard/metrics`
Computes real-time SOC metrics directly from SQLite database records.

### `POST /evaluation/run`
Executes evaluation pipeline on the 20-scenario synthetic dataset and returns Confusion Matrix, Precision, Recall, and F1 score.

---

## 8. Gnani AI Official Vachana Cloud Integration

### Overview
KAVACH AI integrates genuinely with official **Gnani.ai Vachana VoiceOS** speech APIs.

| Service | Official Endpoint | Auth Header | Model / Voice |
| :--- | :--- | :--- | :--- |
| **Speech-to-Text (STT)** | `POST https://api.vachana.ai/stt/v3` | `X-API-Key-ID: <KEY>` | Model: `prisma-v3.0`, Language: `indic-auto` |
| **Text-to-Speech (TTS)** | `POST https://api.vachana.ai/api/v1/tts/inference` | `X-API-Key-ID: <KEY>` | Model: `timbre-v2.5`, Voice: `Nalini` |

### Environment Configuration (`backend/.env`)
```env
PORT=8000
DATABASE_URL=sqlite:///./kavach.db

# Insert your actual secret key from the Gnani / Vachana developer portal:
GNANI_API_KEY=YOUR_ACTUAL_API_KEY

GNANI_PRISMA_ENDPOINT=https://api.vachana.ai/stt/v3
GNANI_TIMBRE_ENDPOINT=https://api.vachana.ai/api/v1/tts/inference

# Mode toggle:
# false = Live authenticated calls to api.vachana.ai
# true  = Offline deterministic simulator (zero credits consumed)
DEMO_MODE=false
RETENTION_DAYS=7
MAX_UPLOAD_SIZE_MB=25
ENVIRONMENT=development
```

### Real API Mode vs Demo Mode
1. **Real API Mode (`DEMO_MODE=false`)**:
   - Sends real authenticated multipart/form-data audio to `api.vachana.ai/stt/v3`.
   - Sends real JSON speech synthesis requests to `api.vachana.ai/api/v1/tts/inference`.
   - Returns genuine cloud provider responses (`provider: "gnani_prisma_v3.0"` and `"gnani_timbre_v2.5"`).
   - If authentication fails (HTTP 401/403) or rate limits occur (HTTP 429), the API surfaces explicit HTTP exceptions rather than masking errors with simulated responses.
2. **Demo Mode (`DEMO_MODE=true` or unconfigured placeholder key)**:
   - Uses local deterministic transcripts mapped to test scenarios.
   - Transparently labels responses as `provider: "gnani_prisma_v3.0 (Simulated / Demo Mode)"` and `is_mock: true`.
   - Synthesizes local playable audio via Windows SAPI5 or audio tone signals.

### Troubleshooting & Diagnostics
- **HTTP 401 / 403 (Unauthorized)**: Verify that `GNANI_API_KEY` in `backend/.env` is active and has permissions for STT and TTS in the Gnani Vachana portal.
- **HTTP 429 (Rate Limit / Quota Exceeded)**: Check your credit balance on Vachana (e.g. 5,000 credit allocation).
- **HTTP 502 / 503 (Bad Gateway / Unreachable)**: Ensure the host machine has outbound internet connectivity to `api.vachana.ai:443`.
- **Credit Protection**: Automated CI unit tests (`pytest`) use mocks to preserve your credit balance. Controlled live tests can be executed using `python scratch/audit_gnani_live.py` (which makes strictly 1 TTS call and 1 STT call).

