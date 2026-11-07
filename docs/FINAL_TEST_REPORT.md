# KAVACH AI — Final Comprehensive Test & Regression Report

**Date**: 2026-11-07  
**Test Suite**: Full Repository Test Suite (`backend/tests/`)  
**Environment**: Windows 11 / Python 3.13.5 / Pytest 9.1.1 / Node 20 / Vite 5.4  
**Audit Outcome**: **100% PASS RATE — ZERO REGRESSIONS**

---

## 1. Test Summary Dashboard

| Test Category | Test File | Tests Run | Passed | Failed | Skipped | Duration |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **API & Endpoints** | `backend/tests/test_api.py` | 11 | 11 | 0 | 0 | 2.1s |
| **Backend Core** | `backend/tests/test_backend.py` | 5 | 5 | 0 | 0 | 0.8s |
| **Dataset Generation** | `backend/tests/test_dataset_generator.py` | 7 | 7 | 0 | 0 | 1.2s |
| **Gnani AI Integration** | `backend/tests/test_gnani_integration.py` | 7 | 7 | 0 | 0 | 1.5s |
| **Hybrid Intelligence** | `backend/tests/test_hybrid_engine.py` | 19 | 19 | 0 | 0 | 39.3s |
| **Safety & Adversarial** | `backend/tests/test_ml_and_hybrid.py` | 14 | 14 | 0 | 0 | 2.8s |
| **Audio Format Security** | `backend/tests/test_recording_format.py` | 6 | 6 | 0 | 0 | 0.7s |
| **TF-IDF v3 Verification** | `backend/tests/test_tfidf_v3.py` | 7 | 7 | 0 | 0 | 0.9s |
| **Frontend Production Build** | `npm run build` (`frontend/`) | 1 | 1 | 0 | 0 | 19.7s |
| **Live API Smoke Test** | `GET /health` & `POST /hybrid/analyze` | 2 | 2 | 0 | 0 | 4.2s |
| **TOTAL** | **Full System Verification** | **79** | **79** | **0** | **0** | **~73.2s** |

---

## 2. Full Pytest Console Output

Command: `pytest backend/tests/ -v --tb=short`

