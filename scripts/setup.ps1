# KAVACH AI - Automated Setup Script (PowerShell)
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  KAVACH AI - Setup & Dependency Verification Engine" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Check Python
Write-Host "`n[1/5] Checking Python Environment..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Error "Python is not installed or not in PATH. Please install Python 3.12+."
    exit 1
}
Write-Host "  Found: $pythonVersion" -ForegroundColor Green

# 2. Check Node & NPM
Write-Host "`n[2/5] Checking Node.js Environment..." -ForegroundColor Yellow
$nodeVersion = node --version 2>&1
$npmVersion = npm --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Error "Node.js / npm is not installed. Please install Node.js 20+."
    exit 1
}
Write-Host "  Found Node: $nodeVersion | npm: $npmVersion" -ForegroundColor Green

# 3. Setup Python Backend Dependencies
Write-Host "`n[3/5] Verifying Backend Dependencies..." -ForegroundColor Yellow
$env:PYTHONPATH = "backend"
python -c "import fastapi, uvicorn, sqlalchemy, reportlab, soundfile; print('  Backend dependencies verified.')"
if ($LASTEXITCODE -ne 0) {
    Write-Host "  Installing missing backend packages from requirements.txt..." -ForegroundColor DarkYellow
    pip install -r backend/requirements.txt
}

# 4. Generate Synthetic Datasets & Init DB
Write-Host "`n[4/5] Initializing Database & Generating Synthetic Scenarios..." -ForegroundColor Yellow
python scripts/generate_synthetic_dataset.py
python -c "from app.database.session import init_db; init_db(); print('  Database tables created successfully.')"

# 5. Frontend NPM Packages
Write-Host "`n[5/5] Verifying Frontend NPM Packages..." -ForegroundColor Yellow
if (-not (Test-Path "frontend/node_modules")) {
    Write-Host "  Installing frontend dependencies..." -ForegroundColor DarkYellow
    npm install --prefix frontend
} else {
    Write-Host "  Frontend node_modules present." -ForegroundColor Green
}

Write-Host "`n==========================================================" -ForegroundColor Green
Write-Host "  KAVACH AI Setup Completed Successfully!" -ForegroundColor Green
Write-Host "  Run .\scripts\start.ps1 to launch application." -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Green
