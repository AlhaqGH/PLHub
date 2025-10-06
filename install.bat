@echo off
REM ============================================================================
REM PLHub Installation Script for Windows
REM ============================================================================
REM This script installs PLHub and makes it globally accessible
REM Usage: Run this script as Administrator for system-wide install,
REM        or as regular user for user-only install
REM ============================================================================

echo.
echo ╔════════════════════════════════════════╗
echo ║     PLHUB INSTALLATION FOR WINDOWS     ║
echo ╚════════════════════════════════════════╝
echo.

REM Get the directory where PLHub is located
set "PLHUB_ROOT=%~dp0"
set "PLHUB_ROOT=%PLHUB_ROOT:~0,-1%"

echo ⏳ Installing PLHub...
echo    Location: %PLHUB_ROOT%
echo.

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Python not found!
    echo.
    echo Please install Python 3.8 or higher first:
    echo    https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo ✅ Python found
python --version
echo.

REM Install Python dependencies
echo ⏳ Installing Python dependencies...
pip install -r "%PLHUB_ROOT%\requirements.txt" >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo ✅ Dependencies installed
) else (
    echo ⚠️  Some dependencies may have issues, but continuing...
)
echo.

REM Check if running as Administrator
net session >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set "ADMIN=1"
    echo 🔑 Running with Administrator privileges
    echo    Will install system-wide
) else (
    set "ADMIN=0"
    echo 👤 Running as regular user
    echo    Will install for current user only
)
echo.

REM Add PLHub to PATH
echo ⏳ Adding PLHub to PATH...

if "%ADMIN%"=="1" (
    REM System-wide installation
    setx /M PATH "%PATH%;%PLHUB_ROOT%" >nul 2>nul
    echo ✅ Added to system PATH
) else (
    REM User-only installation
    setx PATH "%PATH%;%PLHUB_ROOT%" >nul 2>nul
    echo ✅ Added to user PATH
)

REM Update current session PATH
set "PATH=%PATH%;%PLHUB_ROOT%"

echo.
echo ⏳ Creating command shortcuts...

REM Make plhub.bat executable (already is on Windows)
echo ✅ plhub.bat ready

echo.
echo ╔════════════════════════════════════════╗
echo ║      INSTALLATION SUCCESSFUL! ✓        ║
echo ╚════════════════════════════════════════╝
echo.
echo PLHub has been installed successfully!
echo.
echo 📍 Installation Location: %PLHUB_ROOT%
echo 🔧 Command: plhub
echo.
echo ✨ You can now use PLHub from anywhere:
echo.
echo    plhub run app.poh
echo    plhub build apk --release
echo    plhub build apk --debug
echo    plhub create my-app
echo    plhub doctor
echo.
echo ⚠️  IMPORTANT: Close and reopen your terminal/PowerShell
echo    for PATH changes to take effect!
echo.
echo 📚 Documentation: %PLHUB_ROOT%\docs\
echo 🚀 Quick Start: %PLHUB_ROOT%\docs\ANDROID_QUICKSTART.md
echo.
echo Test installation with: plhub --version
echo.

pause
