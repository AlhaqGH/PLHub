# PLHub PATH Setup Helper
# Run this if "plhub" command is not recognized after installation

Write-Host "🔧 PLHub PATH Setup Helper" -ForegroundColor Cyan
Write-Host "============================`n" -ForegroundColor Cyan

# Get PLHub directory
$plhubDir = $PSScriptRoot
if (-not $plhubDir) {
    $plhubDir = Split-Path -Parent $MyInvocation.MyCommand.Path
}
if (-not $plhubDir) {
    $plhubDir = "C:\Users\habib\POHLANG\PLHub"
}

Write-Host "📁 PLHub Location: $plhubDir`n" -ForegroundColor Yellow

# Check if plhub.bat exists
if (Test-Path "$plhubDir\plhub.bat") {
    Write-Host "✅ plhub.bat found`n" -ForegroundColor Green
} else {
    Write-Host "❌ plhub.bat not found!" -ForegroundColor Red
    Write-Host "   Please run install.bat first`n" -ForegroundColor Red
    exit 1
}

# Get current user PATH
$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")

# Check if PLHub is already in PATH
if ($currentPath -like "*$plhubDir*") {
    Write-Host "✅ PLHub is already in PATH`n" -ForegroundColor Green
} else {
    Write-Host "➕ Adding PLHub to PATH..." -ForegroundColor Yellow
    
    # Add to PATH
    $newPath = "$currentPath;$plhubDir"
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    
    Write-Host "✅ PLHub added to PATH`n" -ForegroundColor Green
}

# Update current session PATH
$env:PATH += ";$plhubDir"

Write-Host "🔄 Testing plhub command..." -ForegroundColor Yellow
try {
    $version = & "$plhubDir\plhub.bat" --version 2>&1
    Write-Host "✅ Success: $version`n" -ForegroundColor Green
} catch {
    Write-Host "❌ Error testing plhub command" -ForegroundColor Red
    Write-Host "   $_`n" -ForegroundColor Red
}

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "✅ PATH Setup Complete!`n" -ForegroundColor Green

Write-Host "📝 For this session, PATH has been updated." -ForegroundColor Yellow
Write-Host "   You can now use: plhub --version`n" -ForegroundColor Yellow

Write-Host "🔄 For NEW PowerShell windows:" -ForegroundColor Yellow
Write-Host "   Close and reopen PowerShell/Terminal" -ForegroundColor White
Write-Host "   The PATH will be permanent`n" -ForegroundColor White

Write-Host "🚀 Try these commands:" -ForegroundColor Cyan
Write-Host "   plhub --version" -ForegroundColor White
Write-Host "   plhub doctor" -ForegroundColor White
Write-Host "   plhub build apk --release" -ForegroundColor White
Write-Host "" 

Read-Host "Press Enter to exit"
