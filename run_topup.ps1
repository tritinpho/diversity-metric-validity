param(
    [string]$Label = "topup"
)
# ---------------------------------------------------------------------------
# Same-day top-up / catch-up for the VN news snapshot corpus.
# Sweeps the full trailing window on demand in sequential per-domain batches
# (polite, one Python process at a time), isolates tuoitre last (its sitemap
# is noisy), then rebuilds the data-quality report. Merges into the existing
# parquet by article_id, so re-runs are idempotent.
#
# Usage:  pwsh -NoProfile -ExecutionPolicy Bypass -File run_topup.ps1 -Label topup_now
# ---------------------------------------------------------------------------
$ErrorActionPreference = "Continue"
# Native stderr (the pipeline logs there) must not abort the script.
if (Get-Variable -Name PSNativeCommandUseErrorActionPreference -ErrorAction SilentlyContinue) {
    $PSNativeCommandUseErrorActionPreference = $false
}

Set-Location -LiteralPath $PSScriptRoot
$env:PYTHONIOENCODING = "utf-8"
$py = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if (-not (Test-Path "logs")) { New-Item -ItemType Directory "logs" | Out-Null }
$stamp = Get-Date -Format "yyyy-MM-dd_HHmmss"
$log = Join-Path $PSScriptRoot "logs\${Label}_${stamp}.log"

function Note($msg) { Add-Content -LiteralPath $log -Value $msg }

# Keep the machine awake for the duration; idle-sleep has silently killed runs.
try {
    Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
public static class Awake {
    [DllImport("kernel32.dll")]
    public static extern uint SetThreadExecutionState(uint f);
}
'@ -ErrorAction Stop
    # ES_CONTINUOUS | ES_SYSTEM_REQUIRED  -> hold system awake
    # (cast via string so the high-bit hex isn't parsed as a negative Int32)
    [void][Awake]::SetThreadExecutionState([uint32]"0x80000001")
} catch { Note "WARN could not set wake lock: $($_.Exception.Message)" }

# Proven batch grouping (matches the manual catch-up recipe).
$batches = @(
    "vnexpress,nhandan,vietnamplus",
    "dantri,tienphong,qdnd",
    "vietnamnet,baochinhphu,vneconomy",
    "saostar,24h,kenh14",
    "soha,thanhnien,cafef"
)

Note "===== $Label start $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') ====="
$b = 0
foreach ($grp in $batches) {
    $b++
    Note "----- [B$b] start $(Get-Date -Format 'HH:mm:ss'): --outlets $grp --max 400 -----"
    & $py -m src.pipeline --outlets $grp --max 400 --no-report 2>&1 | Add-Content -LiteralPath $log
    Note "----- [B$b] end   $(Get-Date -Format 'HH:mm:ss') (exit $LASTEXITCODE) -----"
}
# tuoitre isolated with a tighter cap (noisy sitemap).
Note "----- [B6] start $(Get-Date -Format 'HH:mm:ss'): --outlets tuoitre --max 250 -----"
& $py -m src.pipeline --outlets tuoitre --max 250 --no-report 2>&1 | Add-Content -LiteralPath $log
Note "----- [B6] end   $(Get-Date -Format 'HH:mm:ss') (exit $LASTEXITCODE) -----"

Note "----- [report] rebuilding $(Get-Date -Format 'HH:mm:ss') -----"
& $py -m src.pipeline --report-only 2>&1 | Add-Content -LiteralPath $log
Note "===== $Label done  $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') ====="

# Release the wake lock (ES_CONTINUOUS only clears the previous request).
try { [void][Awake]::SetThreadExecutionState([uint32]"0x80000000") } catch { }

Write-Output $log
