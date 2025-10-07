# PL-Hub v0.5.1 - Language-Independent Commands

## 🎉 Major Features

### Language-Independent Commands
- **Short Platform Names** - `plhub build apk` instead of `python plhub.py build --target android`
- **No Python Prefix** - Use `plhub run app.poh` just like `git`, `npm`, `docker`
- **Global Accessibility** - Works from any directory after installation
- **Automated Installation** - `install.bat` (Windows) and `install.sh` (Linux/macOS)
- **Professional CLI** - Commands like `plhub build apk --release`, `plhub build ipa`, `plhub build exe`

## 🐛 Bug Fixes & Improvements
- Fixed Python 3.9 compatibility issues (dataclass slots, union types)
- Cleaned up old Python runtime architecture (6,461+ lines removed)
- Improved SDK compatibility (removed non-existent tool imports)
- Added .gitkeep files for empty directories
- Full CI/CD pipeline coverage (Python 3.9-3.12)

## 📦 Installation Options

### Option 1: Quick Install (Recommended)
```bash
# Clone and install globally
git clone https://github.com/AlhaqGH/PLHub
cd PLHub

# Windows
.\install.bat

# Linux/macOS
chmod +x install.sh && ./install.sh
```

After installation, restart your terminal and use PLHub from anywhere:
```bash
plhub --version
plhub doctor
plhub create my-project
```

### Option 2: Download SDK Package
Download `plhub-sdk-0.5.1.zip` from **Assets** below:
1. Click `plhub-sdk-0.5.1.zip` to download
2. Extract the zip file
3. Navigate to the extracted folder
4. Follow the README instructions

### Option 3: Use Without Installation
```bash
git clone https://github.com/AlhaqGH/PLHub
cd PLHub
python plhub.py --version
python plhub.py run examples/hello.poh
```

## ✅ System Requirements
- **Python:** 3.9, 3.10, 3.11, or 3.12
- **Platforms:** Windows, macOS, Linux
- **Runtime:** PohLang Rust runtime (included in installation)

## 🚀 Quick Start

```bash
# After installation
plhub create my-app
cd my-app
plhub run src/main.poh
plhub build
```

## 📚 Documentation
- [Installation & Usage Guide](https://github.com/AlhaqGH/PLHub/blob/main/INSTALL_AND_USAGE.md)
- [Language-Independent Commands](https://github.com/AlhaqGH/PLHub/blob/main/LANGUAGE_INDEPENDENT_COMMANDS.md)
- [Complete Changelog](https://github.com/AlhaqGH/PLHub/blob/main/CHANGELOG.md)
- [Quick Reference](https://github.com/AlhaqGH/PLHub/blob/main/QUICK_REFERENCE.md)

## 🎯 What's New in v0.5.1

### Before (v0.5.0):
```bash
python plhub.py run app.poh
python plhub.py build --target android --release
python plhub.py create my-project
```

### Now (v0.5.1):
```bash
plhub run app.poh
plhub build apk --release
plhub create my-project
```

### Technical Improvements:
- Pure Rust runtime (removed 6,461+ lines of Python interpreter code)
- Python 3.9+ compatibility (previously required 3.10+)
- Cleaner architecture (SDK separated from full package)
- All CI tests passing (9/9 on Python 3.9-3.12)

## 🙏 Credits
Thanks to all contributors who helped make PLHub better!

## 📊 Release Assets

| Asset | Description | Size |
|-------|-------------|------|
| `plhub-sdk-0.5.1.zip` | Complete SDK package | 9.15 MB |
| `plhub-sdk-0.5.1.zip.sha256` | Checksum for verification | 87 B |
| `Source code (zip)` | Full source code | Auto-generated |
| `Source code (tar.gz)` | Full source code | Auto-generated |

### Verify SDK Download
```bash
# Windows (PowerShell)
(Get-FileHash plhub-sdk-0.5.1.zip -Algorithm SHA256).Hash -eq (Get-Content plhub-sdk-0.5.1.zip.sha256)

# Linux/macOS
sha256sum -c plhub-sdk-0.5.1.zip.sha256
```

---

**Full Changelog:** https://github.com/AlhaqGH/PLHub/compare/v0.5.0...v0.5.1
