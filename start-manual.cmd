@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"
set "PYTHONUTF8=1"
set "AGENTPROBE_PYTHON=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
if exist "%AGENTPROBE_PYTHON%" (
    "%AGENTPROBE_PYTHON%" -m agentprobe.manual %*
    exit /b
)
where py >nul 2>nul
if not errorlevel 1 (
    py -m agentprobe.manual %*
    exit /b
)
where python >nul 2>nul
if not errorlevel 1 (
    python -m agentprobe.manual %*
    exit /b
)
echo Python bulunamadi. Python 3.10 veya ustu gerekiyor.
exit /b 2
