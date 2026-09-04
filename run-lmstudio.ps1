param(
    [string]$Model,
    [switch]$ListModels,
    [string]$BaseUrl = 'http://127.0.0.1:1234/v1',
    [int]$Repeats = 1
)
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$bundledPython = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
if (Test-Path -LiteralPath $bundledPython) { $pythonExecutable = $bundledPython }
elseif (Get-Command py -ErrorAction SilentlyContinue) { $pythonExecutable = 'py' }
elseif (Get-Command python -ErrorAction SilentlyContinue) { $pythonExecutable = 'python' }
else { throw 'Python 3.10+ bulunamadi.' }

$runArguments = @('-m', 'agentprobe', '--backend', 'lmstudio', '--base-url', $BaseUrl)
if ($ListModels) { $runArguments += '--list-models' }
else {
    $reportDirectory = 'reports/lmstudio/' + (Get-Date -Format 'yyyyMMdd-HHmmss-fff')
    $runArguments += @('--out', $reportDirectory, '--repeats', "$Repeats")
    if ($Model) { $runArguments += @('--model', $Model) }
}
& $pythonExecutable @runArguments
exit $LASTEXITCODE
