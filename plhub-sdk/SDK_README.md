# PLHub SDK Structure & Purpose

**PLHub is the complete development framework for PohLang** - think Flutter for Dart, or .NET SDK for C#.

## SDK vs Runtime Distinction

### PohLang Language SDK (in `/PohLang/`)
- **Purpose**: Embed PohLang in applications, create language bindings
- **Contents**: Runtime binary, language spec (Grammar.ebnf), API docs
- **For**: Language developers, tool builders, embedders
- **Example use**: "I want to add PohLang scripting to my C++ game"

### PLHub Development Framework SDK (this package)
- **Purpose**: Build complete applications with PohLang
- **Contents**: CLI tools, project templates, build system, UI toolkit, platform targets
- **For**: Application developers, software engineers
- **Example use**: "I want to build an Android app with PohLang"

## PLHub SDK Components

```
plhub-sdk/
├── cli/                        # Command-line tools
│   ├── plhub.py                # Main CLI entry point
│   ├── commands/               # Command implementations
│   └── utils/                  # CLI utilities
│
├── runtime/                    # Embedded PohLang runtime
│   ├── bin/pohlang(.exe)       # Language runtime binary
│   ├── Interpreter/            # Python fallback interpreter
│   ├── transpiler/             # Dart transpiler
│   └── pohlang_metadata.json   # Version tracking
│
├── templates/                  # Project scaffolding
│   ├── basic/                  # Simple starter
│   ├── console/                # CLI applications
│   ├── library/                # Reusable packages
│   └── web/                    # Web applications
│
├── editor/                     # Editor integrations
│   ├── vscode/                 # VS Code extension
│   ├── language-server/        # LSP implementation
│   └── syntax/                 # Syntax definitions
│
├── tools/                      # Development tools
│   ├── build/                  # Build system
│   ├── test/                   # Testing framework
│   ├── debug/                  # Debugger
│   └── format/                 # Code formatter
│
├── styles/                     # UI theming system
│   ├── themes/                 # 6 built-in themes
│   └── widgets/                # 16 widget templates
│
├── examples/                   # Sample applications
│   ├── complete-apps/          # Full applications
│   │   ├── calculator/         # Android calculator APK
│   │   ├── todo-manager/       # CRUD application
│   │   └── number-game/        # Game with high scores
│   └── tutorials/              # Learning examples
│
├── docs/                       # Comprehensive documentation
│   ├── getting_started.md
│   ├── cli_reference.md
│   ├── AUTOMATION_GUIDE.md
│   ├── CROSS_PLATFORM_GUIDE.md
│   ├── UI_TOOLKIT.md
│   └── development_workflow.md
│
├── setup.py                    # Python package installer
├── requirements.txt            # Dependencies
├── README.md                   # Main documentation
└── SDK_README.md               # This file
```

## What PLHub SDK Provides

### 1. Complete Development Environment
Like **Flutter** provides `flutter create`, `flutter run`, `flutter build`, PLHub provides:
```bash
plhub create my-app --template console
plhub run src/main.poh
plhub build apk
```

### 2. Multi-Platform Build System
- **Android** APKs/AABs
- **iOS** IPAs
- **Windows** EXE/MSIX
- **macOS** DMG/App
- **Web** Progressive Web Apps

### 3. Project Management
- Project templates and scaffolding
- Configuration management
- Dependency resolution (coming soon)
- Version control integration

### 4. Development Automation
- **Watch mode**: Auto-rebuild on file changes
- **Hot reload**: Instant feedback during development
- **Test automation**: Watch mode for tests
- **Debug server**: Breakpoint support

### 5. UI Development Toolkit
- **6 professional themes** (light, dark, ocean, sunset, forest, high-contrast)
- **16 widget templates** (buttons, cards, forms, modals, etc.)
- Theme customization system
- Responsive layout helpers

### 6. Cross-Platform Testing
- Unit tests
- Integration tests
- UI tests
- E2E tests
- CI/CD integration (GitHub Actions, JUnit)

### 7. Editor Integration
- **VS Code tasks** (run, build, test, debug)
- **Launch configurations** for debugging
- **Problem matchers** for error reporting
- **Language server** for IntelliSense

### 8. Deployment Tools
- **Android**: Google Play Store, Firebase
- **iOS**: App Store, TestFlight
- **Windows**: Microsoft Store
- **macOS**: Mac App Store
- **Web**: Netlify, Vercel, Firebase

