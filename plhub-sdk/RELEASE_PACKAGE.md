# PL-Hub v0.5.0 - Release Package

## 📦 Package Information

**Version**: 0.5.0  
**Package Name**: plhub-sdk.zip  
**Package Size**: 9.3 MB (9,302,249 bytes)  
**Release Date**: January 2025  
**License**: MIT  
**Status**: ✅ READY FOR DISTRIBUTION

## 🎉 What's Included

### Core Files
- **plhub.py** (1,990 lines) - Main CLI entry point with v0.5.0 features
- **setup.py** - Python package installation script
- **README.md** - Complete documentation with v0.5.0 features
- **CHANGELOG.md** - Detailed version history
- **MANIFEST.in** - Package manifest for distribution

### Automation Tools (`tools/`)
- **build_automation.py** - Build system with watch mode, incremental compilation
- **test_runner.py** - Test automation with watch mode, CI/CD reports
- **hot_reload.py** - Hot reload server and debug infrastructure
- **project_structure.py** (903 lines) - Project scaffolding with 4 templates
- **style_manager.py** - UI theme management
- **widget_manager.py** - Widget template system

### Project Templates (`templates/`)
- **basic.poh** - Simple starter template
- **console.poh** - Interactive CLI template
- **web.poh** - Web application template
- **vscode/tasks.json** - 7 pre-configured VS Code tasks
- **vscode/launch.json** - 5 debug configurations

### Documentation (`docs/`)
- **AUTOMATION_GUIDE.md** (88KB) - Complete automation workflows
- **RELEASE_v0.5.0.md** - Release summary and examples
- **QUICK_REFERENCE.md** - Command reference and tips
- **cli_reference.md** - CLI command documentation
- **development_workflow.md** - Development best practices
- **getting_started.md** - Getting started guide

