# PL-Hub SDK v0.5.0 - Distribution Package

**Official PohLang Development Environment SDK**

## 📦 What's Included

This SDK package contains everything needed to develop PohLang applications with full automation support.

### Core Components

- **plhub.py** - Main CLI tool (1,994 lines)
- **setup.py** - Python package installer
- **install_official_runtime.py** - Official PohLang v0.5.0 runtime installer

### Automation Tools (`tools/`)

- **build_automation.py** - Incremental builds with watch mode
- **test_runner.py** - Test automation with CI/CD support
- **hot_reload.py** - Development server with instant reload
- **project_structure.py** - Project scaffolding system (951 lines)
- **style_manager.py** - UI theme management
- **widget_manager.py** - Widget template system

### Project Templates (`templates/`)

Four professional project templates with PohLang v0.5.0 features:
- **basic.poh** - Simple starter template
- **console.poh** - Interactive CLI application
- **web.poh** - Web application structure
- **vscode/** - VS Code tasks and debug configurations

### Documentation (`docs/`)

- **AUTOMATION_GUIDE.md** (88KB) - Complete automation workflows
- **RELEASE_v0.5.0.md** - Release summary
- **QUICK_REFERENCE.md** - Command reference
- **cli_reference.md** - CLI documentation
- **development_workflow.md** - Best practices
- **getting_started.md** - Beginner's guide

### Additional Files

- **README.md** - Complete documentation
- **CHANGELOG.md** - Version history
- **COMPATIBILITY.md** - PohLang v0.5.0 compatibility report
- **KNOWN_ISSUES.md** - Known runtime issues and workarounds
- **RELEASE_CHECKLIST.md** - Pre-release verification
- **RELEASE_PACKAGE.md** - Distribution guide

## 🚀 Quick Start

### 1. Installation

```bash
# Extract the SDK
unzip plhub-sdk.zip -d plhub
cd plhub

# Install PohLang v0.5.0 runtime (Windows)
python install_official_runtime.py

# Verify installation
python plhub.py doctor
```

### 2. Create Your First Project

```bash
# Create a project (choose template)
python plhub.py create my_app --template basic

# Navigate to project
cd my_app

# Run the application
python ../plhub.py run src/main.poh

# Start development with hot reload
python ../plhub.py dev
```

### 3. Explore Features

```bash
# Run examples
python ../plhub.py run examples/example.poh

# Run tests
python ../plhub.py test

# Build for distribution
python ../plhub.py build --release
```

## ✨ Key Features

### Development Automation

- **Build Automation** - Watch mode, incremental compilation, caching
- **Test Automation** - Auto-discovery, watch mode, CI/CD reports
- **Hot Reload** - Instant feedback with state preservation
- **Debug Support** - Breakpoint infrastructure

### Professional Templates

| Template | Description | Files | Use Case |
|----------|-------------|-------|----------|
| **basic** | Simple starter | 5 files, 4 dirs | Learning PohLang |
| **console** | Interactive CLI | 8 files, 8 dirs | Command-line tools |
| **library** | Reusable package | 8 files, 8 dirs | Shared libraries |
| **web** | Web application | 8 files, 8 dirs | Web apps (future) |

### PohLang v0.5.0 Support

All 20 phrasal built-in expressions supported:

**Mathematical**: `total of`, `smallest in`, `largest in`, `absolute value of`, `round`, `round down`, `round up`

**String**: `make uppercase`, `make lowercase`, `trim spaces from`

**Collection**: `first in`, `last in`, `reverse of`, `count of`, `join...with`, `split...by`, `contains...in`, `remove...from`, `append...to`, `insert...at...in`

### VS Code Integration

Every project includes:
- **7 pre-configured tasks** (Run, Build, Watch, Test, Dev, Debug, Clean)
- **5 debug configurations** (Run/Debug file, Run/Debug tests, Attach to server)

## 📋 System Requirements

### Required
- Python 3.9 or higher
- Windows, macOS, or Linux

### Optional
- Dart SDK (for Dart transpilation)
- watchdog library (for efficient file watching): `pip install watchdog`
- VS Code (for IDE integration)

## 🎯 Common Commands

```bash
# Project Management
python plhub.py create <name> --template <type>  # Create project
python plhub.py init                              # Initialize current dir
python plhub.py clean                             # Clean artifacts

# Development
python plhub.py run <file.poh>                   # Run program
python plhub.py build [--release|--debug]        # Build project
python plhub.py test [--watch] [--ci]            # Run tests
python plhub.py watch                             # Auto-rebuild
python plhub.py dev                               # Hot reload server
python plhub.py debug                             # Debug session

# Environment
python plhub.py doctor                            # Check environment
python plhub.py sync-runtime-local                # Sync local runtime

# UI Toolkit
python plhub.py style list                        # List themes
python plhub.py widget list                       # List widgets
```

## ⚠️ Known Issues

### Multi-line If Statements

The PohLang v0.5.0 official runtime has a parser issue with multi-line If statements using phrasal comparisons.

**What doesn't work:**
```poh
If temperature is greater than 20
    Write "Warm"
Otherwise
    Write "Cool"
End If
```

**Workaround - Use inline If:**
```poh
If temperature is greater than 20 Write "Warm" Otherwise Write "Cool"
```

**All other features work perfectly**, including all 20 phrasal expressions!

See `KNOWN_ISSUES.md` for details and workarounds.

## 📚 Documentation

| Document | Description |
|----------|-------------|
| **README.md** | Main documentation with examples |
| **AUTOMATION_GUIDE.md** | Complete automation workflows (88KB) |
| **QUICK_REFERENCE.md** | Command reference and tips |
| **COMPATIBILITY.md** | PohLang v0.5.0 compatibility |
| **KNOWN_ISSUES.md** | Known issues and workarounds |
| **RELEASE_PACKAGE.md** | Distribution guide |

## 🎓 Learning Path

### Beginners
1. Install runtime: `python install_official_runtime.py`
2. Create basic project: `python plhub.py create my_app --template basic`
3. Explore examples: `python plhub.py run my_app/examples/example.poh`
4. Modify and learn

### Intermediate
1. Create console app: `python plhub.py create my_cli --template console`
2. Enable hot reload: `python plhub.py dev`
3. Write tests: `python plhub.py test --watch`
4. Build for distribution: `python plhub.py build --release`

### Advanced
1. Create library: `python plhub.py create my_lib --template library`
2. Design APIs using phrasal expressions
3. Document and test comprehensively
4. Distribute your library

## 🔗 Links

- **PohLang Repository**: https://github.com/AlhaqGH/PohLang
- **PLHub Repository**: https://github.com/AlhaqGH/PLHub
- **Official Release**: https://github.com/AlhaqGH/PohLang/releases/tag/v0.5.0
- **Issues**: https://github.com/AlhaqGH/PLHub/issues

## 📄 License

MIT License - See LICENSE file for details.

## 🙏 Credits

Developed by the PohLang team to make programming accessible through natural language.

## 💬 Support

- Documentation: See `docs/` directory
- Run diagnostics: `python plhub.py doctor --verbose`
- Report issues: https://github.com/AlhaqGH/PLHub/issues

---

**PL-Hub v0.5.0** - Making PohLang development fast, efficient, and enjoyable.

**Download**: plhub-sdk.zip  
**Install**: Extract and run `python install_official_runtime.py`  
**Start**: `python plhub.py create my_app --template basic`

🚀 Happy Coding with PohLang v0.5.0!
