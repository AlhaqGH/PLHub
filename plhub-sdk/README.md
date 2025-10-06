# PL-Hub

**PL-Hub (PohLang Hub) is the official development environment for the PohLang programming language.**

While **PohLang** is the core language (Rust runtime, parser, VM, and language specifications), **PL-Hub** provides the complete development ecosystem around it: tooling, project management, package system, editor integration, and deployment tools.

Think of it this way:
- **PohLang** is like **Dart** (the language runtime)
- **PL-Hub** is like **Flutter** (the development framework and tools)

## 🎉 v0.5.0 - Automation & Templates

**New in version 0.5.0:**

🤖 **Full Development Automation**
- **Build Automation** - Watch mode, incremental compilation, dependency detection
- **Test Automation** - Auto-discovery, watch mode, CI/CD integration (GitHub Actions, JUnit)
- **Hot Reload** - Instant feedback with state preservation
- **Debug Server** - Breakpoint infrastructure and runtime inspection

📦 **Professional Project Templates**
- **Basic** - Simple starter template for learning
- **Console** - Interactive CLI with menu system
- **Web** - Web application structure (placeholder for future)
- **Library** - Reusable package with API documentation

🔧 **VS Code Integration**
- Automated tasks.json generation (Run, Build, Watch, Test, Dev)
- Launch configurations for debugging
- Problem matchers for error reporting

📚 **Comprehensive Documentation**
- Complete [AUTOMATION_GUIDE.md](docs/AUTOMATION_GUIDE.md)
- Updated developer workflows
- Template usage examples

## ✨ What is PL-Hub?

PL-Hub is the comprehensive development platform for PohLang that provides:

🔹 **Runtime Integration** – seamlessly integrates PohLang Rust runtime  
🔹 **Project Management** – create, build, and manage PohLang projects  
🔹 **Environment Health Checks** – `doctor` command for diagnostics  
🔹 **Development Tools** – CLI tools for running, building, and testing  
🔹 **Build Automation** – watch mode, incremental builds, dependency detection  
🔹 **Hot Reload** – instant feedback with automatic reloading on file changes  
🔹 **Test Automation** – watch mode, CI/CD reports, auto-discovery  
🔹 **Debugging Support** – breakpoints, variable inspection, step execution  
🔹 **Templates & Scaffolding** – quick-start templates for different project types  
🔹 **Build System** – compile to bytecode, transpile to Dart, or interpret with Python  
🔹 **UI Toolkit** – style themes and reusable widgets for building interfaces  
🔹 **VS Code Integration** – tasks, launch configurations, problem matchers  
🔹 **Package System** – manage PohLang packages and dependencies (coming soon)  

## 🚀 Quick Start

### Installation

```bash
# Clone PLHub (the development environment)
git clone https://github.com/AlhaqGH/PLHub
cd PLHub

# Sync the Rust runtime (assumes PohLang is adjacent)
python plhub.py sync-runtime-local

# Or download official runtime
python plhub.py update-runtime --version latest

# Check environment
python plhub.py doctor
```

### Create Your First Project

```bash
# Create a new project with templates
python plhub.py create my_app --template basic      # Simple starter
python plhub.py create my_cli --template console    # Interactive CLI
python plhub.py create my_lib --template library    # Reusable package
python plhub.py create my_web --template web        # Web app (future)

# Navigate to project
cd my_app

# Run the project
python plhub.py run src/main.poh

# Explore generated structure
ls src/           # Source code
ls tests/         # Test files
ls examples/      # Example files
ls docs/          # Documentation
ls .vscode/       # VS Code configuration

# Explore UI assets (if --no-ui not specified)
ls ui/styles      # Active theme and README
ls ui/widgets     # Sample widgets
```

### Available Commands

```bash
# Environment Management
python plhub.py doctor              # Check environment health
python plhub.py sync-runtime-local  # Sync local Rust runtime
python plhub.py update-runtime      # Download official runtime

# Project Management
python plhub.py create <name>       # Create new project
python plhub.py init                # Initialize current directory
python plhub.py clean               # Clean build artifacts

# Development
python plhub.py run <file.poh>      # Run a PohLang program
python plhub.py build               # Build project
python plhub.py test                # Run tests

# Automation
python plhub.py watch               # Watch and rebuild automatically
python plhub.py dev                 # Start dev server with hot reload
python plhub.py test --watch        # Watch and re-run tests
python plhub.py debug               # Start debug session

# UI Toolkit
python plhub.py style list          # List available themes
python plhub.py style apply <theme> # Apply a theme to project
python plhub.py style create <name> # Create custom theme
python plhub.py widget list         # List widget templates
python plhub.py widget generate <t> # Generate widget from template

# Information
python plhub.py list examples       # List example programs
python plhub.py list templates      # List project templates
python plhub.py --version           # Show version
```

