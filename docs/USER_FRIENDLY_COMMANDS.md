# PLHub User-Friendly Command Reference

**Making PLHub commands intuitive, helpful, and easy to use** 🚀

## Overview

PLHub now features enhanced user experience across all commands with:

✅ **Beautiful Progress Indicators** - See exactly what's happening  
✅ **Helpful Error Messages** - Clear errors with solutions  
✅ **Interactive Wizards** - Guided setup for complex tasks  
✅ **Smart Suggestions** - Did-you-mean for typos  
✅ **Colored Output** - Easy-to-read terminal output  
✅ **Progress Tracking** - Downloads, builds, and installations

---

## Enhanced Commands

### 📦 Installation & Setup

#### `plhub install <package>`
**Now with visual feedback:**

```bash
$ plhub install web_framework

🚀 Installing web_framework

⠋ Resolving web_framework...
✅ Resolved web_framework@2.1.0

→ Downloading package...
⬇️  web_framework: 45.2% (2.3/5.1 MB) at 1.2 MB/s ETA: 2s
✅ Package verified

⠋ Installing...
✅ web_framework installed successfully

✅ Completed in 3.2s
```

**Features:**
- Real-time download progress with speed and ETA
- Package verification
- Dependency resolution preview
- Rollback on failure
- Size and version information

**Interactive Mode:**
```bash
$ plhub install

ℹ️  Package name: web_framework
ℹ️  Version [latest]: 2.1.0
ℹ️  Install location [project]: 
ℹ️  Install dependencies? [Y/n]: y

📋 Installation Summary:
   Package: web_framework
   Version: 2.1.0
   Location: ./plhub_modules
   Dependencies: 3 packages

ℹ️  Proceed with installation? [Y/n]: y
```

---

### 🏗️ Building Projects

#### `plhub build`
**Enhanced with progress tracking:**

```bash
$ plhub build --target dart --release

🚀 Build Configuration

🏗️  Building project

[1] Checking dependencies...
✅ All dependencies resolved

[2] Compiling source files...
⠋ Compiling... ████████████████████░░░░  75% (15/20 files)
✅ Compilation complete

[3] Optimizing...
⠋ Running optimizations...
✅ Optimization complete

[4] Generating artifacts...
✅ Build artifacts ready

📦 Build Artifacts
  • dist/main.dart (45.2 KB)
  • dist/main.dart.js (123.4 KB)
  • dist/assets/ (2.1 MB)

💡 Tip: Artifacts saved to: dist/

✅ Build completed in 12.5s
```

**Interactive Build Configuration:**
```bash
$ plhub build --interactive

🏗️  Build Configuration

ℹ️  Build target
  [1] python
  [2] dart
  [3] native
  [4] bytecode (default)

Select [1-4]: 2

ℹ️  Build configuration
  [1] debug (default)
  [2] release

Select [1-2]: 2

ℹ️  Enable optimizations? [Y/n]: y

📋 Build Summary:
   Target: dart
   Configuration: release
   Optimizations: enabled

ℹ️  Start build? [Y/n]: y
```

---

### 🚀 Creating Projects

#### `plhub create <name>`
**Now with interactive wizard:**

```bash
$ plhub create

✨ Create New Project

Let's set up your new PohLang project!

ℹ️  Project name: my_awesome_app

ℹ️  Select project template
  [1] basic (default)
  [2] console
  [3] web
  [4] library

Select [1-4]: 3

ℹ️  Include UI toolkit? [Y/n]: y

ℹ️  Select target platforms (leave empty to skip)
ℹ️    Target Android? [y/N]: y
ℹ️    Target iOS? [y/N]: n
ℹ️    Target macOS? [y/N]: n
ℹ️    Target Windows? [y/N]: n
ℹ️    Target Web? [y/N]: y

📋 Project Configuration
   Name: my_awesome_app
   Template: web
   UI Toolkit: Yes
   Platforms: android, web

ℹ️  Create project with these settings? [Y/n]: y

→ Creating project structure...
✅ Project structure created

→ Installing dependencies...
✅ Dependencies installed

→ Setting up platforms...
✅ Android project initialized
✅ Web project initialized

→ Configuring UI toolkit...
✅ UI toolkit configured

✅ Project 'my_awesome_app' created successfully!

📁 Location: ./my_awesome_app
📦 Structure: 12 directories, 24 files

🚀 Next Steps:
  1. cd my_awesome_app
  2. plhub run src/main.poh
  3. plhub platform run android

✅ Completed in 5.3s
```

---

### 🐛 Debugging

#### `plhub debug <file>`
**Enhanced debugging experience:**

