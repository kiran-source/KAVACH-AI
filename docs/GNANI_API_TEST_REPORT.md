# KAVACH AI — Gnani API Test Report

**Test Suite**: `backend/tests/test_gnani_integration.py` & `backend/tests/test_api.py`  
**Execution Environment**: Python 3.13.5 (Windows)  
**Total Tests**: 7 automated unit and integration tests  
**Pass Rate**: 100% (7/7 Passed)

---

## 1. Test Execution Breakdown

| Test Identifier | Test Name | Target Tested | Result |
| :--- | :--- | :--- | :---: |
| **GNANI-01** | `test_gnani_configuration_loading` | Verifies environment loading of endpoints, headers, and API keys. | **PASSED** |
| **GNANI-02** | `test_missing_or_placeholder_key_in_demo_mode` | Ensures unconfigured/placeholder keys safely default to demo mode without crashing. | **PASSED** |
| **GNANI-03** | `test_prisma_request_construction_with_mock` | Verifies multipart request payload, header injection (`X-API-Key-ID`), and language parameter formatting. | **PASSED** |
| **GNANI-04** | `test_timbre_request_construction_with_mock` | Validates JSON request payload, audio decoding, and file writing to warnings directory. | **PASSED** |
| **GNANI-05** | `test_real_mode_raises_on_auth_failure` | Confirms that in `DEMO_MODE=false`, an authentication failure (HTTP 401/403) raises a structured `HTTPException(502)`. | **PASSED** |
| **GNANI-06** | `test_demo_mode_separation` | Confirms strict cryptographic and behavioral isolation between demo simulation and real API calls. | **PASSED** |
| **GNANI-07** | `test_end_to_end_pipeline_with_real_transcript` | Validates full pipeline: Audio input $\to$ STT $\to$ Transcript $\to$ Scam Detection $\to$ Voice Warning. | **PASSED** |

---

## 2. Test Execution Command & Evidence

Command: `pytest backend/tests/test_gnani_integration.py -v`

Output:
```text
backend/tests/test_gnani_integration.py::test_gnani_configuration_loading PASSED
backend/tests/test_gnani_integration.py::test_missing_or_placeholder_key_in_demo_mode PASSED
backend/tests/test_gnani_integration.py::test_prisma_request_construction_with_mock PASSED
backend/tests/test_gnani_integration.py::test_timbre_request_construction_with_mock PASSED
backend/tests/test_gnani_integration.py::test_real_mode_raises_on_auth_failure PASSED
backend/tests/test_gnani_integration.py::test_demo_mode_separation PASSED
backend/tests/test_gnani_integration.py::test_end_to_end_pipeline_with_real_transcript PASSED

======================== 7 passed in 1.48s ========================
```

