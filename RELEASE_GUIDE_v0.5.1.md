# Release Guide for PLHub v0.5.1

**Current Status:** ✅ Code ready, CI passing, awaiting publication

---

## 📋 Pre-Release Checklist (COMPLETED ✅)

- ✅ All tests passing (9/9 on Python 3.9-3.12)
- ✅ Version bumped to 0.5.1 in all files
- ✅ CHANGELOG.md updated
- ✅ Git tag `v0.5.1` created
- ✅ SDK synced and packaged (`plhub-sdk-0.5.1.zip`)
- ✅ SDK checksum generated (`plhub-sdk-0.5.1.zip.sha256`)
- ✅ CI workflow passing
- ✅ Documentation updated

---

## 🚀 Release Options

You have **3 main options** for releasing PLHub v0.5.1:

### Option 1: GitHub Release (Recommended)
**Best for:** Open source distribution, easy downloads, visibility

### Option 2: PyPI Release
**Best for:** `pip install plhub` support, professional Python package

### Option 3: Both GitHub + PyPI
**Best for:** Maximum distribution reach

---

## 📦 Option 1: Create GitHub Release

### Manual Method (Easiest)

1. **Go to GitHub Releases:**
   ```
   https://github.com/AlhaqGH/PLHub/releases/new
   ```

2. **Choose tag:** `v0.5.1` (already exists)

3. **Release title:** `PL-Hub v0.5.1 - Language-Independent Commands`

4. **Description:** Copy from `RELEASE_NOTES.md` or use this template:

   ```markdown
   # PL-Hub v0.5.1 - Language-Independent Commands

   ## 🎉 Major Features

   ### Language-Independent Commands
   - **Short Platform Names** - `plhub build apk` instead of `python plhub.py build --target android`
   - **No Python Prefix** - Use `plhub run app.poh` just like `git`, `npm`, `docker`
   - **Global Accessibility** - Works from any directory after installation
   - **Automated Installation** - `install.bat` (Windows) and `install.sh` (Linux/macOS)
   - **Professional CLI** - Commands like `plhub build apk --release`, `plhub build ipa`, `plhub build exe`

   ## 🐛 Bug Fixes
   - Fixed Python 3.9 compatibility issues
   - Cleaned up old Python runtime architecture
   - Improved SDK compatibility

   ## 📦 Downloads
   - **SDK Package:** `plhub-sdk-0.5.1.zip` (attached below)
   - **Install via git:** `git clone https://github.com/AlhaqGH/PLHub && cd PLHub && ./install.sh`

   ## 📚 Documentation
   - [Installation Guide](INSTALL_AND_USAGE.md)
   - [Language-Independent Commands](LANGUAGE_INDEPENDENT_COMMANDS.md)
   - [Complete Changelog](CHANGELOG.md)

   ## ✅ Compatibility
   - Python 3.9, 3.10, 3.11, 3.12
   - Windows, macOS, Linux
   - Rust runtime required
   ```

5. **Upload artifacts:**
   - `plhub-sdk-0.5.1.zip`
   - `plhub-sdk-0.5.1.zip.sha256`

6. **Click "Publish release"**

### Automated Method (Using GitHub CLI)

```powershell
# Install GitHub CLI if not installed
# winget install GitHub.cli

# Login to GitHub
gh auth login

# Create release
gh release create v0.5.1 `
  --title "PL-Hub v0.5.1 - Language-Independent Commands" `
  --notes-file RELEASE_NOTES.md `
  plhub-sdk-0.5.1.zip `
  plhub-sdk-0.5.1.zip.sha256

# Verify release
gh release view v0.5.1
```

---

## 🐍 Option 2: Publish to PyPI

### Prerequisites

```powershell
# Install build and twine
pip install build twine

# Set up PyPI credentials (one-time setup)
# Create account at https://pypi.org/account/register/
# Generate API token at https://pypi.org/manage/account/token/
```

### Build the Package

```powershell
# Navigate to PLHub directory
cd C:\Users\habib\POHLANG\PLHub

