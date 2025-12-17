$ErrorActionPreference = "SilentlyContinue"

$serviceName = "AssetIntegrityAgent"
$appDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$serviceExe = Join-Path $appDir "service.exe"

function Ensure-Service {
    $svc = Get-Service -Name $serviceName -ErrorAction SilentlyContinue
    if (-not $svc) {
        if (Test-Path $serviceExe) {
            & $serviceExe install | Out-Null
        }
    }
}

function Ensure-Recovery {
    try {
        & sc.exe failure $serviceName reset= 0 actions= restart/60000/restart/60000/restart/60000 | Out-Null
    } catch {}
}

function Ensure-Started {
    $svc = Get-Service -Name $serviceName -ErrorAction SilentlyContinue
    if ($svc -and $svc.Status -ne 'Running') {
        Start-Service -Name $serviceName -ErrorAction SilentlyContinue
    }
}

Ensure-Service
Ensure-Recovery
Ensure-Started
