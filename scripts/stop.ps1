# KAVACH AI - Service Shutdown Script (PowerShell)
param (
    [int]$BackendPort = 8000,
    [int]$FrontendPort = 5173
)

Write-Host "==========================================================" -ForegroundColor Yellow
Write-Host "  Stopping KAVACH AI Services" -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Yellow

$stoppedAny = $false
$ports = @($BackendPort, $FrontendPort)

foreach ($port in $ports) {
    $conns = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
    if ($conns) {
        $pids = $conns.OwningProcess | Select-Object -Unique
        foreach ($pidToKill in $pids) {
            Write-Host "  Terminating process $pidToKill listening on port $port..." -ForegroundColor Cyan
            Stop-Process -Id $pidToKill -Force -ErrorAction SilentlyContinue
            $stoppedAny = $true
        }
    }
}

if (-not $stoppedAny) {
    Write-Host "  No active processes found on ports $BackendPort or $FrontendPort." -ForegroundColor Gray
} else {
    Write-Host "  All KAVACH AI services stopped successfully." -ForegroundColor Green
}
