# KAVACH AI — Application Security & Privacy Review Report

**Generated:** 2026-11-04  
**Scope:** Backend (FastAPI), Frontend (React/Vite), SQLite Database, Gnani API Integrations  

## 1. Security Architecture Summary

KAVACH AI is engineered as an evaluation prototype and security decision-support tool. It enforces strict local-first privacy, zero secret exposure, and comprehensive upload validation.

## 2. Security Assessment Matrix

| Dimension | Implementation & Safeguards | Status |
|---|---|---|
| **Network Binding** | Bound strictly to `127.0.0.1` (`HOST=127.0.0.1`). Refuses external network connections. | SECURE |
| **CORS Policy** | Whitelisted strictly to local origins: `http://localhost:5173`, `http://127.0.0.1:5173`, `http://localhost:8000`. | SECURE |
| **API Key Isolation** | Secrets loaded strictly from `backend/.env`. Excluded from git, client JS bundles, and packaged archives. Startup check ensures real mode requires credentials without silent fallback. | SECURE |
| **Path Traversal Protection** | Audio filenames sanitized using regex (`[A-Za-z0-9_.-]`), mapped to unique UUIDs, and validated inside designated directories. | SECURE |
| **Upload File Validation** | Maximum size enforced (`MAX_UPLOAD_SIZE_MB=25`). Magic bytes inspected (`RIFF` for WAV, `ID3` for MP3, WebM/Matroska header). Non-audio files rejected. | SECURE |
| **SQL Injection Protection** | 100% parameterized queries via SQLAlchemy ORM; zero raw concatenated SQL strings. | SECURE |
| **XSS & Content Security** | React 18 automated JSX escaping. HTML tags stripped from user case notes. | SECURE |
| **Telephony Compliance** | Strictly consent-based. Explicit browser microphone permission required. No cellular line tapping or unauthorized recording. | COMPLIANT |
| **PII Protection** | Automated regex pattern scanners verify absence of credit card and Aadhaar numbers. Real OTPs/passwords not retained in persistent logs. | PASS |

## 3. Known Limitations & Prototype Boundaries

- **Multi-Tenant Authentication:** The current system does not implement user login or role-based access control (RBAC). It is designed as a local single-operator SOC prototype.
- **Rate Limiting:** Reverse-proxy rate limiting (e.g., NGINX / Cloudflare) is recommended before exposing to a public network.
- **External KMS:** In enterprise production, API keys should be stored in cloud secret managers (e.g. AWS Secrets Manager, GCP Secret Manager) rather than local `.env` files.