### Additional Components
- **CLI/** - Command-line interface implementation
- **Editor/** - Editor integrations (VS Code extension support)
- **Examples/** - Example projects and tutorials
- **Runtime/** - PohLang runtime integration

## 🚀 Quick Start

### Installation

```bash
# Extract the SDK
unzip plhub-sdk.zip -d plhub
cd plhub

# Install dependencies (optional)
pip install watchdog  # For better file watching

# Verify installation
python plhub.py --version
# Output: PL-Hub v0.5.0 - PohLang Development Environment with Automation

# Check environment
python plhub.py doctor
```

### Create Your First Project

```bash
# Create a new project (choose a template)
python plhub.py create my_app --template basic      # Simple starter
python plhub.py create my_cli --template console    # Interactive CLI
python plhub.py create my_lib --template library    # Reusable library
python plhub.py create my_web --template web        # Web application

# Navigate to project
cd my_app

# Run the project
python ../plhub.py run src/main.poh

# Start development with hot reload
python ../plhub.py dev
```

## ✨ Key Features (v0.5.0)

### 🤖 Development Automation
- **Build Automation** - Watch mode, incremental builds, dependency detection
- **Test Automation** - Auto-discovery, watch mode, CI/CD integration
- **Hot Reload** - Instant feedback with state preservation
- **Debug Server** - Breakpoint infrastructure and runtime inspection

### 📦 Professional Templates
- **Basic** - Simple starter for learning (4 directories, 5 files)
- **Console** - Interactive CLI with menu system (8 directories, 8 files)
- **Library** - Reusable package with modular structure (8 directories, 8 files)
- **Web** - Web application structure for future features

### 🔧 VS Code Integration
- **7 Pre-configured Tasks**: Run, Build, Watch, Test, Dev Server, Debug, Clean
- **5 Debug Configurations**: Run/Debug file, Run/Debug tests, Attach to server
- **Problem Matchers**: Automatic error detection and reporting
- **Background Tasks**: Long-running processes with proper lifecycle

### 📚 Comprehensive Documentation
- **88KB Automation Guide**: Complete workflows, best practices, troubleshooting
- **Release Summary**: Feature highlights and examples
- **Quick Reference**: Command reference and tips
- **Migration Guide**: Upgrade instructions (none needed - fully backward compatible)

## 🛠 Command Reference

### Project Management
```bash
python plhub.py create <name> [--template <type>]  # Create project
python plhub.py init                                # Initialize current dir
python plhub.py clean                               # Clean build artifacts
```

### Development
```bash
python plhub.py run <file.poh>                     # Run a program
python plhub.py build [--release|--debug]          # Build project
python plhub.py test [--watch] [--ci]              # Run tests
python plhub.py watch                               # Auto-rebuild on changes
python plhub.py dev                                 # Hot reload server
python plhub.py debug                               # Debug session
```

### Build Options
```bash
python plhub.py build                               # Default: bytecode
python plhub.py build --release                     # Optimized build
python plhub.py build --debug                       # Debug build
python plhub.py build --target bytecode             # Bytecode target
python plhub.py build --target dart                 # Dart transpilation
python plhub.py build --target native               # Native compilation
```

### Environment
```bash
python plhub.py doctor [--verbose]                 # Check environment
python plhub.py sync-runtime-local                 # Sync local runtime
python plhub.py update-runtime [--version <v>]     # Update runtime
```

### UI Toolkit
```bash
python plhub.py style list                         # List themes
python plhub.py style apply <theme>                # Apply theme
python plhub.py widget list                        # List widgets
python plhub.py widget generate <template> <name>  # Generate widget
```

## 📊 What's New in v0.5.0

### Major Changes
1. **Full Automation Stack** - Build, test, hot reload, and debug automation
2. **Professional Templates** - 4 complete project templates with best practices
3. **VS Code Integration** - Automatic task and debug configuration generation
4. **Build Improvements** - Added --release and --debug flags, default to bytecode
5. **Documentation** - 88KB automation guide and comprehensive references

### New Commands
- `python plhub.py watch` - Automatic rebuild on file changes
- `python plhub.py dev` - Hot reload development server
- `python plhub.py debug` - Start debug session
- `python plhub.py test --watch` - Continuous testing
- `python plhub.py test --ci` - Generate CI/CD reports
- `python plhub.py build --release` - Optimized builds
- `python plhub.py build --debug` - Debug builds

### Bug Fixes
- Fixed test command path resolution issues
- Fixed relative path errors in test output
- Improved error handling in project creation
- Better cleanup on project creation failures

## 🎯 Use Cases

### Learning PohLang
```bash
python plhub.py create tutorial --template basic
cd tutorial
python ../plhub.py dev  # Hot reload for instant feedback
```

### Building CLI Tools
```bash
python plhub.py create my_tool --template console
cd my_tool
python ../plhub.py run src/main.poh
```

### Creating Libraries
```bash
python plhub.py create utils_lib --template library
cd utils_lib
# Edit src/core/ and src/utils/
python ../plhub.py test --watch
```

### Web Development (Future)
```bash
python plhub.py create my_site --template web
cd my_site
python ../plhub.py dev  # Hot reload server
```

## 🔧 System Requirements

### Required
- Python 3.9 or higher
- Windows, macOS, or Linux
- PohLang Rust runtime (synced or downloaded)

### Optional
- Dart SDK (for Dart transpilation)
- watchdog library (for efficient file watching): `pip install watchdog`
- VS Code (for IDE integration)

## 📝 Template Details

### Basic Template Structure
```
my_app/
├── src/main.poh       # Simple hello world
├── tests/             # Test examples
├── examples/          # Usage examples
├── docs/              # Documentation
├── .vscode/           # VS Code config
├── .gitignore
├── plhub.json
└── README.md
```

### Console Template Structure
```
my_cli/
├── src/
│   ├── main.poh       # Menu-driven CLI
│   ├── commands/      # Command handlers
│   └── utils/         # Utilities
├── tests/             # Test suite
├── examples/          # CLI examples
├── docs/              # Documentation
├── .vscode/
├── USAGE.md           # Usage instructions
├── plhub.json
└── README.md
```

### Library Template Structure
```
my_lib/
├── src/
│   ├── lib.poh        # Library entry
│   ├── core/          # Core functions
│   └── utils/         # Utility functions
├── tests/             # Test suite
├── examples/          # API examples
├── docs/
│   ├── api.md         # API docs
│   └── README.md
├── .vscode/
├── USAGE.md
├── plhub.json
└── README.md
```

## 🎓 Learning Resources

### Documentation Files
- **README.md** - Main documentation with examples
- **docs/AUTOMATION_GUIDE.md** - Complete automation workflows
- **docs/QUICK_REFERENCE.md** - Quick command reference
- **docs/getting_started.md** - Beginner's guide
- **docs/development_workflow.md** - Best practices

### Example Projects
- **Examples/hello_world.poh** - Simple hello world
- **Examples/poh/** - Various PohLang examples
- Template projects include working examples

### Online Resources
- GitHub: https://github.com/AlhaqGH/PLHub
- Issues: https://github.com/AlhaqGH/PLHub/issues
- PohLang Core: https://github.com/AlhaqGH/PohLang

## 🐛 Known Issues

1. **Web Template** - Placeholder for future web features
2. **Debug Server** - Requires additional runtime support (in development)
3. **Hot Reload** - May not preserve all application state types
4. **Test Parsing** - Some advanced PohLang syntax may have parsing issues (runtime-level)

## 🔮 Future Plans (v0.6.0)

- Full web framework integration
- Package registry with dependency resolution
- Remote debugging support
- Performance profiling tools
- Code coverage reports
- LSP (Language Server Protocol) integration
- Plugin system for extensibility

## 💬 Support & Feedback

### Getting Help
1. Check documentation: `docs/` directory
2. Run `python plhub.py doctor --verbose` for diagnostics
3. Check AUTOMATION_GUIDE.md for workflows
4. Search issues: https://github.com/AlhaqGH/PLHub/issues

### Reporting Issues
- GitHub Issues: https://github.com/AlhaqGH/PLHub/issues
- Include output of `python plhub.py doctor --verbose`
- Provide steps to reproduce

### Contributing
Contributions welcome! See CONTRIBUTING.md (if available) or open an issue to discuss.

## 📜 License

MIT License - See LICENSE file for details.

## 🙏 Acknowledgments

Thank you to all contributors and users of PL-Hub and PohLang!

---

**PL-Hub v0.5.0** - Making PohLang development fast, efficient, and enjoyable.

**Download**: plhub-sdk.zip (9.3 MB)  
**Install**: `unzip plhub-sdk.zip && cd plhub && python plhub.py --version`  
**Start**: `python plhub.py create my_app --template basic`

🚀 Happy Coding!
