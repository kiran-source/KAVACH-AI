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
pytest backend/tests/ -v
```

### Run Synthetic Benchmark Pipeline
```powershell
$env:PYTHONPATH = "backend"
python -c "from app.services.evaluation import run_evaluation_pipeline; print(run_evaluation_pipeline()['metrics'])"
```

---

## 3. Test Coverage Summary (52 Passed Tests)

The full automated backend test suite consists of **52 tests** across 6 test modules, achieving a **100% pass rate**:

| Test Module | Test Count | Focus Areas | Status |
| :--- | :---: | :--- | :---: |
| `backend/tests/test_api.py` | 11 | Health, providers, audio metadata, incidents, PDF generation, security | **PASSED** |
| `backend/tests/test_backend.py` | 5 | Direct engine initialization, scam/safe triage, Prisma mock integration | **PASSED** |
| `backend/tests/test_dataset_generator.py` | 7 | Storage monitoring, API ledger tracking, turn/PII validation, Timbre/Prisma adapters | **PASSED** |
| `backend/tests/test_gnani_integration.py` | 7 | Config validation, auth error handling, demo/real mode separation | **PASSED** |
| `backend/tests/test_ml_and_hybrid.py` | 16 | 7 Rule-Priority & safety edge cases, educational context, abstention, multilinguality | **PASSED** |
| `backend/tests/test_recording_format.py` | 6 | Container magic-byte validation (WAV, MP3, M4A, WebM) & script rejection | **PASSED** |
| **Total** | **52** | **Full Backend, Hybrid ML & Security Suite (63.30s)** | **100% PASS** |

---

## 4. Frontend Build & Type Validation
The React TypeScript frontend is compiled with strict type checking and zero warnings:
```powershell
npm run build --prefix frontend
```
- **TypeScript**: `tsc` compiles clean with zero type errors.
- **Vite**: Production bundle generated in `frontend/dist/`.