```bash
$ plhub debug src/main.poh

🐛 Debug Session

→ Starting debug server on port 5858
ℹ️  File: src/main.poh

📋 Debug Instructions
  • Set breakpoints in your code
  • Connect your IDE debugger to localhost:5858
  • Press Ctrl+C to stop debugging

────────────────────────────────────────────────────

ℹ️  Debug server ready
💡 Tip: See docs/debugging.md for IDE setup instructions

Listening on ws://localhost:5858
Waiting for debugger connection...

✅ Debugger connected from 127.0.0.1:51234

🟢 Debug session active
   Breakpoints: 3
   Watch expressions: 2

► Paused at src/main.poh:15
   15 |   Set count to count plus 1
   16 |   Write "Count: " plus count
   17 | End

Variables:
   count = 5
   name = "Alice"

Commands:
   [c]ontinue  [s]tep  [n]ext  [p]rint  [q]uit

debug> 
```

**Runtime Error Display:**
```bash
❌ Runtime Errors (2)

1. Line 15: Division by zero
   in src/calculator.poh

   13 | Set result to numerator divide denominator
   14 | Write "Result: " plus result
   15 | # Error occurred here
      | ^^^^^^^^^^^^^^^^^^^^^^

💡 Tip: Check if denominator is zero before dividing

2. Line 23: Undefined variable 'total'
   in src/main.poh

   21 | Set count to 5
   22 | Repeat count
   23 |   Write total  # 'total' not defined
      |         ^^^^^

💡 Tip: Initialize 'total' before using it
```

---

### 🌐 Platform Development

#### `plhub platform create <platform> <name>`
**With platform detection:**

```bash
$ plhub platform create android myapp

🚀 Creating android project: myapp

⚙️  Platform Status
  ✅ android      Available
  ✗ ios          Not Available
  ✗ macos        Not Available
  ✅ windows      Available
  ✅ web          Available

💡 Tip: To enable ios, macos, install the required SDKs

→ Creating project structure...
✅ Project structure created

→ Configuring Gradle...
✅ Gradle configured

→ Setting up Android manifest...
✅ Manifest created

✓ Project created at: ./myapp
  Platform: android
  Package: com.pohlang.myapp

📋 Next Steps:
  1. Open project in Android Studio
  2. Sync Gradle files
  3. Run: plhub platform run android
  4. Connect device or start emulator

✅ Completed in 2.1s
```

#### `plhub platform devices`
**Interactive device selection:**

```bash
$ plhub platform devices --platform android

📱 Available Android Devices

  [1] Pixel 5 (emulator) online
  [2] Samsung Galaxy S21 (device) online
  [3] Nexus 5X (emulator) offline

ℹ️  Select device [1-3]: 1

→ Selected: Pixel 5 (emulator-5554)

🚀 Launch app on this device? [Y/n]: y

→ Installing APK...
⠋ Installing... ██████████████████████████  100%
✅ App installed

→ Launching app...
✅ App launched successfully

💡 Tip: Enable hot reload with --hot-reload flag
```

---

### 📥 Downloading & Updates

#### `plhub update-runtime`
**With download progress:**

```bash
$ plhub update-runtime

🚀 Update PohLang Runtime

🔍 Checking for latest version...
✅ Found PohLang SDK v0.5.0

→ Downloading PohLang SDK...
⬇️  pohlang-sdk-0.5.0.zip: 67.3% (34.5/51.2 MB) at 2.3 MB/s ETA: 7s

✅ Download complete

→ Verifying checksum...
ℹ️  SDK zip SHA256: a1b2c3d4e5f6...
✅ Checksum verified

→ Extracting runtime...
⠋ Extracting... ████████████████░░░░  80% (16/20 files)
✅ Runtime extracted

→ Installing binary...
✅ Installed pohlang.exe -> Runtime/bin/pohlang.exe

→ Updating metadata...
✅ Updated metadata: Runtime/pohlang_metadata.json

✅ Runtime update complete
```

---

### 🧪 Testing

#### `plhub test`
**With detailed progress:**

```bash
$ plhub test

🚀 Run Tests

🔍 Finding test files...
✅ Found 8 test files

🧪 Running Tests
────────────────────────────────────────────────────

📝 tests/test_arithmetic.poh
    ✅ PASSED (0.3s)

📝 tests/test_collections.poh
    ✅ PASSED (0.5s)

📝 tests/test_functions.poh
    ❌ FAILED (0.2s)
    Error: Expected 10, got 9

📝 tests/test_control_flow.poh
    ✅ PASSED (0.4s)

📝 tests/test_imports.poh
    ✅ PASSED (0.1s)

📝 tests/test_syntax.poh
    ✅ PASSED (0.2s)

📝 tests/test_types.poh
    ✅ PASSED (0.3s)

📝 tests/test_errors.poh
    ✅ PASSED (0.2s)

────────────────────────────────────────────────────

📊 Test Results:
   Total: 8 tests
   Passed: 7 (87.5%)
   Failed: 1 (12.5%)
   Duration: 2.2s

❌ Test suite failed

💡 Tip: Run with --verbose to see detailed output
💡 Tip: Run 'plhub test --filter test_functions' to re-run failed tests
```

