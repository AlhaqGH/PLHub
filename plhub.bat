@echo off
REM PLHub Launcher for Windows
REM Makes PLHub commands short and language-independent
REM Usage: plhub run, plhub build apk --release, etc.

setlocal

REM Get the directory where this script is located
set "PLHUB_ROOT=%~dp0"

REM Check if Python is available
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python not found in PATH
    echo Please install Python 3.8 or higher
    echo Download from: https://www.python.org/downloads/
    exit /b 1
)

REM Run PLHub with all arguments
python "%PLHUB_ROOT%plhub.py" %*

endlocal