## Installation Methods

### Method 1: Python Package (Recommended)
```bash
pip install plhub
plhub --version
```

### Method 2: Standalone SDK
```bash
# Download plhub-sdk-{version}.tar.gz or .zip
tar -xzf plhub-sdk-{version}.tar.gz
cd plhub-sdk-{version}

# Linux/macOS
./install.sh

# Windows
install.bat
```

### Method 3: Development Setup
```bash
git clone https://github.com/AlhaqGH/PLHub
cd PLHub
pip install -e .
```

## SDK vs Language Runtime Comparison

| Feature | PohLang SDK | PLHub SDK |
|---------|-------------|-----------|
| **Purpose** | Language embedding | App development |
| **Primary users** | Tool builders | App developers |
| **Contains** | Runtime + specs | CLI + tools + templates |
| **Example use** | "Embed PohLang in C++" | "Build Android app" |
| **Key files** | libpohlang, Grammar.ebnf | plhub CLI, templates |
| **Analogy** | Python C API | Django/Flask |
| **Size** | ~50 MB | ~200 MB |
| **Dependencies** | None (standalone) | Python 3.9+ |

## Quick Start Examples

### Example 1: Create Console App
```bash
plhub create calculator --template console
cd calculator
plhub run src/main.poh
```

### Example 2: Build Android APK
```bash
cd examples/android-calculator
plhub build apk
# Output: build/android/calculator-debug.apk
```

### Example 3: Development with Hot Reload
```bash
plhub create my-app
cd my-app
plhub dev  # Hot reload enabled
# Edit src/main.poh - changes apply instantly!
```

### Example 4: Apply UI Theme
```bash
plhub style list
plhub style apply ocean_blue
plhub widget generate button --name PrimaryButton
```

### Example 5: Cross-Platform Build
```bash
plhub platform create android MyApp
plhub platform run android --hot-reload
plhub platform test android
plhub platform build android --config release
```

## Embedded Runtime

PLHub SDK includes the PohLang runtime binary for immediate use:
- **Location**: `runtime/bin/pohlang(.exe)`
- **Version**: Tracked in `runtime/pohlang_metadata.json`
- **Update**: `plhub update-runtime --version latest`
- **Local sync**: `plhub sync-runtime-local` (for development)

## Documentation Structure

- **README.md** - Overview and quick start
- **SDK_README.md** - This file (SDK structure)
- **docs/getting_started.md** - First steps
- **docs/cli_reference.md** - Complete command reference
- **docs/AUTOMATION_GUIDE.md** - Watch, hot reload, testing
- **docs/CROSS_PLATFORM_GUIDE.md** - Android, iOS, Web, etc.
- **docs/UI_TOOLKIT.md** - Themes and widgets
- **docs/development_workflow.md** - Best practices

## System Requirements

### Minimum
- **OS**: Windows 10/11, macOS 13+, Ubuntu 20.04+
- **Python**: 3.9 or higher
- **RAM**: 4 GB
- **Storage**: 500 MB

### Platform-Specific
- **Android**: Java JDK 11+, Android Studio, Android SDK
- **iOS**: macOS 13+, Xcode 15+
- **Windows apps**: Visual Studio 2022, .NET 8.0
- **Web**: Node.js 18+

## Troubleshooting

### Command not found
```bash
# Verify installation
plhub --version

# If not found, check PATH
# Windows: Add %APPDATA%\plhub to PATH
# Linux/macOS: Add ~/.local/bin to PATH
```

### Runtime not found
```bash
plhub doctor          # Check environment
plhub update-runtime  # Download runtime
```

### Build errors
```bash
plhub clean          # Clean build artifacts
plhub doctor         # Check requirements
```

## Support & Resources

- **Issues**: https://github.com/AlhaqGH/PLHub/issues
- **Discussions**: https://github.com/AlhaqGH/PLHub/discussions
- **PohLang Language**: https://github.com/AlhaqGH/PohLang
- **Documentation**: Full docs in `docs/` directory

## License

MIT License - Same as PohLang project

---

**PLHub SDK** = Complete development framework for building PohLang applications

**PohLang SDK** = Language runtime and specs for embedding/tooling

Choose the right SDK for your needs!
