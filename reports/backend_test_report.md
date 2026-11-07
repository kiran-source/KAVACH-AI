# KAVACH AI — Backend Test Suite Execution Report

**Generated:** 2026-11-04  
**Status:** 100% PASSED (36/36 tests)  

## 1. Test Execution Summary

| Test Run | Configuration | Total | Passed | Failed | Skipped | Exit Code | Duration |
|---|---|---|---|---|---|---|---|
| Run 1 | Clean Environment (No API Key, Demo Mode) | 36 | 36 | 0 | 0 | 0 | 2.87s |
| Run 2 | Mock Configuration (Mocked Timbre & Prisma) | 36 | 36 | 0 | 0 | 0 | 5.70s |

## 2. Tested Components

- `test_api.py` (11 tests): Health endpoints, provider health, threat detection rules, incident lifecycle, ReportLab PDF generation, evaluation metrics.
- `test_backend.py` (5 tests): SQLite persistence, models, database session management.
- `test_dataset_generator.py` (7 tests): Storage safety checks, API ledger, dataset validation, Timbre adapter mock, Prisma adapter mock, Stage 2 pilot simulation, Stage 3 bulk generation simulation.
- `test_gnani_integration.py` (7 tests): Canonical config resolution, strict API key enforcement in real mode, Prisma request construction, Timbre request construction, auth error handling, demo mode isolation, end-to-end pipeline with real transcript.
- `test_recording_format.py` (6 tests): MediaRecorder MIME validation, WebM/WAV header checks, audio conversion validation, audio upload size limits.