## 📂 Project Structure

```
PLHub/                          # Development Environment
│
├─ Runtime/                    # PohLang Rust runtime integration
│  ├─ bin/                     # Runtime binary (pohlang.exe)
│  ├─ Interpreter/             # Python interpreter (fallback)
│  ├─ transpiler/              # Dart transpiler
│  └─ pohlang_metadata.json    # Runtime version tracking
├─ CLI/                        # Command-line interface tools
├─ Editor/                     # Editor integrations & language server
├─ Examples/                   # Example projects and tutorials
├─ Modules/                    # Shared modules and libraries
├─ templates/                  # Project templates (basic, console, web)
├─ styles/                     # Built-in theme definitions
├─ widgets/                    # Widget template library
├─ tools/                      # Development and build tools
├─ Tests/                      # PLHub environment tests
├─ docs/                       # PLHub documentation and guides
├─ plhub.py                    # Main PLHub entry point
├─ setup.py                    # PLHub installation script
├─ PLHUB_DEVELOPER_GUIDE.md    # Comprehensive developer guide
├─ PLHUB_QUICK_REFERENCE.md    # Quick command reference
└─ README.md                   # This file

PohLang/                       # Core Language (separate repository)
├─ runtime/                    # Rust runtime (parser, VM, compiler)
│  ├─ src/                     # Runtime source code
│  ├─ tests/                   # Runtime tests
│  └─ Cargo.toml               # Rust project configuration
├─ spec/                       # Language specifications
├─ examples/                   # Language examples
└─ doc/                        # Language documentation
```

## 🛠 Development Workflow

### 1. Create Project
```bash
python plhub.py create calculator --template console
cd calculator
```

### 2. Develop
Edit `src/main.poh`:
```poh
Start Program

Write "Simple Calculator"
Ask for first_number
Ask for second_number
Set result to first_number plus second_number
Write "Result: " plus result

End Program
```

### 3. Run & Test
```bash
# Run with Rust runtime (fast)
python plhub.py run src/main.poh

# Run all tests
python plhub.py test
```

### 4. Build
```bash
# Build to bytecode (recommended)
python plhub.py build --target bytecode

# Or transpile to Dart
python plhub.py build --target dart
```

### 5. Environment Check
```bash
# Verify everything is working
python plhub.py doctor --verbose
```

## � Runtime Integration

PL-Hub seamlessly integrates with the PohLang Rust runtime, providing optimal performance while maintaining fallback compatibility.

### Runtime Priority

1. **Runtime/bin/pohlang.exe** - Primary Rust runtime (preferred)
2. **bin/pohlang.exe** - Legacy location
3. **PATH environment** - System-wide installation
4. **Python Interpreter** - Fallback if no Rust runtime found

### Syncing Local Builds

During development, easily sync your local Rust runtime:

```bash
# Build the runtime (in PohLang repo)
cargo build --manifest-path ../PohLang/runtime/Cargo.toml

# Sync to PLHub
python plhub.py sync-runtime-local

# Or sync release build for performance
cargo build --release --manifest-path ../PohLang/runtime/Cargo.toml
python plhub.py sync-runtime-local --profile release
```

### Downloading Official Releases

```bash
# Get latest release
python plhub.py update-runtime --version latest

# Get specific version
python plhub.py update-runtime --version 0.5.0

# Verify installation
python plhub.py doctor
```

### Runtime Metadata

PLHub tracks runtime information in `Runtime/pohlang_metadata.json`:

```json
{
  "pohlang_version": "0.5.0",
  "source_repo": "https://github.com/AlhaqGH/PohLang",
  "build_profile": "debug",
  "installed_at": "2025-10-05T12:00:00Z",
  "source": "local_build"
}
```

## 🎯 Project Templates

**PL-Hub v0.5.0** includes professional project templates with complete structure:

### Available Templates

| Template | Description | Use Case |
|----------|-------------|----------|
| **basic** | Simple starter | Learning PohLang fundamentals |
| **console** | Interactive CLI | Command-line applications with menus |
| **library** | Reusable package | Creating shared libraries and modules |
| **web** | Web application | Web apps (placeholder for future) |

### Template Features

