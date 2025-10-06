# 🚀 PLHub Installation & Quick Reference

## Installation

### Windows

```powershell
# Navigate to PLHub directory
cd PLHub

# Run installer (as Administrator for system-wide, or regular user for user-only)
.\install.bat
```

### Linux/macOS

```bash
# Navigate to PLHub directory
cd PLHub

# Make installer executable and run
chmod +x install.sh
./install.sh
```

After installation, **close and reopen your terminal** for PATH changes to take effect.

---

## Command Reference (Short Syntax)

### Basic Commands

```bash
# Check installation
plhub --version
plhub doctor

# Get help
plhub --help
plhub build --help
```

### Running Programs

```bash
# Run a PohLang program
plhub run app.poh
plhub run src/main.poh
plhub run examples/hello.poh --verbose
plhub run test.poh --debug
```

### Building Applications

#### Android APK
```bash
# Build debug APK (for testing)
plhub build apk

# Build release APK (optimized for production)
plhub build apk --release

# Build with custom output
plhub build apk --release --out MyApp.apk
```

#### iOS IPA
```bash
# Build iOS app (macOS only)
plhub build ipa
plhub build ipa --release
```

#### Windows EXE
```bash
# Build Windows executable
plhub build exe
plhub build exe --release
```

#### macOS APP
```bash
# Build macOS application
plhub build app
plhub build app --release
```

#### Web Application
```bash
# Build for web
plhub build web
```

#### Other Targets
```bash
# Build bytecode (default)
plhub build
plhub build bytecode

# Build Dart
plhub build dart

# Build native
plhub build native
```

### Project Management

```bash
# Create new project
plhub create my-app
plhub create my-app --template console
plhub create my-app --template android

# Initialize current directory
plhub init

# Clean build artifacts
plhhub clean
plhub clean --all
```

### Development

```bash
# Watch mode (auto-rebuild on changes)
plhub watch

# Development server with hot reload
plhub dev
plhub dev --file src/main.poh

# Debug session
plhub debug
plhub debug --port 5858
```

### Testing

```bash
# Run tests
plhub test
plhub test --verbose
plhub test --watch
plhub test --ci
```

### Package Management

```bash
# Install package
plhub install math_utils

# List items
plhub list examples
plhub list templates
plhub list packages
```

### Cross-Platform Commands

```bash
# Create platform project
plhub platform create android MyApp
plhub platform create ios MyApp

# Build platform project
plhub platform build android
plhub platform build ios --config release

# Run on platform
plhub platform run android
plhub platform run ios --device iPhone14

# List devices
plhub platform devices
plhub platform devices --platform android

# Launch emulator
plhub platform launch android pixel_6
```

---

## Quick Examples

### Example 1: Run Hello World
```bash
plhub run examples/hello.poh
```

### Example 2: Build Android APK
```bash
cd Examples/android-calculator
plhub build apk --release
adb install build/android/android-calculator-release.apk
```

### Example 3: Create and Run New App
```bash
plhub create my-app --template console
cd my-app
plhub run src/main.poh
```

### Example 4: Development with Hot Reload
```bash
cd my-app
plhub dev
# Edit src/main.poh - changes auto-reload
```

### Example 5: Build for Multiple Platforms
```bash
# Android
plhub build apk --release

# Web
plhub build web

# Windows
plhub build exe --release
```

---

## Command Comparison

### Old vs New Syntax

| Old Command | New Command |
|-------------|-------------|
| `python plhub.py run app.poh` | `plhub run app.poh` |
| `python plhub.py build --target android` | `plhub build apk` |
| `python plhub.py build --target android --release` | `plhub build apk --release` |
| `python plhub.py create my-app` | `plhub create my-app` |
| `python plhub.py doctor` | `plhub doctor` |

### Both syntaxes work! Old commands still supported for compatibility.

---

## Environment Variables

```bash
# Android SDK location (required for APK builds)
export ANDROID_HOME=/path/to/Android/Sdk         # Linux/Mac
$env:ANDROID_HOME = "C:\...\Android\Sdk"         # Windows PowerShell

# Java home (if not in PATH)
export JAVA_HOME=/path/to/jdk                    # Linux/Mac
$env:JAVA_HOME = "C:\...\Java\jdk-11"            # Windows PowerShell
```

---

## Troubleshooting

### Command Not Found

**Windows:**
1. Close and reopen terminal/PowerShell
2. Or add manually: `System Properties > Environment Variables > PATH > Add: C:\path\to\PLHub`

**Linux/macOS:**
1. Run: `source ~/.bashrc` (or `~/.zshrc`)
2. Or add manually: `echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc`

### Python Not Found

Install Python 3.8+:
- **Windows**: https://www.python.org/downloads/
- **Ubuntu**: `sudo apt install python3 python3-pip`
- **macOS**: `brew install python3`

### Permissions Error (Linux/macOS)

```bash
chmod +x PLHub/plhub.sh
chmod +x PLHub/install.sh
```

---

## Next Steps

1. **Verify Installation**: `plhub --version`
2. **Check Environment**: `plhub doctor`
3. **Try Examples**: `plhub run examples/hello.poh`
4. **Build APK**: `cd Examples/android-calculator && plhub build apk`
5. **Read Docs**: `docs/ANDROID_QUICKSTART.md`

---

## Full Documentation

- **Installation**: This file
- **Android APK Building**: `docs/ANDROID_APK_GUIDE.md`
- **Quick Start**: `docs/ANDROID_QUICKSTART.md`
- **Complete Apps**: `docs/COMPLETE_APP_GUIDE.md`
- **CLI Reference**: `docs/cli_reference.md`

---

**🎉 Enjoy using PLHub with short, language-independent commands!**
