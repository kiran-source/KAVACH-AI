# KAVACH AI — Verification & Automated Testing Guide

## 1. Automated Testing Framework
KAVACH AI employs **Pytest** for backend integration and logic verification, alongside an automated synthetic dataset evaluation pipeline.

---

## 2. Test Execution Commands

### Run Entire Test Suite via PowerShell
```powershell
.\scripts\test.ps1
```

### Run Backend Pytest Suite Directly
```powershell
$env:PYTHONPATH = "backend"
pytest -v backend/tests/test_api.py
```

### Run Synthetic Benchmark Pipeline
```powershell
$env:PYTHONPATH = "backend"
python -c "from app.services.evaluation import run_evaluation_pipeline; print(run_evaluation_pipeline()['metrics'])"
```

---

## 3. Test Coverage Matrix

| Test Case | Module | Description | Status |
| :--- | :--- | :--- | :---: |
| `test_health_check` | `app.main` | Validates `/api/v1/health` status, service identity, and version | **PASSED** |
| `test_provider_health` | `app.main` | Validates Gnani Prisma & Timbre provider connection contracts | **PASSED** |
| `test_threat_detection_engine_credential_theft` | `app.detection` | Tests OTP, UPI PIN, and CVV keyword/regex rule triggering | **PASSED** |
| `test_threat_detection_engine_digital_arrest` | `app.detection` | Tests CBI and continuous video call pattern recognition | **PASSED** |
| `test_threat_detection_engine_negative_context` | `app.detection` | Verifies bank security advisories are suppressed from false positives | **PASSED** |
| `test_multilingual_safety_warnings` | `app.detection` | Validates localized warning copy in Telugu, Hindi, and English | **PASSED** |
| `test_audio_metadata_extraction` | `app.audio` | Tests sample rate, channel count, and duration extraction | **PASSED** |
| `test_end_to_end_incident_and_report_flow` | E2E | Tests upload -> transcribe -> analyze -> incident -> PDF export | **PASSED** |
| `test_evaluation_pipeline_metrics` | `app.services` | Validates 20-scenario dataset precision, recall, and F1 >= 0.90 | **PASSED** |

---

## 4. Frontend Build & Type Validation
The React TypeScript frontend is compiled with strict type checking and zero warnings:
```powershell
npm run build --prefix frontend
```
- **TypeScript**: `tsc` compiles clean with zero type errors.
- **Vite**: Production bundle generated in `frontend/dist/`.

