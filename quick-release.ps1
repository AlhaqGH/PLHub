#!/usr/bin/env pwsh
# Quick Release Script for PLHub v0.5.1
# Run this to create a GitHub release quickly

Write-Host "🚀 PLHub v0.5.1 Quick Release Script" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

$VERSION = "v0.5.1"
$SDK_ZIP = "plhub-sdk-0.5.1.zip"
$SDK_CHECKSUM = "plhub-sdk-0.5.1.zip.sha256"

# Check if files exist
Write-Host "📦 Checking release artifacts..." -ForegroundColor Yellow
if (-not (Test-Path $SDK_ZIP)) {
    Write-Host "❌ Error: $SDK_ZIP not found" -ForegroundColor Red
    exit 1
}
if (-not (Test-Path $SDK_CHECKSUM)) {
    Write-Host "❌ Error: $SDK_CHECKSUM not found" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Release artifacts found" -ForegroundColor Green
Write-Host ""

# Check if gh CLI is installed
Write-Host "🔍 Checking GitHub CLI..." -ForegroundColor Yellow
$ghExists = Get-Command gh -ErrorAction SilentlyContinue
if (-not $ghExists) {
    Write-Host "❌ GitHub CLI not found. Please install it:" -ForegroundColor Red
    Write-Host "   winget install GitHub.cli" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Or create release manually at:" -ForegroundColor Yellow
    Write-Host "   https://github.com/AlhaqGH/PLHub/releases/new" -ForegroundColor Cyan
    exit 1
}
Write-Host "✅ GitHub CLI found" -ForegroundColor Green
Write-Host ""

# Check if logged in
Write-Host "🔐 Checking GitHub authentication..." -ForegroundColor Yellow
$authStatus = gh auth status 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Not logged in to GitHub" -ForegroundColor Yellow
    Write-Host "Running: gh auth login" -ForegroundColor Yellow
    gh auth login
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Authentication failed" -ForegroundColor Red
        exit 1
    }
}
Write-Host "✅ Authenticated" -ForegroundColor Green
Write-Host ""

# Show release info
Write-Host "📋 Release Information:" -ForegroundColor Cyan
Write-Host "   Version: $VERSION" -ForegroundColor White
Write-Host "   SDK Zip: $SDK_ZIP" -ForegroundColor White
Write-Host "   Checksum: $SDK_CHECKSUM" -ForegroundColor White
Write-Host ""

# Confirm
Write-Host "🎯 Ready to create GitHub release?" -ForegroundColor Yellow
Write-Host "   This will:" -ForegroundColor White
Write-Host "   1. Create release for tag $VERSION" -ForegroundColor White
Write-Host "   2. Upload SDK zip and checksum" -ForegroundColor White
Write-Host "   3. Generate release notes from changelog" -ForegroundColor White
Write-Host ""
$confirm = Read-Host "Continue? (y/N)"
if ($confirm -ne "y" -and $confirm -ne "Y") {
    Write-Host "❌ Release cancelled" -ForegroundColor Red
    exit 0
}
Write-Host ""

# Create release notes
Write-Host "📝 Preparing release notes..." -ForegroundColor Yellow
$releaseNotes = @"
# PL-Hub v0.5.1 - Language-Independent Commands

## 🎉 Major Features

### Language-Independent Commands
- **Short Platform Names** - ``plhub build apk`` instead of ``python plhub.py build --target android``
- **No Python Prefix** - Use ``plhub run app.poh`` just like ``git``, ``npm``, ``docker``
- **Global Accessibility** - Works from any directory after installation
- **Automated Installation** - ``install.bat`` (Windows) and ``install.sh`` (Linux/macOS)
- **Professional CLI** - Commands like ``plhub build apk --release``, ``plhub build ipa``, ``plhub build exe``

## 🐛 Bug Fixes & Improvements
- Fixed Python 3.9 compatibility issues (dataclass slots, union types)
- Cleaned up old Python runtime architecture (6,461+ lines removed)
- Improved SDK compatibility (removed non-existent tool imports)
- Added .gitkeep files for empty directories
- Full CI/CD pipeline coverage (Python 3.9-3.12)

## 📦 Installation

### Quick Install
````bash
# Clone and install
git clone https://github.com/AlhaqGH/PLHub
cd PLHub

# Windows
.\install.bat

# Linux/macOS
chmod +x install.sh && ./install.sh
````

### Using SDK Package
Download ``plhub-sdk-0.5.1.zip`` from assets below and extract.

## ✅ Compatibility
- **Python:** 3.9, 3.10, 3.11, 3.12
- **Platforms:** Windows, macOS, Linux
- **Runtime:** PohLang Rust runtime required

## 📚 Documentation
- [Installation Guide](https://github.com/AlhaqGH/PLHub/blob/main/INSTALL_AND_USAGE.md)
- [Language-Independent Commands](https://github.com/AlhaqGH/PLHub/blob/main/LANGUAGE_INDEPENDENT_COMMANDS.md)
- [Complete Changelog](https://github.com/AlhaqGH/PLHub/blob/main/CHANGELOG.md)

## 🙏 Thank You
Thanks to all contributors and users who helped make PLHub better!

---

**Full Changelog:** https://github.com/AlhaqGH/PLHub/compare/v0.5.0...v0.5.1
"@

$releaseNotes | Out-File -FilePath "release_notes_temp.md" -Encoding UTF8
Write-Host "✅ Release notes created" -ForegroundColor Green
Write-Host ""

# Create release
Write-Host "🚀 Creating GitHub release..." -ForegroundColor Yellow
gh release create $VERSION `
    --title "PL-Hub v0.5.1 - Language-Independent Commands" `
    --notes-file release_notes_temp.md `
    $SDK_ZIP `
    $SDK_CHECKSUM

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Release created successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🎊 Your release is live at:" -ForegroundColor Cyan
    Write-Host "   https://github.com/AlhaqGH/PLHub/releases/tag/$VERSION" -ForegroundColor White
    Write-Host ""
    Write-Host "📊 Next steps:" -ForegroundColor Yellow
    Write-Host "   1. Verify the release page" -ForegroundColor White
    Write-Host "   2. Test downloading the SDK zip" -ForegroundColor White
    Write-Host "   3. Share the release announcement" -ForegroundColor White
    Write-Host "   4. (Optional) Publish to PyPI: python -m build && python -m twine upload dist/*" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "❌ Release creation failed" -ForegroundColor Red
    Write-Host "   Check the error above and try again" -ForegroundColor Yellow
    Write-Host "   Or create manually at: https://github.com/AlhaqGH/PLHub/releases/new" -ForegroundColor Yellow
}

# Cleanup
Remove-Item -Force release_notes_temp.md -ErrorAction SilentlyContinue

Write-Host ""
