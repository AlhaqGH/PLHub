# PL-Hub

**PL-Hub (PohLang Hub) is the official development environment for the PohLang programming language.**

While **PohLang** is the core language (interpreter, transpiler, and language specifications), **PL-Hub** provides the complete development ecosystem around it: tooling, project management, package system, editor integration, and deployment tools.

Think of it this way:
- **PohLang** is like **Dart** (the language)
- **PL-Hub** is like **Flutter** (the development framework and tools)

## ✨ What is PL-Hub?

PL-Hub is the comprehensive development platform for PohLang that provides:

🔹 **Project Management** – create, build, and manage PohLang projects  
🔹 **Package System** – install and manage PohLang packages and dependencies  
🔹 **Development Tools** – CLI tools for running, building, and testing  
🔹 **Editor Integration** – syntax highlighting, autocomplete, and language server  
🔹 **Templates & Scaffolding** – quick-start templates for different project types  
🔹 **Build System** – compile to Dart, Python, or other targets  
🔹 **Testing Framework** – automated testing tools and runners  
🔹 **Documentation Tools** – generate docs and guides  

## 🚀 Quick Start

### Installation

```bash
# Install PohLang (the core language)
pip install pohlang

# Clone PLHub (the development environment)
git clone https://github.com/yourname/PLHub
cd PLHub
```

### Create Your First Project

```bash
# Create a new project
python plhub.py create my_app

# Navigate to project
cd my_app

# Run the project
python plhub.py run src/main.poh
```

### Available Commands

```bash
# Run a PohLang program
python plhub.py run <file.poh>

# Transpile a program
python plhub.py transpile <file.poh> --to dart

# Create new project
python plhub.py create <project_name> [--template basic|console|web]

# Install packages
python plhub.py install <package_name>

# Build project
python plhub.py build [--target dart|python]

# List examples, templates, or packages
python plhub.py list [examples|templates|packages]
```

## 📂 Project Structure

```
PLHub/                          # Development Environment
│
├─ CLI/                        # Command-line interface tools
├─ Editor/                     # Editor integrations & language server
├─ Examples/                   # Example projects and tutorials
├─ Modules/                    # Shared modules and libraries
├─ packages/                   # Package registry (local)
├─ plugins/                    # PLHub plugins and extensions
├─ templates/                  # Project templates
├─ tools/                      # Development and build tools
├─ Tests/                      # PLHub environment tests
├─ docs/                       # PLHub documentation and guides
├─ plhub.py                    # Main PLHub entry point
├─ setup.py                    # PLHub installation script
└─ README.md                   # This file

PohLang/                       # Core Language (separate project)
├─ Interpreter/                # Python interpreter implementation
├─ transpiler/                 # Dart transpiler
├─ lib/                        # Dart runtime library
├─ bin/                        # Language CLI tools
├─ doc/                        # Language documentation
├─ examples/                   # Language examples
└─ tests_python/               # Language tests
```

## 🛠 Development Workflow

### 1. Create Project
```bash
python plhub.py create calculator --template console
cd calculator
```

### 2. Develop
Edit `src/main.poh`:
```pohLang
Write "Simple Calculator"
Ask for first_number
Ask for second_number
Set result to first_number plus second_number
Write "Result: " plus result
```

### 3. Run & Test
```bash
python plhub.py run src/main.poh
```

### 4. Build
```bash
# Build to Dart (for performance)
python plhub.py build --target dart

# Or keep as Python (for development)
python plhub.py build --target python
```

## 📦 Package Management

### Project Configuration (`plhub.json`)
```json
{
  "name": "my_project",
  "version": "1.0.0",
  "description": "My PohLang project",
  "main": "src/main.poh",
  "dependencies": {
    "math_utils": "^1.0.0",
    "web_framework": "^2.1.0"
  },
  "dev_dependencies": {
    "test_framework": "^1.0.0"
  }
}
```

### Installing Packages
```bash
# Install a package
python plhub.py install math_utils

# List installed packages
python plhub.py list packages
```

## 🎯 Templates

Available project templates:

- **basic**: Simple console application
- **console**: Advanced console app with I/O
- **web**: Web application (experimental)

Create with template:
```bash
python plhub.py create my_web_app --template web
```

## 🔧 Integration with PohLang

PL-Hub automatically detects and uses your PohLang installation:

1. **Local Development**: If PLHub is next to PohLang directory
2. **System Installation**: If PohLang is installed via pip
3. **Manual Path**: Set POHLANG_PATH environment variable

## 🤝 Contributing

PL-Hub welcomes contributions:

- **Tools**: Add new development tools in `tools/`
- **Templates**: Create project templates in `templates/`
- **Editor Support**: Improve editor integrations in `Editor/`
- **Packages**: Contribute packages to the ecosystem
- **Documentation**: Improve guides in `docs/`

## 📖 Documentation

- [Getting Started Guide](docs/getting_started.md)
- [Project Structure](docs/project_structure.md)
- [Package Development](docs/package_development.md)
- [Editor Setup](docs/editor_setup.md)
- [Build System](docs/build_system.md)

## 🌟 Status

PL-Hub v2.0.0 - Major architecture update:
- ✅ Proper separation from PohLang core
- ✅ Project management system
- ✅ Package system foundation
- ✅ Build system integration
- 🚧 Package registry (coming soon)
- 🚧 Editor language server (in progress)
- 🚧 Web deployment tools (planned)

**PL-Hub is under active development. Contributions and feedback welcome!**

## 🚀 Release Automation

PL-Hub includes a one-command release workflow that integrates the latest PohLang interpreter, runs tests, builds artifacts, and tags the release.

Quick start:

```bash
plhub release
```

What it does:
- Copies `PohLang/Interpreter/` into `PLHub/Runtime/Interpreter/`
- Copies `PohLang/transpiler/` and `PohLang/bin/` into `PLHub/Runtime/` (for Dart transpiler)
- Writes `PLHub/Runtime/pohlang_metadata.json` with version/commit and timestamp
- Runs PL-Hub tests (pytest or unittest)
- Builds sdist and wheel into `dist/`
- Creates a git tag like `plhub-v<PLHub version>` and optionally pushes

Options:
- `--pohlang-path`: path to PohLang repo (defaults to `../PohLang`)
- `--skip-tests`: do not run tests
- `--no-push`: skip pushing commits/tags
- `--tag`: override tag name
