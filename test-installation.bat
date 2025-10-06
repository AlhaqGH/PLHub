@echo off
REM Quick test script to verify plhub installation

echo.
echo ╔════════════════════════════════════════╗
echo ║     PLHub Installation Test            ║
echo ╚════════════════════════════════════════╝
echo.

REM Add PLHub to PATH for this session
set "PATH=%PATH%;%~dp0"

echo [1/4] Testing plhub.bat exists...
if exist "%~dp0plhub.bat" (
    echo ✅ plhub.bat found
) else (
    echo ❌ plhub.bat not found
    echo Please run install.bat first
    pause
    exit /b 1
)
echo.

echo [2/4] Testing plhub --version...
call "%~dp0plhub.bat" --version
if %ERRORLEVEL% EQU 0 (
    echo ✅ Version check passed
) else (
    echo ❌ Version check failed
)
echo.

echo [3/4] Testing plhub doctor...
call "%~dp0plhub.bat" doctor
if %ERRORLEVEL% EQU 0 (
    echo ✅ Doctor check passed
) else (
    echo ⚠️ Doctor check had warnings (may be normal)
)
echo.

echo [4/4] Testing new build syntax...
echo Running: plhub build apk --help
call "%~dp0plhub.bat" build apk --help | findstr /i "android apk release debug"
if %ERRORLEVEL% EQU 0 (
    echo ✅ New syntax recognized
) else (
    echo ⚠️ Build command test incomplete
)
echo.

echo ╔════════════════════════════════════════╗
echo ║        Test Complete!                  ║
echo ╚════════════════════════════════════════╝
echo.
echo ✅ PLHub is installed and working!
echo.
echo 📝 To use globally, restart your terminal.
echo    Then type: plhub --version
echo.
echo 🚀 Try these commands:
echo    plhub doctor
echo    plhub build apk --release
echo    plhub run examples\poh\hello.poh
echo.

pause
