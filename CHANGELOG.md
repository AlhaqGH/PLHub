# Changelog

All notable changes to PL-Hub will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.1] - 2025-10-06

### Added

#### 🚀 Language-Independent Commands
- **Global CLI Access** - PLHub now works like professional tools (git, npm, docker)
  - Direct `plhub` command without `python` prefix
  - Works from any directory after installation
  - Automated PATH configuration

- **Launcher Scripts** - Cross-platform command wrappers
  - `plhub.bat` for Windows - Batch script wrapper calling Python internally
  - `plhub.sh` for Linux/macOS - Bash script wrapper with python3
  - Automatic Python detection and error handling
  - Passes all arguments transparently

- **Automated Installation** - One-command setup for all platforms
  - `install.bat` (Windows) - Interactive installer with PATH configuration
  - `install.sh` (Linux/macOS) - Shell-agnostic installer with symlink creation
  - Dependency installation from requirements.txt
  - Admin/sudo detection for system-wide vs user installation
  - PATH verification and setup instructions

- **Short Platform Names** - Intuitive build target syntax
  - `apk` → Android APK (instead of `--target android`)
  - `ipa` → iOS IPA (instead of `--target ios`)
  - `exe` → Windows EXE (instead of `--target windows`)
  - `app` → macOS APP (instead of `--target macos`)
  - `dmg` → macOS DMG (alternate macOS format)
  - `web` → Web application

- **Helper Scripts** - Troubleshooting and verification tools
  - `setup-path.ps1` - PowerShell PATH configuration helper
  - `test-installation.bat` - Installation verification script

#### 📚 Documentation
- **INSTALL_AND_USAGE.md** - Complete command reference with short syntax
- **LANGUAGE_INDEPENDENT_COMMANDS.md** - Full migration guide and technical details
- **PATH_SETUP_HELP.md** - Comprehensive PATH troubleshooting guide
- **IMPLEMENTATION_COMPLETE.md** - Implementation status and verification

### Changed

#### 🔄 Command Syntax
- **Build Command** - Now accepts positional target argument
  - Before: `python plhub.py build --target android --release`
  - After: `plhub build apk --release`
  - Legacy `--target` flag still supported for backward compatibility

- **All Commands** - Shortened by removing Python prefix
  - `plhub run app.poh` (was: `python plhub.py run app.poh`)
  - `plhub create my-app` (was: `python plhub.py create my-app`)
  - `plhub doctor` (was: `python plhub.py doctor`)
  - `plhub test` (was: `python plhub.py test`)

- **Documentation** - Updated throughout with new syntax
  - README.md - All examples use short commands
  - ANDROID_QUICKSTART.md - Updated build examples
  - All guide documents - Reflect new CLI experience

#### 🎨 Version Strings
- Updated version to 0.5.1 across all files
- Version description: "Language-Independent Commands"

### Fixed
- None (feature-focused release)

### Technical Details

#### Platform Mapping Implementation
```python
target_map = {
    'apk': 'android',
    'ipa': 'ios',
    'exe': 'windows',
    'app': 'macos',
    'dmg': 'macos',
}
```

#### Command Parser Updates
- Positional `target` argument with choices including short names
- Backward-compatible `--target` flag (dest='legacy_target')
- Priority: explicit target → legacy --target → default 'bytecode'

### Backward Compatibility
- ✅ All v0.5.0 commands continue to work
- ✅ `python plhub.py` syntax still supported
- ✅ `--target android` still works alongside `apk`
- ✅ No breaking changes

### Migration Guide
- **For existing users:** Both old and new syntax work
- **For new users:** Use short commands after installation
- **Recommendation:** Update documentation to new syntax for professionalism

---

## [0.5.0] - 2025-10-05

### Added

#### 🤖 Development Automation
- **Build Automation** - Intelligent build system with watch mode, incremental compilation, and dependency detection
  - SHA256-based change detection for efficient rebuilds
  - Dependency graph analysis to rebuild only affected files
  - Build caching to avoid unnecessary recompilation
  - Watch mode with configurable debouncing
  - Detailed build reports and statistics

- **Test Automation** - Comprehensive test runner with watch mode and CI/CD integration
  - Automatic test discovery in `tests/` directory
  - Watch mode for continuous testing during development
  - CI/CD report generation (GitHub Actions workflow, JUnit XML)
  - Test statistics and performance tracking
  - Colored output for better readability

- **Hot Reload Server** - Development server with instant feedback
  - File watching with automatic process restart
  - State preservation between reloads
  - Output streaming in separate thread
  - Graceful shutdown and cleanup
  - Configurable file patterns and debouncing

- **Debug Server** - Debugging infrastructure for runtime inspection
  - Breakpoint management system
  - Variable inspection support
  - Step execution planning (step over, step into, step out)
  - Debug session management
  - Integration with VS Code debugger