# Clean previous builds
if (Test-Path dist) { Remove-Item -Recurse -Force dist }
if (Test-Path build) { Remove-Item -Recurse -Force build }
if (Test-Path *.egg-info) { Remove-Item -Recurse -Force *.egg-info }

# Build the package
python -m build

# Verify build
ls dist/
# Should show:
#   plhub-0.5.1-py3-none-any.whl
#   plhub-0.5.1.tar.gz
```

### Test Upload (Recommended First Time)

```powershell
# Upload to TestPyPI first
python -m twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ plhub==0.5.1

# If successful, proceed to real PyPI
```

### Upload to PyPI

```powershell
# Upload to real PyPI
python -m twine upload dist/*

# Enter your PyPI API token when prompted
# Or set environment variable:
$env:TWINE_PASSWORD = "pypi-your-token-here"
python -m twine upload -u __token__ dist/*
```

### Verify Installation

```powershell
# Test pip install
pip install plhub==0.5.1

# Verify version
plhub --version
# Should show: PL-Hub v0.5.1 - PohLang Development Environment with Language-Independent Commands
```

---

## 🎯 Option 3: Complete Release (GitHub + PyPI)

### Step-by-Step Process

1. **Build for PyPI:**
   ```powershell
   python -m build
   ```

2. **Upload to PyPI:**
   ```powershell
   python -m twine upload dist/*
   ```

3. **Create GitHub Release:**
   ```powershell
   gh release create v0.5.1 `
     --title "PL-Hub v0.5.1 - Language-Independent Commands" `
     --notes-file RELEASE_NOTES.md `
     plhub-sdk-0.5.1.zip `
     plhub-sdk-0.5.1.zip.sha256
   ```

4. **Update README badges:**
   Add PyPI version badge:
   ```markdown
   [![PyPI version](https://badge.fury.io/py/plhub.svg)](https://badge.fury.io/py/plhub)
   ```

5. **Announce the release:**
   - Update README with installation instructions
   - Post on social media / forums
   - Update documentation site

---

## 🔍 Post-Release Verification

### GitHub Release Checks
```powershell
# Check release exists
gh release view v0.5.1

# Download and verify SDK zip
gh release download v0.5.1 --pattern "plhub-sdk-0.5.1.zip"
```

### PyPI Release Checks
```powershell
# Check package on PyPI
# Visit: https://pypi.org/project/plhub/0.5.1/

# Test fresh installation
pip install --upgrade plhub
plhub --version
plhub doctor
```

### Integration Tests
```powershell
# Test all major commands
plhub create test_project
cd test_project
plhub run src/main.poh
plhub build
plhub test
cd ..
Remove-Item -Recurse -Force test_project
```

---

## 📊 Release Metrics to Track

After release, monitor:
- GitHub release downloads
- PyPI download statistics
- GitHub stars/forks
- Issue reports
- User feedback

---

## 🚨 Common Issues & Solutions

### Issue: PyPI Upload Fails
**Solution:** Check credentials, ensure version doesn't already exist

### Issue: GitHub Release Upload Fails
**Solution:** Check file paths, ensure tag exists, verify GitHub token

### Issue: SDK Zip Missing Files
**Solution:** Regenerate SDK with `python tools/update_sdk.py --sync`

---

## 📝 Quick Command Reference

```powershell
# Build package
python -m build

# Test upload
python -m twine upload --repository testpypi dist/*

# Real upload
python -m twine upload dist/*

# GitHub release
gh release create v0.5.1 --notes-file RELEASE_NOTES.md plhub-sdk-0.5.1.zip

# Verify
pip install plhub==0.5.1
plhub --version
```

---

## 🎊 Ready to Release?

Choose your release strategy:
- ✅ **GitHub Only:** Simple, open source distribution
- ✅ **PyPI Only:** Professional Python package
- ✅ **Both:** Maximum reach and professionalism

**Recommendation:** Start with **GitHub Release** (easiest), then add PyPI later if needed.

---

## 📞 Need Help?

- Check `tools/release_automation.py` for automation
- Review `RELEASE_CHECKLIST.md` for detailed steps
- See `SDK_ZIP_RELEASE_GUIDE.md` for SDK specifics

**You're ready to release PLHub v0.5.1! 🚀**
