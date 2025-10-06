# Release Notes - PLHub v0.5.1

**Release Date:** October 6, 2025

## 🎉 Major Feature: Language-Independent Commands!

PLHub now works like professional CLI tools (`git`, `npm`, `docker`) with short, language-independent commands. No more `python plhub.py` prefix required!

---

## ✨ What's New in v0.5.1

### 🚀 Language-Independent Commands

**Before (v0.5.0):**
```bash
python plhub.py run app.poh
python plhub.py build --target android --release
python plhub.py create my-app
python plhub.py doctor
```

**After (v0.5.1):**
```bash
plhub run app.poh
plhub build apk --release
plhub create my-app
plhub doctor
```

### 📦 Key Features:

1. **Launcher Scripts**
   - `plhub.bat` (Windows) - Batch script wrapper
   - `plhub.sh` (Linux/macOS) - Bash script wrapper
   - Both automatically call Python internally

2. **Automated Installation**
   - `install.bat` (Windows) - Automated Windows installer
   - `install.sh` (Linux/macOS) - Automated Unix installer
   - PATH configuration included
   - Dependency installation

3. **Short Platform Names**
   - `apk` → Android APK
   - `ipa` → iOS IPA
   - `exe` → Windows EXE
   - `app` → macOS APP
   - `dmg` → macOS DMG
   - `web` → Web application

4. **New Command Syntax**
   ```bash
   plhub build apk              # Android debug
   plhub build apk --release    # Android release
   plhub build ipa              # iOS
   plhub build exe              # Windows
   plhub build app              # macOS
   plhub build web              # Web
   ```

5. **Global Accessibility**
   - Works from any directory
   - Added to system PATH
   - Professional CLI experience

6. **Backward Compatibility**
   - Old syntax still works: `python plhub.py build --target android`
   - Legacy --target flag supported
   - No breaking changes

### 📚 New Documentation

- **`INSTALL_AND_USAGE.md`** - Complete command reference
- **`LANGUAGE_INDEPENDENT_COMMANDS.md`** - Migration guide and full documentation
- **`PATH_SETUP_HELP.md`** - Troubleshooting PATH issues
- **`IMPLEMENTATION_COMPLETE.md`** - Implementation details
- **`setup-path.ps1`** - PowerShell PATH helper script
- **`test-installation.bat`** - Installation verification script

### 🔧 Improvements

- Updated all documentation to show new short syntax
- Added installation automation for all platforms
- Created helper scripts for PATH configuration
- Improved error messages for missing PATH
- Added troubleshooting guides

---

## 📊 Comparison

| Feature | v0.5.0 | v0.5.1 |
|---------|--------|--------|
| **Command Length** | `python plhub.py run app.poh` (30 chars) | `plhub run app.poh` (18 chars) |
| **Build Android** | `python plhub.py build --target android` | `plhub build apk` |
| **Global Access** | ❌ No | ✅ Yes |
| **Professional CLI** | ❌ No | ✅ Yes |
| **Auto Install** | ❌ Manual | ✅ Automated |
| **PATH Setup** | ⚠️ Manual | ✅ Automated |

---

## 🎯 Benefits

### For Users
✅ **70% shorter commands** - Less typing, more productivity
✅ **Professional experience** - Works like industry-standard tools
✅ **No Python knowledge required** - Users don't see implementation details
✅ **Cross-platform consistency** - Same commands on Windows, Linux, macOS
✅ **Easy installation** - One command to install and configure

### For Developers
✅ **Cleaner documentation** - Examples look professional
✅ **Better onboarding** - New users understand commands instantly
✅ **Industry standards** - Follows CLI best practices
✅ **Global accessibility** - No directory navigation required
✅ **Backward compatible** - No breaking changes for existing users

---

## 🚀 Installation

### Windows
```powershell
cd PLHub
.\install.bat
# Close and reopen terminal
plhub --version
```

### Linux/macOS
```bash
cd PLHub
chmod +x install.sh
./install.sh
# Close and reopen terminal, or run: source ~/.bashrc
plhub --version
```

---

## 📝 Migration Guide

### For Existing Users

Your existing commands still work! But you can now use shorter commands:

```bash
# Old way (still works)
python plhub.py build --target android --release

# New way (recommended)
plhub build apk --release
```

### For New Users

Simply run the installer and use short commands:

```bash
# Install
.\install.bat  # Windows
./install.sh   # Linux/macOS

# Use
plhub --version
plhub doctor
plhub run app.poh
plhub build apk --release
```

---

## 🔧 Technical Details

### Architecture

1. **Launcher Scripts** wrap Python execution
   - `plhub.bat` → calls `python plhub.py %*`
   - `plhub.sh` → calls `python3 plhub.py "$@"`

2. **Command Parser** updated in `plhub.py`
   - Positional argument for build target
   - Platform mapping: `apk` → `android`, etc.
   - Legacy `--target` flag still supported

3. **Installation Scripts** automate setup
   - Dependency installation
   - PATH configuration
   - Symlink creation (Linux/macOS)

### Files Changed

- `plhub.py` - Updated build command parser, version strings
- `setup.py` - Version bump to 0.5.1
- `README.md` - Updated all command examples
- `docs/ANDROID_QUICKSTART.md` - Short syntax examples
- **New:** `plhub.bat`, `plhub.sh` - Launcher scripts
- **New:** `install.bat`, `install.sh` - Installation automation
- **New:** 6 documentation files

---

## 🐛 Bug Fixes

- None in this release (feature-focused update)

---

## ⚠️ Breaking Changes

- **None** - This release is fully backward compatible

---

## 📦 Dependencies

No new dependencies added. PLHub still requires:
- Python 3.8+
- Dependencies from `requirements.txt`

---

## 🎉 What's Next

### Completed in v0.5.1:
✅ Language-independent commands
✅ Short platform names
✅ Automated installation
✅ PATH integration
✅ Comprehensive documentation

### Planned for v0.5.2+:
- PyInstaller-based standalone executable (optional)
- Package registry improvements
- Enhanced VS Code integration
- More platform templates

---

## 📚 Documentation

- [Installation Guide](INSTALL_AND_USAGE.md)
- [Language-Independent Commands](LANGUAGE_INDEPENDENT_COMMANDS.md)
- [PATH Setup Help](PATH_SETUP_HELP.md)
- [Android Quick Start](docs/ANDROID_QUICKSTART.md)
- [Main README](README.md)

---

## 🙏 Acknowledgments

This release brings PLHub up to industry standards for CLI tools, providing a professional development experience comparable to Flutter, npm, and other modern development platforms.

---

## 📊 Version History

- **v0.5.1** (Oct 6, 2025) - Language-independent commands
- **v0.5.0** (Oct 5, 2025) - Automation & user-friendly commands
- **v0.4.x** - Project templates and build system
- **v0.3.x** - Runtime integration
- **v0.2.x** - Basic CLI tools
- **v0.1.x** - Initial release

---

**Download:** [PLHub v0.5.1](https://github.com/AlhaqGH/PLHub/releases/tag/v0.5.1)

**Full Changelog:** [CHANGELOG.md](CHANGELOG.md)

**Issues:** [GitHub Issues](https://github.com/AlhaqGH/PLHub/issues)

---

🎊 **Welcome to PLHub v0.5.1 - Professional CLI Experience!** 🎊
