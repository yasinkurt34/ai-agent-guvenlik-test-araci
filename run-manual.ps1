param([string]$Model = 'gemma-4-e4b-it', [string]$Mode = 'protected', [string]$Prompt, [switch]$VerifyAudit)
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$env:PYTHONUTF8 = '1'
[Console]::InputEncoding = [System.Text.UTF8Encoding]::new()
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
$bundledPython = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
if (Test-Path -LiteralPath $bundledPython) { $pythonExecutable = $bundledPython }
elseif (Get-Command py -ErrorAction SilentlyContinue) { $pythonExecutable = 'py' }
elseif (Get-Command python -ErrorAction SilentlyContinue) { $pythonExecutable = 'python' }
else { throw 'Python 3.10+ bulunamadi.' }
$runArguments = @('-m', 'agentprobe.manual', '--model', $Model, '--mode', $Mode)
if ($PSBoundParameters.ContainsKey('Prompt')) { $runArguments += @('--prompt', $Prompt) }
if ($VerifyAudit) { $runArguments += '--verify-audit' }
& $pythonExecutable @runArguments
exit $LASTEXITCODE