All templates include:
- ✅ Complete directory structure (src/, tests/, examples/, docs/)
- ✅ Natural language PohLang code (Phase 1 syntax only)
- ✅ README with usage instructions
- ✅ .gitignore for version control
- ✅ VS Code tasks.json and launch.json
- ✅ Test structure and examples
- ✅ Project configuration (plhub.json)

### Creating Projects

```bash
# Basic starter project
python plhub.py create my_app --template basic

# Interactive console application
python plhub.py create my_cli --template console

# Reusable library package
python plhub.py create my_lib --template library

# Web application (experimental)
python plhub.py create my_web --template web
```

### Customization Options

```bash
# Skip UI scaffolding
python plhub.py create my_app --template basic --no-ui

# Choose custom theme
python plhub.py create styled_app --ui-theme midnight_dark
```

**Example Console Template Output:**
```
my_cli/
├── src/
│   ├── main.poh       # Menu-driven CLI with natural language
│   └── commands/      # Command handlers
├── tests/             # Test suite
├── examples/          # Usage examples
├── docs/              # Documentation
├── .vscode/           # VS Code integration
└── plhub.json         # Project configuration
```

## ⚡ Automation & Development Workflow

PLHub provides comprehensive automation for a smooth development experience.

### Watch Mode & Hot Reload

**Watch Mode** - Automatically rebuild on file changes:
```bash
python plhub.py watch
```

**Hot Reload** - Instant feedback with automatic restarts:
```bash
python plhub.py dev

# Custom entry file
python plhub.py dev --file examples/demo.poh
```

Features:
- 🔄 Automatic rebuilds on file changes
- 🚀 Instant process restart
- 📊 Incremental builds (only changed files)
- 🔗 Dependency detection
- ⏱️ Debouncing to prevent rapid reloads

### Test Automation

**Run tests**:
```bash
python plhub.py test
```

**Watch mode for tests** - Auto re-run on changes:
```bash
python plhub.py test --watch
```

**Filter specific tests**:
```bash
python plhub.py test --filter arithmetic
```

**CI/CD integration**:
```bash
# Generate GitHub Actions report
python plhub.py test --ci --ci-format github

# Generate JUnit XML (Jenkins, GitLab CI)
python plhub.py test --ci --ci-format junit --ci-output results.xml
```

### Debugging

Start debug session with breakpoint support:
```bash
python plhub.py debug
python plhub.py debug --file src/main.poh
```

### VS Code Integration

All projects automatically include VS Code configurations:

- **Tasks** (`.vscode/tasks.json`) - Run, Build, Test, Watch commands
- **Launch configs** (`.vscode/launch.json`) - Debug configurations
- **Problem matchers** - Parse errors and show in Problems panel

Use `Ctrl+Shift+B` to build or `F5` to debug!

### Complete Development Workflow

```bash
# Terminal 1: Hot reload
python plhub.py dev

# Terminal 2: Watch tests
python plhub.py test --watch

# Edit your code - changes auto-reload, tests auto-run! ✨
```

📚 **See [AUTOMATION_GUIDE.md](docs/AUTOMATION_GUIDE.md) for complete documentation**

## 🎨 UI Toolkit

PLHub includes a built-in UI toolkit for styling and widget management.

### Themes & Styling

```bash
# List available themes
python plhub.py style list

# Apply a theme to your project
python plhub.py style apply midnight_dark

# View theme details
python plhub.py style show default_light

# Create a custom theme based on an existing one
python plhub.py style create "My Theme" --base default_light --activate
```

**Built-in Themes:**
- `default_light` – Baseline light theme optimized for readability
- `midnight_dark` – High-contrast dark theme inspired by modern developer tooling

**Theme Structure:**
```
ui/styles/
├── active_style.json          # Points to the current theme
├── themes/
│   └── default_light.json     # Editable theme copy
└── README.md                  # Styling guide
```

### Widgets

```bash
# List widget templates
python plhub.py widget list

# Preview a widget before generating
python plhub.py widget preview card

# Generate a widget in your project
python plhub.py widget generate button --name PrimaryButton

# Dry-run to see what would be created
python plhub.py widget generate stack --name LayoutDemo --dry-run
```

**Built-in Widget Templates:**
- `button` – Simple button display with customizable label (uses only Set and Write)
- `card` – Framed content block with title and body (natural language only)
- `stack` – Vertical layout showing items in a list (using Repeat times)

**Design Philosophy:**  
Widgets are **standalone PohLang programs** using only **natural language statements**: `Set`, `Write`, `If/Otherwise`, `Repeat times`, and natural operators (`plus`, `minus`, etc.). No complex function parameters, no brackets, no symbols—just simple, readable code!

