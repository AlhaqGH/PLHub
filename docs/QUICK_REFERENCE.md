# PL-Hub v0.5.0 - Quick Reference

**🎨 Now with Enhanced User-Friendly Commands!** ✨

> See `USER_FRIENDLY_COMMANDS.md` for detailed examples with progress bars, colored output, and interactive modes.

## 🚀 Installation & Setup

```bash
# Clone PLHub
git clone https://github.com/AlhaqGH/PLHub
cd PLHub

# Check environment
python plhub.py doctor

# Sync PohLang runtime (if developing locally)
python plhub.py sync-runtime-local
```

## 📦 Project Creation

```bash
# Basic starter project
python plhub.py create my_app --template basic

# Interactive console app
python plhub.py create my_cli --template console

# Reusable library
python plhub.py create my_lib --template library

# Web application (experimental)
python plhub.py create my_web --template web

# Skip UI scaffolding
python plhub.py create my_app --template basic --no-ui

# Custom theme
python plhub.py create my_app --ui-theme midnight_dark
```

## 🏃 Running Code

```bash
# Run a file
python plhub.py run src/main.poh

# Run with hot reload
python plhub.py dev

# Run in debug mode
python plhub.py debug
```

## 🔨 Building

```bash
# Build project
python plhub.py build

# Watch and rebuild automatically
python plhub.py watch

# Clean build artifacts
python plhub.py clean

# Build to specific target
python plhub.py build --target bytecode
python plhub.py build --target dart
```

## 🧪 Testing

```bash
# Run all tests
python plhub.py test

# Watch and re-run tests
python plhub.py test --watch

# Generate CI/CD reports
python plhub.py test --ci

# Run specific test
python plhub.py run tests/test_main.poh
```

## 🎨 UI Toolkit

```bash
# List available themes
python plhub.py style list

# Apply theme to project
python plhub.py style apply midnight_dark

# Create custom theme
python plhub.py style create my_theme

# List widget templates
python plhub.py widget list

# Generate widget from template
python plhub.py widget generate button MyButton
```

## 🔍 Environment Management

```bash
# Check environment health
python plhub.py doctor

# Verbose diagnostics
python plhub.py doctor --verbose

# Update runtime
python plhub.py update-runtime --version latest

# Sync local runtime build
python plhub.py sync-runtime-local --profile release
```

## 📚 Information & Examples

```bash
# List examples
python plhub.py list examples

# List templates
python plhub.py list templates

# Show version
python plhub.py --version

# Show help
python plhub.py --help
python plhub.py create --help
```

## 🎯 Template Structures

### Basic Template
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

### Console Template
```
my_cli/
├── src/
│   ├── main.poh       # Menu-driven interface
│   ├── commands/      # Command handlers
│   └── utils/         # Utilities
├── tests/             # Test suite
├── examples/          # CLI examples
├── docs/              # Documentation
├── .vscode/
├── plhub.json
└── README.md
```

### Library Template
```
my_lib/
├── src/
│   ├── lib.poh        # Library entry
│   ├── core/          # Core functions
│   └── utils/         # Utilities
├── tests/             # Test suite
├── examples/          # API examples
├── docs/
│   ├── api.md         # API documentation
│   └── README.md
├── .vscode/
└── plhub.json
```

## 📝 VS Code Tasks (Automatically Generated)

Press `Ctrl+Shift+B` in VS Code to see:

1. **Run Program** - Run current file
2. **Build Project** - Build entire project (default)
3. **Watch Mode** - Auto-rebuild on changes
4. **Run Tests** - Run all tests (default test task)
5. **Watch Tests** - Auto-run tests on changes
6. **Start Dev Server** - Hot reload server
7. **Clean Build** - Remove build artifacts

## 🐛 Debug Configurations (Automatically Generated)

Press `F5` in VS Code to start debugging with:

1. **Run Current File** - Execute current .poh file
2. **Debug Current File** - Debug current file
3. **Run Tests** - Execute test suite
4. **Debug Tests** - Debug test suite
5. **Attach to Dev Server** - Attach to running dev server

## 🔄 Automation Workflows

