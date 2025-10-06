# 🎉 PLHub Language-Independent Commands

**PLHub now works like professional CLI tools!**

No more `python plhub.py` - just type `plhub` directly! 🚀

---

## 📦 What Changed?

### Before (Old Way)
```bash
python plhub.py run app.poh
python plhub.py build --target android --release
python plhub.py create my-app
python plhub.py doctor
```

### After (New Way) ✨
```bash
plhub run app.poh
plhub build apk --release
plhub create my-app
plhub doctor
```

---

## 🛠 Installation

### Windows

```powershell
cd PLHub
.\install.bat
```

**What it does:**
- ✅ Checks Python installation
- ✅ Installs dependencies from `requirements.txt`
- ✅ Adds PLHub to your PATH
- ✅ Creates `plhub.bat` launcher
- ✅ Configures system-wide or user-only access

**After installation:**
- Close and reopen PowerShell/Terminal
- Type `plhub --version` to verify

### Linux/macOS

```bash
cd PLHub
chmod +x install.sh
./install.sh
```

**What it does:**
- ✅ Checks Python 3 and pip installation
- ✅ Installs dependencies from `requirements.txt`
- ✅ Makes `plhub.sh` executable
- ✅ Creates symlink in `~/.local/bin/plhub`
- ✅ Adds to PATH (interactive prompt)
- ✅ Detects your shell (.bashrc, .zshrc, .profile)

**After installation:**
- Run `source ~/.bashrc` (or your shell config)
- Or close and reopen terminal
- Type `plhub --version` to verify

---

## 🎯 New Command Syntax

### Run Commands
```bash
# Old
python plhub.py run app.poh

# New
plhub run app.poh
```

### Build Commands (Short Platform Names)

#### Android APK
```bash
# Old
python plhub.py build --target android
python plhub.py build --target android --release

# New
plhub build apk
plhub build apk --release
```

#### iOS IPA
```bash
# Old
python plhub.py build --target ios --release

# New
plhub build ipa --release
```

#### Windows EXE
```bash
# Old
python plhub.py build --target windows --release

# New
plhub build exe --release
```

#### macOS APP
```bash
# Old
python plhub.py build --target macos --release

# New
plhub build app --release
plhub build dmg --release  # Also supported
```

#### Web
```bash
# Old
python plhub.py build --target web

# New
plhub build web
```

#### Other Targets (unchanged)
```bash
plhub build                    # Bytecode (default)
plhub build bytecode
plhub build dart               # Transpile to Dart
plhub build native             # Native compilation
```

### Platform Mapping

| Short Name | Full Platform | Description |
|------------|---------------|-------------|
| `apk` | `android` | Android APK package |
| `ipa` | `ios` | iOS app package |
| `exe` | `windows` | Windows executable |
| `app` | `macos` | macOS application |
| `dmg` | `macos` | macOS disk image |
| `web` | `web` | Web application |

### Project Management
```bash
# Old
python plhub.py create my-app
python plhub.py init
python plhub.py clean

# New
plhub create my-app
plhub init
plhub clean
```

### Environment Commands
```bash
# Old
python plhub.py doctor
python plhub.py sync-runtime-local
python plhub.py update-runtime

# New
plhub doctor
plhub sync-runtime-local
plhub update-runtime
```

### Development Commands
```bash
# Old
python plhub.py watch
python plhub.py dev
python plhub.py test
python plhub.py debug

# New
plhub watch
plhub dev
plhub test
plhub debug
```

### UI Toolkit Commands
```bash
# Old
python plhub.py style list
python plhub.py widget generate button

# New
plhub style list
plhub widget generate button
```

---

## 🔧 Technical Implementation

### Launcher Scripts

**Windows (`plhub.bat`):**
```batch
@echo off
setlocal

REM Get the directory where plhub.bat is located
set "PLHUB_ROOT=%~dp0"

REM Check if Python is available
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python not found in PATH
    echo Please install Python 3.8 or higher
    exit /b 1
)

REM Run plhub.py with all arguments
python "%PLHUB_ROOT%plhub.py" %*
```

**Linux/macOS (`plhub.sh`):**
```bash
#!/usr/bin/env bash

# Get the directory where plhub.sh is located
PLHUB_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 not found"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Run plhub.py with all arguments
python3 "$PLHUB_ROOT/plhub.py" "$@"
```

### Command Parser Changes

**In `plhub.py`:**
```python
# Old: Positional argument with --target flag
build_parser.add_argument('--target', choices=['python', 'dart', 'android', ...])

# New: Direct positional argument with short names
build_parser.add_argument('target', nargs='?', default='bytecode',
    choices=['python', 'dart', 'native', 'bytecode', 'apk', 'ipa', 'exe', 'app', 'dmg', 'web', ...])

# New: Platform mapping
target_map = {
    'apk': 'android',
    'ipa': 'ios',
    'exe': 'windows',
    'app': 'macos',
    'dmg': 'macos',
}
target = target_map.get(target, target)

# Backward compatibility
build_parser.add_argument('--target', dest='legacy_target', ...)
if args.legacy_target:
    target = args.legacy_target
```

---

## ✅ Backward Compatibility

**Old commands still work!** We maintain full backward compatibility:

```bash
# Still works (legacy syntax)
python plhub.py build --target android --release
python plhub.py run app.poh

# New syntax (recommended)
plhub build apk --release
plhub run app.poh
```

---