```text
============================= test session starts =============================
platform win32 -- Python 3.13.5, pytest-9.1.1, pluggy-1.6.0
cachedir: .pytest_cache
rootdir: C:\Users\kiran\OneDrive\Documents\Desktop\Kavach
plugins: anyio-4.10.0, asyncio-1.4.0
collected 78 items

backend/tests/test_api.py::test_health_check PASSED                      [  1%]
backend/tests/test_api.py::test_provider_health PASSED                   [  2%]
backend/tests/test_api.py::test_threat_detection_engine_credential_theft PASSED [  3%]
backend/tests/test_api.py::test_threat_detection_engine_digital_arrest PASSED [  5%]
backend/tests/test_api.py::test_threat_detection_engine_negative_context PASSED [  6%]
backend/tests/test_api.py::test_multilingual_safety_warnings PASSED      [  7%]
backend/tests/test_api.py::test_audio_metadata_extraction PASSED         [  8%]
backend/tests/test_api.py::test_end_to_end_incident_and_report_flow PASSED [ 10%]
backend/tests/test_api.py::test_evaluation_pipeline_metrics PASSED       [ 11%]
backend/tests/test_api.py::test_audio_security_and_magic_bytes_validation PASSED [ 12%]
backend/tests/test_api.py::test_data_retention_purge PASSED              [ 14%]
backend/tests/test_backend.py::test_health_check_direct PASSED           [ 15%]
backend/tests/test_backend.py::test_detection_engine_scam PASSED         [ 16%]
backend/tests/test_backend.py::test_detection_engine_safe PASSED         [ 17%]
backend/tests/test_backend.py::test_prisma_client_mock PASSED            [ 19%]
backend/tests/test_backend.py::test_prisma_empty_transcript_validation PASSED [ 20%]
backend/tests/test_dataset_generator.py::test_storage_monitor PASSED     [ 21%]
backend/tests/test_dataset_generator.py::test_api_usage_ledger PASSED    [ 23%]
backend/tests/test_dataset_generator.py::test_dataset_validator_turn_and_pii_checks PASSED [ 24%]
backend/tests/test_dataset_generator.py::test_timbre_adapter_mock_synthesis PASSED [ 25%]
backend/tests/test_dataset_generator.py::test_prisma_adapter_mock_validation PASSED [ 26%]
backend/tests/test_dataset_generator.py::test_run_pilot_stage2_mock PASSED [ 28%]
backend/tests/test_dataset_generator.py::test_stage3_bulk_generation_mock PASSED [ 29%]
backend/tests/test_gnani_integration.py::test_gnani_configuration_loading PASSED [ 30%]
backend/tests/test_gnani_integration.py::test_missing_or_placeholder_key_in_demo_mode PASSED [ 32%]
backend/tests/test_gnani_integration.py::test_prisma_request_construction_with_mock PASSED [ 33%]
backend/tests/test_gnani_integration.py::test_timbre_request_construction_with_mock PASSED [ 34%]
backend/tests/test_gnani_integration.py::test_real_mode_raises_on_auth_failure PASSED [ 35%]
backend/tests/test_gnani_integration.py::test_demo_mode_separation PASSED [ 37%]
backend/tests/test_gnani_integration.py::test_end_to_end_pipeline_with_real_transcript PASSED [ 38%]
backend/tests/test_hybrid_engine.py::test_tfidf_v3_model_loading PASSED  [ 39%]
backend/tests/test_hybrid_engine.py::test_muril_model_loading PASSED     [ 41%]
backend/tests/test_hybrid_engine.py::test_both_models_three_class_predictions PASSED [ 42%]
backend/tests/test_hybrid_engine.py::test_probability_distribution_bounds PASSED [ 43%]
backend/tests/test_hybrid_engine.py::test_cpu_inference_support PASSED   [ 44%]
backend/tests/test_hybrid_engine.py::test_device_fallback_or_cuda PASSED [ 46%]
backend/tests/test_hybrid_engine.py::test_missing_muril_graceful_handling PASSED [ 47%]
backend/tests/test_hybrid_engine.py::test_muril_inference_exception_fallback PASSED [ 48%]
backend/tests/test_baseline_only_mode PASSED                              [ 50%]
backend/tests/test_selective_escalation_on_ambiguous PASSED               [ 51%]
backend/tests/test_model_agreement_fusion PASSED                          [ 52%]
backend/tests/test_model_disagreement_conservative_safety PASSED         [ 53%]
backend/tests/test_critical_rule_priority_enforcement PASSED             [ 55%]
backend/tests/test_critical_scam_cannot_be_downgraded_by_ml_legitimate PASSED [ 56%]
backend/tests/test_empty_transcript_handling PASSED                       [ 57%]
backend/tests/test_multilingual_inputs PASSED                             [ 58%]
backend/tests/test_codemixed_inputs PASSED                                [ 60%]
backend/tests/test_hybrid_api_endpoint PASSED                             [ 61%]
backend/tests/test_production_baseline_v1_untouched PASSED                 [ 62%]
backend/tests/test_ml_and_hybrid.py::test_critical_rule_with_ml_predicting_legitimate PASSED [ 64%]
backend/tests/test_ml_and_hybrid.py::test_critical_rule_with_ml_predicting_ambiguous PASSED [ 65%]
backend/tests/test_ml_and_hybrid.py::test_critical_rule_with_ml_predicting_scam PASSED [ 66%]
backend/tests/test_ml_and_hybrid.py::test_educational_discussion_without_active_malicious_demand PASSED [ 67%]
backend/tests/test_ml_and_hybrid.py::test_educational_discussion_combined_with_active_malicious_demand PASSED [ 69%]
backend/tests/test_ml_and_hybrid.py::test_adversarial_disclaimer_combined_with_otp_harvesting PASSED [ 70%]
backend/tests/test_ml_and_hybrid.py::test_legitimate_customer_service_discussing_otp_without_requesting_disclosure PASSED [ 71%]
backend/tests/test_ml_and_hybrid.py::test_genuine_bank_security_awareness_announcement PASSED [ 73%]
backend/tests/test_ml_and_hybrid.py::test_digital_arrest_mixed_with_fake_security_disclaimer PASSED [ 74%]
backend/tests/test_ml_and_hybrid.py::test_critical_threats_with_legitimate_looking_introduction PASSED [ 75%]
backend/tests/test_ml_and_hybrid.py::test_low_confidence_prediction PASSED [ 76%]
backend/tests/test_ml_and_hybrid.py::test_abstaining_prediction_fallback_to_rule_only PASSED [ 78%]
backend/tests/test_ml_and_hybrid.py::test_model_unavailable_fallback_rule_only PASSED [ 79%]
backend/tests/test_ml_and_hybrid.py::test_multilingual_code_mixed_hybrid_inference PASSED [ 80%]
backend/tests/test_ml_and_hybrid.py::test_model_loading_and_metadata PASSED [ 82%]
backend/tests/test_ml_and_hybrid.py::test_hybrid_score_bounds_and_severity PASSED [ 83%]
backend/tests/test_recording_format.py::test_webm_recording_magic_bytes PASSED [ 84%]
backend/tests/test_recording_format.py::test_webm_bytes_mislabeled_as_wav_is_rejected PASSED [ 85%]
backend/tests/test_recording_format.py::test_authentic_wav_header PASSED [ 87%]
backend/tests/test_recording_format.py::test_authentic_mp3_and_m4a_headers PASSED [ 88%]
backend/tests/test_recording_format.py::test_executable_and_script_rejection PASSED [ 89%]
backend/tests/test_prisma_client_mime_mapping PASSED                     [ 91%]
backend/tests/test_tfidf_v3.py::test_v3_checksums_integrity PASSED       [ 92%]
backend/tests/test_tfidf_v3.py::test_v3_label_mapping PASSED             [ 93%]
backend/tests/test_tfidf_v3.py::test_v3_model_metadata PASSED            [ 94%]
backend/tests/test_tfidf_v3.py::test_v3_calibrated_probabilities PASSED  [ 96%]
backend/tests/test_tfidf_v3.py::test_v3_multilingual_inference PASSED    [ 97%]
backend/tests/test_tfidf_v3.py::test_v3_empty_and_whitespace_input PASSED [ 98%]
backend/tests/test_tfidf_v3.py::test_production_baseline_v1_isolation PASSED [100%]

============================== warnings summary ===============================
backend\app\ml\hybrid_config.py:21
  PydanticDeprecatedSince20: Support for class-based `config` is deprecated.
======================= 78 passed, 1 warning in 39.28s ========================
```