### Workflow 1: Development with Hot Reload
```bash
cd my_app
python plhub.py dev
# Edit files - see changes instantly!
# Ctrl+C to stop
```

### Workflow 2: Test-Driven Development
```bash
cd my_lib
python plhub.py test --watch
# Write test -> Edit code -> Test auto-runs
# Ctrl+C to stop
```

### Workflow 3: Continuous Building
```bash
cd my_project
python plhub.py watch
# Edit files - automatic incremental rebuild
# Ctrl+C to stop
```

### Workflow 4: CI/CD Integration
```bash
# Generate CI reports
python plhub.py test --ci

# Outputs:
# - .github/workflows/test.yml (GitHub Actions)
# - test-results.xml (JUnit format)
```

## 🛠 Troubleshooting

### Runtime Not Found
```bash
# Check environment
python plhub.py doctor --verbose

# Sync runtime
python plhub.py sync-runtime-local

# Or download official
python plhub.py update-runtime --version latest
```

### Build Issues
```bash
# Clean and rebuild
python plhub.py clean
python plhub.py build

# Check for errors
python plhub.py doctor
```

### Test Failures
```bash
# Run tests with verbose output
python plhub.py test --verbose

# Run specific test
python plhub.py run tests/test_name.poh
```

### Watch Mode Not Detecting Changes
```bash
# Install watchdog for better performance
pip install watchdog

# Or adjust debounce delay (in automation code)
```

## 📊 Performance Tips

1. **Use Watch Mode**: Incremental builds are 10-100x faster
2. **Install Watchdog**: `pip install watchdog` for efficient file watching
3. **Incremental Compilation**: Only changed files are rebuilt
4. **Dependency Caching**: Unchanged dependencies are skipped
5. **Hot Reload**: Instant feedback without full restarts

## 🔗 Key Files

| File | Purpose |
|------|---------|
| `plhub.json` | Project configuration |
| `.vscode/tasks.json` | VS Code build tasks |
| `.vscode/launch.json` | Debug configurations |
| `.gitignore` | Version control exclusions |
| `README.md` | Project documentation |
| `USAGE.md` | Usage instructions (console/library templates) |

## 📚 Documentation

- **[README.md](../README.md)** - Main documentation
- **[AUTOMATION_GUIDE.md](AUTOMATION_GUIDE.md)** - Complete automation guide (88KB)
- **[RELEASE_v0.5.0.md](RELEASE_v0.5.0.md)** - Release summary
- **[CHANGELOG.md](../CHANGELOG.md)** - Detailed release notes

## 💡 Tips & Tricks

1. **Quick Start**: Use `--template console` for interactive apps
2. **Hot Reload**: `python plhub.py dev` gives instant feedback
3. **Test Watch**: `python plhub.py test --watch` for TDD workflow
4. **VS Code**: Open folder and press `Ctrl+Shift+B` for tasks
5. **No UI**: Use `--no-ui` to skip UI scaffolding
6. **Custom Themes**: Create themes with `python plhub.py style create`
7. **CI Integration**: Use `--ci` flag to generate workflow files

## 🎓 Learning Resources

### Examples Directory
```bash
# Browse examples
ls PLHub/Examples/

# Run an example
python plhub.py run Examples/hello_world.poh
```

### Template Examples
Each template includes:
- Complete working code
- Test examples
- Usage documentation
- Best practices

### Online Resources
- PohLang Language Guide: `PohLang/PohLang_Guide.md`
- Vocabulary Reference: `PohLang/spec/Vocabulary.md`
- Grammar Specification: `PohLang/spec/Grammar.md`

## 🚀 Next Steps

1. **Create Your First Project**
   ```bash
   python plhub.py create my_first_app --template basic
   cd my_first_app
   ```

2. **Start Development**
   ```bash
   python plhub.py dev
   ```

3. **Open in VS Code**
   ```bash
   code .
   ```

4. **Start Coding!**
   - Edit `src/main.poh`
   - See changes instantly with hot reload
   - Run tests with `Ctrl+Shift+T`
   - Debug with `F5`

---

**Version**: 0.5.0  
**Last Updated**: January 2025  
**License**: MIT
