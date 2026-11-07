# KAVACH AI - Service Startup Script (PowerShell)
param (
    [int]$BackendPort = 8000,
    [int]$FrontendPort = 5173
)

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  Launching KAVACH AI Security Platform" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$backendDir = (Resolve-Path (Join-Path $PSScriptRoot "..\backend")).Path
$backendEnv = Join-Path $backendDir ".env"

# 1. Validate Canonical Environment Configuration
Write-Host "Validating canonical configuration ($backendEnv)..." -ForegroundColor Yellow
if (-not (Test-Path $backendEnv)) {
    Write-Host "  [WARN] backend\.env not found! Creating from backend\.env.example..." -ForegroundColor Yellow
    Copy-Item (Join-Path $backendDir ".env.example") $backendEnv
}

# Inspect environment settings safely without exposing secrets
$demoMode = "false"
$keyConfigured = $false
Get-Content $backendEnv | ForEach-Object {
    $line = $_.Trim()
    if ($line -match "^DEMO_MODE\s*=\s*(true|false)") {
        $demoMode = $matches[1].ToLower()
    }
    if ($line -match "^GNANI_API_KEY\s*=\s*(.+)$") {
        $k = $matches[1].Trim()
        if ($k -and $k -ne "YOUR_ACTUAL_API_KEY" -and $k -ne "mock_key" -and $k -ne "mock_gnani_api_key_for_testing") {
            $keyConfigured = $true
        }
    }
}

Write-Host "  Runtime Mode: $(if ($demoMode -eq 'true') { 'DEMO / LOCAL SIMULATOR' } else { 'REAL API INFERENCE' })" -ForegroundColor Cyan
Write-Host "  Gnani Credentials: $(if ($keyConfigured) { 'CONFIGURED (Active)' } else { 'MISSING OR PLACEHOLDER' })" -ForegroundColor Cyan

if ($demoMode -eq 'false' -and -not $keyConfigured) {
    Write-Host "`n[FATAL CONFIGURATION ERROR]" -ForegroundColor Red
    Write-Host "DEMO_MODE is set to 'false' (Real API Mode), but no valid GNANI_API_KEY is configured in backend\.env." -ForegroundColor Red
    Write-Host "KAVACH AI will not silently start in mock mode when real mode is requested." -ForegroundColor Red
    Write-Host "Action Required: Either provide your real GNANI_API_KEY in backend\.env or set DEMO_MODE=true." -ForegroundColor Yellow
    exit 1
}

# 2. Kill any existing instances on ports 8000 & 5173
Write-Host "`nChecking for existing processes on ports $BackendPort and $FrontendPort..." -ForegroundColor Yellow
$activePorts = @($BackendPort, $FrontendPort)
foreach ($port in $activePorts) {
    $conns = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
    if ($conns) {
        $pids = $conns.OwningProcess | Select-Object -Unique
        foreach ($p in $pids) {
            Write-Host "  Stopping existing process $p on port $port..." -ForegroundColor DarkYellow
            Stop-Process -Id $p -Force -ErrorAction SilentlyContinue
        }
    }
}

# 3. Start Backend FastAPI Server
Write-Host "`nStarting KAVACH AI Backend (FastAPI + SQLite + Gnani Providers)..." -ForegroundColor Yellow
$backendProcess = Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit", "-ExecutionPolicy", "Bypass", "-Command", "`$host.UI.RawUI.WindowTitle = 'KAVACH AI - Backend (Port $BackendPort)'; python -m uvicorn app.main:app --host 127.0.0.1 --port $BackendPort" -WorkingDirectory $backendDir -PassThru

# 4. Start Frontend Vite Server
Write-Host "Starting KAVACH AI Frontend (React + Vite + Tailwind)..." -ForegroundColor Yellow
$frontendDir = (Resolve-Path (Join-Path $PSScriptRoot "..\frontend")).Path
$frontendProcess = Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit", "-ExecutionPolicy", "Bypass", "-Command", "`$host.UI.RawUI.WindowTitle = 'KAVACH AI - Frontend (Port $FrontendPort)'; npm run dev -- --port $FrontendPort" -WorkingDirectory $frontendDir -PassThru

for ($i = 0; $i -lt 10; $i++) {
    Start-Sleep -Seconds 1
    $backendOk = Get-NetTCPConnection -LocalPort $BackendPort -State Listen -ErrorAction SilentlyContinue
    $frontendOk = Get-NetTCPConnection -LocalPort $FrontendPort -State Listen -ErrorAction SilentlyContinue
    if ($backendOk -and $frontendOk) { break }
}

if ($backendOk) {
    Write-Host "  Backend running PID: $($backendProcess.Id) at http://127.0.0.1:$BackendPort" -ForegroundColor Green
    Write-Host "  Swagger API Docs: http://127.0.0.1:$BackendPort/docs" -ForegroundColor Green
} else {
    Write-Host "  [WARN] Backend does not appear to be listening on port $BackendPort yet." -ForegroundColor Yellow
}

if ($frontendOk) {
    Write-Host "  Frontend running at http://localhost:$FrontendPort (http://127.0.0.1:$FrontendPort)" -ForegroundColor Green
} else {
    Write-Host "  [WARN] Frontend does not appear to be listening on port $FrontendPort yet." -ForegroundColor Yellow
}

Write-Host "`n==========================================================" -ForegroundColor Green
Write-Host "  KAVACH AI Platform is now ONLINE!" -ForegroundColor Green
Write-Host "  -> Open Browser: http://localhost:$FrontendPort" -ForegroundColor Cyan
Write-Host "  -> API Explorer: http://127.0.0.1:$BackendPort/docs" -ForegroundColor Cyan
Write-Host "  -> Stop Services: .\scripts\stop.ps1" -ForegroundColor DarkGray
Write-Host "==========================================================" -ForegroundColor Green
