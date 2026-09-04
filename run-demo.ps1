$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot

$bundledPython = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
if (Test-Path -LiteralPath $bundledPython) {
    $pythonExecutable = $bundledPython
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    $pythonExecutable = 'py'
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonExecutable = 'python'
} else {
    throw 'Python 3.10+ bulunamadi. Python kurduktan sonra tekrar calistirin.'
}

& $pythonExecutable -m agentprobe --out reports/demo
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'Rapor: reports/demo/report.html'