---

### ❓ Getting Help

#### Smart Command Suggestions
**When you make a typo:**

```bash
$ plhub biuld

❌ Command 'biuld' not found

💡 Did you mean:
  plhub build
  plhub list

ℹ️  Run plhub --help to see all commands
```

#### Context-Aware Help
**When stuck:**

```bash
$ plhub create myapp
❌ Error: Directory 'myapp' already exists.

💡 Try these solutions:
  1. Use a different name: plhub create myapp2
  2. Remove existing directory: rm -rf myapp
  3. Use --force to overwrite: plhub create myapp --force

ℹ️  Run 'plhub create --help' for more options
```

---

### 🩺 System Diagnostics

#### `plhub doctor`
**Comprehensive health check:**

```bash
$ plhub doctor

🔍 PLHub Environment Diagnostics
════════════════════════════════════════════════════════════

✅ Python: 3.11.5

📦 PohLang Runtime:
  ✅ Found: Runtime/bin/pohlang.exe
  ✅ Version: 0.5.0

📋 Runtime Metadata:
  Version: 0.5.0
  Source: local_build

🐍 Python Interpreter (fallback):
  ✅ Python interpreter available

🎯 Dart SDK (optional):
  ✅ Dart version 3.1.0

📁 Project Configuration:
  ✅ Project: myapp
  📌 Version: 1.0.0
  📦 Dependencies: 3

📝 Templates: 4 available

⚙️  Platform Status:
  ✅ android      Available
  ✗ ios          Not Available
  ✗ macos        Not Available
  ✅ windows      Available
  ✅ web          Available

════════════════════════════════════════════════════════════

✅ All checks passed! PLHub is ready to use.

💡 Tip: To enable iOS/macOS development, install Xcode on macOS
```

---

## Environment Variables

Configure PLHub behavior:

```bash
# Disable colors (for CI/CD)
PLHUB_NO_COLOR=1

# Change cache location
PLHUB_CACHE=/path/to/cache

# Custom registry URL
PLHUB_REGISTRY=https://packages.example.com

# Verbose output by default
PLHUB_VERBOSE=1

# Use specific Python interpreter
PLHUB_PYTHON=/usr/bin/python3.11
```

---

## Tips & Tricks

### 🎨 Colorful Output
PLHub automatically detects terminal capabilities and enables colored output when supported. Disable with:
```bash
plhub <command> --no-color
# or
export PLHUB_NO_COLOR=1
```

### ⚡ Quick Commands
Common shortcuts:
```bash
# Quick run (same as 'plhub run')
plhub Examples/hello.poh

# Auto-detect and fix
plhub doctor --fix

# Interactive mode
plhub create   # No arguments = wizard mode
plhub build --interactive
```

### 📊 Progress Bars
All long-running operations show progress:
- Downloads with speed and ETA
- Builds with file count
- Tests with pass/fail status
- Installations with verification

### 🔍 Smart Suggestions
PLHub learns from your usage:
- Suggests commands for typos
- Recommends related commands
- Shows common next steps
- Contextual help messages

### 💡 Helpful Errors
Every error includes:
- Clear description
- Probable cause
- Suggested solutions
- Related documentation

---

## Examples

### Complete Workflow
```bash
# 1. Check system
$ plhub doctor
✅ All checks passed!

# 2. Create project (interactive)
$ plhub create
✨ Create New Project
ℹ️  Project name: calculator
ℹ️  Select project template: console
✅ Project created!

# 3. Develop
$ cd calculator
$ code src/main.poh

# 4. Test as you go
$ plhub run src/main.poh
✅ Program executed successfully

# 5. Run tests
$ plhub test
✅ All tests passed

# 6. Build for production
$ plhub build --release
✅ Build completed in 3.2s

# 7. Deploy
$ plhub publish
✅ Published to registry
```

### Error Recovery
```bash
$ plhub build

❌ Build failed: Missing dependency 'math_utils'

💡 Install it with:
$ plhub install math_utils

$ plhub install math_utils
✅ math_utils installed

$ plhub build
✅ Build completed
```

---

## Keyboard Shortcuts

During interactive prompts:
- `Ctrl+C` - Cancel operation
- `Ctrl+D` - Use default value
- `↑`/`↓` - Navigate history
- `Tab` - Auto-complete (where supported)

---

## Getting More Help

- 📚 Full documentation: `docs/`
- 💬 Command help: `plhub <command> --help`
- 🔍 System check: `plhub doctor`
- 🌐 Online docs: https://pohlang.org/docs
- 🐛 Report issues: https://github.com/AlhaqGH/PLHub/issues

---

## Feedback

We're constantly improving the user experience. Have suggestions?
- Open an issue on GitHub
- Join our community Discord
- Email: feedback@pohlang.org

**Happy coding with PLHub!** 🎉