#### 📦 Project Templates
- **ProjectStructureGenerator** - Automated project scaffolding system
  - Four professional templates: basic, console, web, library
  - Complete directory structure generation
  - Pre-configured files with natural language PohLang code
  - Template-specific documentation and examples

- **Basic Template** - Simple starter for learning
  - Hello world with variables and arithmetic
  - Basic test examples
  - Minimal structure for quick prototyping

- **Console Template** - Interactive CLI applications
  - Menu-driven interface with natural language conditionals
  - User input handling patterns
  - Command structure for extensibility
  - Input validation examples

- **Library Template** - Reusable package creation
  - Modular structure (core/, utils/)
  - API documentation templates
  - Example usage patterns
  - Export/import guidelines

- **Web Template** - Web application structure
  - Route handlers placeholder
  - View templates structure
  - Static assets directory
  - Future web features foundation

#### 🔧 VS Code Integration
- **Automated Configuration Generation**
  - `tasks.json` with 7 pre-configured tasks:
    - Run PohLang File
    - Build Project
    - Watch and Build
    - Run Tests
    - Watch Tests
    - Start Dev Server
    - Debug
  - `launch.json` with 5 debug configurations:
    - Run Current File
    - Debug Current File
    - Run Tests
    - Debug Tests
    - Attach to Dev Server
  - Problem matchers for error reporting
  - Task groups for better organization

#### 📚 Documentation
- **AUTOMATION_GUIDE.md** - Comprehensive 88KB automation guide
  - Build automation workflows and best practices
  - Test automation strategies
  - Hot reload development workflows
  - Debug session management
  - CI/CD integration guides
  - Troubleshooting and FAQ

- **Updated README.md**
  - v0.5.0 feature highlights
  - Project template documentation
  - Automation workflow examples
  - Command reference updates

#### 🛠 CLI Commands
- `python plhub.py watch` - Watch mode with automatic rebuilds
- `python plhub.py dev` - Development server with hot reload
- `python plhub.py debug` - Start debug session
- `python plhub.py test --watch` - Watch mode for tests
- `python plhub.py test --ci` - Generate CI/CD reports
- Enhanced `create` command with `--template` option

### Changed
- **Project Creation** - Now uses automated ProjectStructureGenerator
  - Replaced manual directory/file creation
  - Added template selection support
  - Improved error handling and cleanup
  - Better progress reporting with file/directory counts

- **Version String** - Updated to "PL-Hub v0.5.0 - PohLang Development Environment with Automation"

- **UI Toolkit** - All widgets simplified to Phase 1 natural language only
  - No symbols, brackets, or complex code
  - Uses only: Set, Write, Ask for, If/Otherwise, While, Repeat times
  - ASCII characters only (no Unicode)

### Fixed
- Project structure consistency across all templates
- VS Code configuration file generation
- Error handling in project creation with automatic cleanup

### Dependencies
- Added optional `watchdog` library for efficient file watching
  - Falls back to polling-based watching if not installed
  - Recommended for better performance: `pip install watchdog`

## [0.4.0] - Previous Release

### Added
- UI Toolkit with StyleManager and WidgetManager
- Theme system with multiple built-in themes
- Widget template library
- Style commands (list, apply, create)
- Widget commands (list, generate)

## [0.3.0] - Previous Release

### Added
- Runtime integration with PohLang Rust runtime
- Doctor command for environment diagnostics
- Runtime sync capabilities
- Build system foundations

---

## Release Notes

### v0.5.0 Summary

This release transforms PL-Hub into a fully automated development environment with professional project templates, comprehensive automation tools, and seamless VS Code integration. The focus is on developer productivity through:

1. **Zero-configuration development** - Templates include everything needed
2. **Instant feedback loops** - Watch mode, hot reload, and continuous testing
3. **Production-ready structure** - All templates follow best practices
4. **Natural language code** - All templates use Phase 1 PohLang syntax only

### Migration Guide

**From v0.4.x to v0.5.0:**

1. **New Project Creation**: Now supports templates
   ```bash
   # Old way (still works)
   python plhub.py create my_app
   
   # New way (recommended)
   python plhub.py create my_app --template basic
   python plhub.py create my_cli --template console
   python plhub.py create my_lib --template library
   ```

2. **Automation Tools**: New commands available
   ```bash
   python plhub.py watch      # Build automation
   python plhub.py dev        # Hot reload
   python plhub.py debug      # Debug server
   python plhub.py test --watch  # Test automation
   ```

3. **VS Code Integration**: Automatically generated for new projects
   - `.vscode/tasks.json` - Build, run, test tasks
   - `.vscode/launch.json` - Debug configurations

### Known Issues
- Web template is placeholder for future features
- Debug server requires runtime support (in development)
- Hot reload may not preserve all state types

### Future Plans (v0.6.0)
- Full web framework integration
- Package registry implementation
- Remote debugging support
- Performance profiling tools
- Code coverage reports
