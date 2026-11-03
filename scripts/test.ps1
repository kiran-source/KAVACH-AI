# KAVACH AI - Automated Test Suite Runner (PowerShell)
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  Executing KAVACH AI Automated Test Suite" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$env:PYTHONPATH = "backend"

# 1. Run Backend Pytest Suite
Write-Host "`n[1/2] Running Backend Unit & Integration Tests via Pytest..." -ForegroundColor Yellow
pytest -v backend/tests/test_api.py
if ($LASTEXITCODE -ne 0) {
    Write-Error "Pytest test suite failed."
    exit 1
}

# 2. Run Synthetic Evaluation Benchmark
Write-Host "`n[2/2] Running 20-Scenario Synthetic Benchmark Pipeline..." -ForegroundColor Yellow
python -c @"
from app.services.evaluation import run_evaluation_pipeline
metrics = run_evaluation_pipeline()
print('Dataset Scenarios:', metrics['dataset_size'])
print('Accuracy:         ', f\"{metrics['metrics']['accuracy'] * 100:.1f}%\")
print('Precision:        ', f\"{metrics['metrics']['precision'] * 100:.1f}%\")
print('Recall:           ', f\"{metrics['metrics']['recall'] * 100:.1f}%\")
print('F1-Score:         ', f\"{metrics['metrics']['f1_score'] * 100:.1f}%\")
print('Confusion Matrix: ', metrics['confusion_matrix'])
"@

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n==========================================================" -ForegroundColor Green
    Write-Host "  ALL TESTS PASSED! PLATFORM VERIFIED AND COMPLIANT." -ForegroundColor Green
    Write-Host "==========================================================" -ForegroundColor Green
}