**Widget Structure:**
```
ui/widgets/
├── primary_button.poh         # Generated widget (standalone program)
├── welcome_card.poh           # Sample widget (created during project scaffolding)
├── templates/                 # Project-specific templates (optional)
└── README.md                  # Widget usage guide
```

**Example Widget** (`ui/widgets/welcome_card.poh`):
```poh
Start Program

# Welcome Card - Card Widget
# Displays content in a framed box

Set card_title to "Welcome"
Set card_body to "Thanks for using PohLang!"

Write "========================"
Write card_title
Write "------------------------"
Write card_body
Write "========================"

End Program
```

To use a widget pattern in your main program, simply copy the relevant code and customize the variable values!

## � Code Standards

All PohLang files must be wrapped in `Start Program` / `End Program`:

```poh
Start Program

# Your code here
Write "Hello, World!"

# Comments supported with # or //
Set x to 42
Write "The answer is " plus x

End Program
```

## 🧪 Testing

```bash
# Run all tests in tests/ directory
python plhub.py test

# Filter specific tests
python plhub.py test --filter unit_tests

# Verbose output
python plhub.py test --verbose
```

## 🧹 Maintenance

```bash
# Clean build artifacts and bytecode
python plhub.py clean

# Also remove dependencies (when package manager is active)
python plhub.py clean --all

# Check environment health
python plhub.py doctor

# Detailed diagnostics
python plhub.py doctor --verbose
```

## 🤝 Contributing

PL-Hub welcomes contributions:

- **Tools**: Add new development tools
- **Templates**: Create project templates in `templates/`
- **Runtime Integration**: Improve runtime detection and management
- **Commands**: Add new CLI commands (see `plhub.py`)
- **Documentation**: Improve guides in this README and documentation files
- **Testing**: Add tests in `Tests/`

See `PLHUB_DEVELOPER_GUIDE.md` for detailed contribution guidelines.

## 📖 Documentation

- **[Developer Guide](PLHUB_DEVELOPER_GUIDE.md)** - Comprehensive guide to PLHub
- **[Quick Reference](PLHUB_QUICK_REFERENCE.md)** - Command cheat sheet
- [Getting Started](docs/getting_started.md) - First steps with PLHub
- [CLI Reference](docs/cli_reference.md) - Detailed command documentation
- [Development Workflow](docs/development_workflow.md) - Best practices

### PohLang Documentation

- [PohLang Guide](../PohLang/PohLang_Guide.md) - Language tutorial
- [Runtime Design](../PohLang/runtime/DESIGN.md) - Runtime architecture
- [Grammar Spec](../PohLang/spec/Grammar.md) - Language grammar
- [Vocabulary](../PohLang/spec/Vocabulary.md) - Keyword reference

## 🌟 Status & Roadmap

**PLHub v0.5.0** - Current Release

### ✅ Completed
- Rust runtime integration with automatic detection
- `doctor` command for environment health checks
- `init`, `test`, `clean` commands
- Enhanced project scaffolding with proper templates
- `sync-runtime-local` with metadata tracking
- Support for # and // comments in parser
- UI toolkit with style themes and widget templates
- Comprehensive documentation

### 🚧 In Progress
- Package registry and dependency resolution
- VS Code extension integration
- Language server protocol support

### 📋 Planned
- Live theme preview in editors
- Hot reload during development
- Interactive REPL
- Web-based playground
- Deployment tools for various platforms
- Performance profiling tools

## � Troubleshooting

### Runtime Not Found

```bash
$ python plhub.py run main.poh
Error: PohLang Rust runtime not found

# Solution:
$ python plhub.py sync-runtime-local
# Or
$ python plhub.py update-runtime --version latest
```

### Build Errors

```bash
# Clean and rebuild
python plhub.py clean --all
cd ../PohLang/runtime
cargo build
cd ../../PLHub
python plhub.py sync-runtime-local
```

### Environment Issues

```bash
# Run diagnostics
python plhub.py doctor --verbose

# Check what it reports and follow suggestions
```

## 📜 License

PL-Hub is open source. See LICENSE file for details.

## 🙏 Acknowledgments

PL-Hub is inspired by modern development ecosystems like Flutter, Cargo, and npm, adapted for the natural-language philosophy of PohLang.

**PL-Hub is under active development. Contributions, feedback, and bug reports are welcome!**

---

For more information, visit:
- 📚 [Developer Guide](PLHUB_DEVELOPER_GUIDE.md)
- ⚡ [Quick Reference](PLHUB_QUICK_REFERENCE.md)
- 🌐 [PohLang Repository](https://github.com/AlhaqGH/PohLang)