## 📖 Updated Documentation

The following documentation has been updated to use new syntax:

- ✅ `README.md` - Main PLHub documentation
- ✅ `INSTALL_AND_USAGE.md` - Complete installation and usage guide
- ✅ `docs/ANDROID_QUICKSTART.md` - Android quick start guide
- ✅ This file - Language-independent commands reference

**Still using old syntax:**
- `docs/ANDROID_APK_GUIDE.md` (to be updated)
- `docs/COMPLETE_APP_GUIDE.md` (to be updated)
- Example README files (to be updated)

---

## 🐛 Troubleshooting

### Command Not Found

**Symptoms:**
```bash
$ plhub --version
plhub: command not found
```

**Windows Fix:**
1. Close and reopen PowerShell/Terminal
2. Or run `install.bat` again
3. Or add manually:
   - Open "System Properties"
   - Click "Environment Variables"
   - Edit "Path" variable
   - Add: `C:\Users\YourName\POHLANG\PLHub`

**Linux/macOS Fix:**
```bash
# Reload shell configuration
source ~/.bashrc  # or ~/.zshrc

# Or add manually
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Verify symlink exists
ls -l ~/.local/bin/plhub
```

### Python Not Found

**Symptoms:**
```bash
$ plhub run app.poh
Error: Python not found in PATH
```

**Fix:**
Install Python 3.8 or higher:
- **Windows**: https://www.python.org/downloads/
- **Ubuntu/Debian**: `sudo apt install python3 python3-pip`
- **macOS**: `brew install python3`

### Permissions Error (Linux/macOS)

**Symptoms:**
```bash
$ plhub run app.poh
Permission denied
```

**Fix:**
```bash
chmod +x PLHub/plhub.sh
chmod +x ~/.local/bin/plhub
```

### Launcher Not Working

**Symptoms:**
Commands work with `python plhub.py` but not with `plhub`

**Windows:**
```powershell
# Check if plhub.bat exists
dir PLHub\plhub.bat

# If missing, create it manually or run install.bat
.\install.bat
```

**Linux/macOS:**
```bash
# Check if plhub.sh exists and is executable
ls -l PLHub/plhub.sh

# Check if symlink exists
ls -l ~/.local/bin/plhub

# If missing
./install.sh
```

---

## 🎯 Benefits

### For Users
✅ **Shorter commands** - `plhub run` vs `python plhub.py run`
✅ **Professional feel** - Works like `git`, `npm`, `docker`
✅ **No language prefix** - Don't need to know it's Python
✅ **Faster typing** - Less characters to type
✅ **Cross-platform** - Same experience on all platforms

### For Developers
✅ **Cleaner examples** - Documentation looks professional
✅ **Easier onboarding** - New users don't see Python implementation
✅ **Standard conventions** - Follows CLI best practices
✅ **Global accessibility** - Works from any directory
✅ **Backward compatible** - Old commands still work

---

## 🚀 Quick Examples

### Example 1: Run Hello World
```bash
# Navigate to examples
cd PLHub/examples/poh

# Run example
plhub run hello.poh
```

### Example 2: Build Android APK
```bash
# Navigate to calculator app
cd PLHub/Examples/android-calculator

# Build debug APK
plhub build apk

# Build release APK
plhub build apk --release

# Install on device
adb install build/android/android-calculator-debug.apk
```

### Example 3: Create New Project
```bash
# Create project
plhub create my-game --template console

# Navigate to project
cd my-game

# Run project
plhub run src/main.poh

# Build for Android
plhub build apk --release
```

### Example 4: Development Workflow
```bash
# Terminal 1: Hot reload
plhub dev

# Terminal 2: Watch tests
plhub test --watch

# Edit code - changes auto-reload!
```

### Example 5: Cross-Platform Build
```bash
# Build for multiple platforms
plhub build apk --release      # Android
plhub build ipa --release      # iOS
plhub build exe --release      # Windows
plhub build app --release      # macOS
plhub build web                # Web
```

---

## 📊 Comparison Table

| Feature | Old Way | New Way |
|---------|---------|---------|
| **Run command** | `python plhub.py run app.poh` | `plhub run app.poh` |
| **Build Android** | `python plhub.py build --target android` | `plhub build apk` |
| **Build iOS** | `python plhub.py build --target ios` | `plhub build ipa` |
| **Build Windows** | `python plhub.py build --target windows` | `plhub build exe` |
| **Create project** | `python plhub.py create app` | `plhub create app` |
| **Environment check** | `python plhub.py doctor` | `plhub doctor` |
| **Character count** | 30-50 chars | 15-25 chars |
| **Cross-platform** | ⚠️ Varies | ✅ Consistent |
| **Professional** | ❌ No | ✅ Yes |

---

## 🎉 Success!

PLHub now has language-independent commands! 🚀

**Before installation:**
```bash
python plhub.py build --target android --release
```

**After installation:**
```bash
plhub build apk --release
```

**Enjoy the new streamlined experience!** 🎊

---

## 📚 Next Steps

1. **Try it out**: `plhub --version`
2. **Check environment**: `plhub doctor`
3. **Run examples**: `plhub run examples/hello.poh`
4. **Build APK**: `cd Examples/android-calculator && plhub build apk`
5. **Read docs**: `INSTALL_AND_USAGE.md`

---

**Questions?** Check [INSTALL_AND_USAGE.md](INSTALL_AND_USAGE.md) for complete command reference!
