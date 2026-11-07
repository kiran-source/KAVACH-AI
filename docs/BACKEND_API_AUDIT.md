# KAVACH AI — Backend & API Quality Audit

**Date**: 2026-11-07  
**Auditor**: Senior Python Backend Engineer & Application Security Specialist  
**Framework**: FastAPI 0.115+ / Python 3.13 / SQLAlchemy 2.0 / SQLite  
**Scope**: Routing, Validation, Schema Contracts, Exception Handling, Database Persistence, and File Safety.

---

## 1. Route Organization & API Contracts

All endpoints are logically organized under `/api/v1/` prefix in `backend/app/main.py`:

| Endpoint Route | HTTP Method | Request Payload | Response Contract | Security / Validation |
| :--- | :---: | :--- | :--- | :--- |
| `/api/v1/health` | `GET` | None | Service status, version, environment | Public ping endpoint |
| `/api/v1/health/providers` | `GET` | None | Provider status (Prisma, Timbre, SQLite) | Genuine runtime check |
| `/api/v1/dashboard/metrics` | `GET` | None | Incident counts, risk distributions | SQL aggregation query |
| `/api/v1/audio/upload` | `POST` | `UploadFile` (multipart) | Audio ID, file size, format metadata | Magic byte verification |
| `/api/v1/audio/recording` | `POST` | `audio_blob`, `duration` | Stored recording metadata | Validates WebM/WAV header |
| `/api/v1/transcription/{id}` | `POST` | `language` hint | Transcript ID, full text, segments | Rate-limited STT trigger |
| `/api/v1/analysis/{id}` | `POST` | None | Risk score, severity, threats, advice | Persists to `analysis_results` |
| `/api/v1/analysis/text` | `POST` | `text`, `language` | Real-time threat classification | Fast streaming evaluation |
| `/api/v1/warnings/generate` | `POST` | `language`, `categories` | Audio URL, synthesis provider | Audio file generated in uploads |
| `/api/v1/incidents` | `GET` | Query filters | List of security incident records | Filterable pagination |
| `/api/v1/reports/generate` | `POST` | `incident_id` | PDF file path, cryptographic hash | Generates tamper-evident PDF |
| `/api/v1/hybrid/analyze` | `POST` | `HybridAnalysisRequest` (JSON) | Multi-stage telemetry payload | Isolated experimental endpoint |

---

## 2. Security & Defensive Engineering Review

1. **No Credentials in Frontend**:
   - `GNANI_API_KEY` is loaded strictly on the server side via `backend/app/core/config.py`.
   - No sensitive tokens, headers, or keys are returned in JSON payloads.
2. **Audio File Header Magic-Byte Validation**:
   - Audio upload checks actual binary file magic bytes (`RIFF` for WAV, `ID3`/`\xFF\xFB` for MP3, `\x1A\x45\xDF\xA3` for WebM).
   - Spoofed files (e.g. executable `.exe` or shell `.sh` renamed to `.wav`) are immediately rejected with `400 Bad Request`.
3. **Path Traversal Defenses**:
   - File uploads are assigned randomized UUIDs.
   - Storage paths are generated with strict `os.path.basename` and resolved against absolute base directories (`backend/uploads/`).
4. **Data Retention & Privacy Purge**:
   - Includes retention service (`backend/app/services/retention.py`) with configurable TTL to purge audio recordings and temporary buffers while retaining cryptographic incident digests.
5. **CORS & Environment Controls**:
   - CORS is configured with explicit origins (`http://localhost:5173`, `http://127.0.0.1:5173`).

