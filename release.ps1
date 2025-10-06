#!/usr/bin/env pwsh
# PLHub Release Script for Windows (PowerShell)
# Automates the release process for PLHub

param(
    [Parameter(Mandatory=$true)]
    [string]$Version,
    
    [Parameter(Mandatory=$false)]
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║     PLHub Release Automation           ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Validate version format
if ($Version -notmatch '^\d+\.\d+\.\d+$') {
    Write-Host "❌ Error: Invalid version format '$Version'" -ForegroundColor Red
    Write-Host "   Expected format: X.Y.Z (e.g., 0.5.1)" -ForegroundColor Red
    exit 1
}

Write-Host "📦 Preparing release v$Version" -ForegroundColor Yellow
Write-Host ""

# Check if we're in PLHub directory
if (-not (Test-Path "plhub.py")) {
    Write-Host "❌ Error: Must run from PLHub root directory" -ForegroundColor Red
    exit 1
}

Write-Host "✅ In PLHub directory" -ForegroundColor Green

# Check for uncommitted changes
$gitStatus = git status --porcelain
if ($gitStatus -and -not $DryRun) {
    Write-Host "⚠️  Warning: Uncommitted changes detected:" -ForegroundColor Yellow
    Write-Host $gitStatus
    $continue = Read-Host "Continue anyway? (y/N)"
    if ($continue -ne 'y') {
        Write-Host "❌ Release cancelled" -ForegroundColor Red
        exit 1
    }
}

# Verify version in setup.py
Write-Host ""
Write-Host "🔍 Verifying version in setup.py..." -ForegroundColor Yellow
$setupContent = Get-Content "setup.py" -Raw
if ($setupContent -match 'version="([^"]+)"') {
    $setupVersion = $matches[1]
    if ($setupVersion -eq $Version) {
        Write-Host "✅ setup.py version: $setupVersion" -ForegroundColor Green
    } else {
        Write-Host "❌ setup.py version mismatch: $setupVersion (expected: $Version)" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "⚠️  Could not verify setup.py version" -ForegroundColor Yellow
}

# Verify version in plhub.py
Write-Host "🔍 Verifying version in plhub.py..." -ForegroundColor Yellow
$plhubContent = Get-Content "plhub.py" -Raw
if ($plhubContent -match "version='PL-Hub v([0-9.]+)") {
    $plhubVersion = $matches[1]
    if ($plhubVersion -eq $Version) {
        Write-Host "✅ plhub.py version: $plhubVersion" -ForegroundColor Green
    } else {
        Write-Host "❌ plhub.py version mismatch: $plhubVersion (expected: $Version)" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "⚠️  Could not verify plhub.py version" -ForegroundColor Yellow
}

if ($DryRun) {
    Write-Host ""
    Write-Host "🧪 DRY RUN MODE - No changes will be made" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Would execute:" -ForegroundColor Yellow
    Write-Host "  1. git add ." -ForegroundColor White
    Write-Host "  2. git commit -m 'Release v$Version'" -ForegroundColor White
    Write-Host "  3. git tag -a v$Version -m 'PLHub v$Version'" -ForegroundColor White
    Write-Host "  4. git push origin main" -ForegroundColor White
    Write-Host "  5. git push origin v$Version" -ForegroundColor White
    Write-Host ""
    Write-Host "✅ Dry run complete" -ForegroundColor Green
    exit 0
}

# Commit changes
Write-Host ""
Write-Host "📝 Committing changes..." -ForegroundColor Yellow
git add .
git commit -m "Release v$Version: Language-Independent Commands"

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Commit failed" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Changes committed" -ForegroundColor Green

# Create tag
Write-Host ""
Write-Host "🏷️  Creating tag v$Version..." -ForegroundColor Yellow
git tag -a "v$Version" -m "PLHub v$Version - Language-Independent Commands"

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Tag creation failed" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Tag created" -ForegroundColor Green

# Push to GitHub
Write-Host ""
Write-Host "🚀 Pushing to GitHub..." -ForegroundColor Yellow
git push origin main

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Push failed" -ForegroundColor Red
    exit 1
}

git push origin "v$Version"

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Tag push failed" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Pushed to GitHub" -ForegroundColor Green

# Success
Write-Host ""
Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║      RELEASE v$Version COMPLETE! ✓          ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

Write-Host "📦 Release v$Version is now live!" -ForegroundColor Green
Write-Host ""
Write-Host "🔗 Next steps:" -ForegroundColor Cyan
Write-Host "   1. Create GitHub release at:" -ForegroundColor White
Write-Host "      https://github.com/AlhaqGH/PLHub/releases/new?tag=v$Version" -ForegroundColor White
Write-Host "   2. Copy content from RELEASE_NOTES.md" -ForegroundColor White
Write-Host "   3. Announce on social media" -ForegroundColor White
Write-Host ""

# Open browser to create release
$openBrowser = Read-Host "Open GitHub releases page? (Y/n)"
if ($openBrowser -ne 'n') {
    Start-Process "https://github.com/AlhaqGH/PLHub/releases/new?tag=v$Version"
}

Write-Host "🎉 Done!" -ForegroundColor Green
