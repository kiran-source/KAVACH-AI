# KAVACH AI - Service Startup Script (PowerShell)
param (
    [int]$BackendPort = 8000,
    [int]$FrontendPort = 5173
)

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  Launching KAVACH AI Security Platform" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Kill any existing instances on ports 8000 & 5173
Write-Host "Checking for existing processes on ports $BackendPort and $FrontendPort..." -ForegroundColor Yellow
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

# 2. Start Backend FastAPI Server
Write-Host "`nStarting KAVACH AI Backend (FastAPI + SQLite + Gnani Providers)..." -ForegroundColor Yellow
$env:PYTHONPATH = "backend"
$backendProcess = Start-Process -FilePath "python" -ArgumentList "-m uvicorn app.main:app --host 127.0.0.1 --port $BackendPort" -PassThru -WindowStyle Hidden

Start-Sleep -Seconds 2
Write-Host "  Backend running PID: $($backendProcess.Id) at http://127.0.0.1:$BackendPort" -ForegroundColor Green
Write-Host "  Swagger API Docs: http://127.0.0.1:$BackendPort/docs" -ForegroundColor Green

# 3. Start Frontend Vite Server
Write-Host "`nStarting KAVACH AI Frontend (React + Vite + Tailwind)..." -ForegroundColor Yellow
Set-Location frontend
$frontendProcess = Start-Process -FilePath "npm.cmd" -ArgumentList "run dev -- --port $FrontendPort" -PassThru -WindowStyle Hidden
Set-Location ..

Start-Sleep -Seconds 3
Write-Host "  Frontend running PID: $($frontendProcess.Id) at http://localhost:$FrontendPort" -ForegroundColor Green

Write-Host "`n==========================================================" -ForegroundColor Green
Write-Host "  KAVACH AI Platform is now ONLINE!" -ForegroundColor Green
Write-Host "  -> Open Browser: http://localhost:$FrontendPort" -ForegroundColor Cyan
Write-Host "  -> API Explorer: http://127.0.0.1:$BackendPort/docs" -ForegroundColor Cyan
Write-Host "  -> Stop Services: .\scripts\stop.ps1" -ForegroundColor DarkGray
Write-Host "==========================================================" -ForegroundColor Green
