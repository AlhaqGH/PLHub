# PLHub Automation Guide

**Automated Development Workflow for PohLang Projects**

PLHub provides comprehensive automation for building, testing, debugging, and hot reloading your PohLang applications.

## Table of Contents

- [Build Automation](#build-automation)
- [Test Automation](#test-automation)
- [Hot Reload](#hot-reload)
- [Debugging](#debugging)
- [VS Code Integration](#vs-code-integration)
- [CI/CD Integration](#cicd-integration)

---

## Build Automation

### Watch Mode

Automatically rebuild your project when files change:

```bash
python plhub.py watch
```

Features:
- **Incremental builds**: Only rebuilds changed files and their dependencies
- **Build caching**: Tracks file hashes to avoid unnecessary rebuilds
- **Dependency detection**: Automatically detects `Import` statements
- **File watching**: Uses `watchdog` library for efficient file monitoring
- **Debouncing**: Prevents multiple rebuilds from rapid file changes

**Output**:
```
👀 Watching for changes in C:\Users\habib\POHLANG\my_project
Press Ctrl+C to stop

📝 Changes detected: 2 file(s)
[10:30:45] Building src\main.poh...
[10:30:45] Building src\utils.poh...
✅ Build successful: 2 file(s) compiled
   Compiled main.poh -> main.pbc
   Compiled utils.poh -> utils.pbc

👀 Watching for changes...
```

### Manual Build

Build all project files:

```bash
python plhub.py build
```

Options:
- `--target bytecode` - Compile to bytecode (.pbc files)
- `--out <dir>` - Specify output directory
- `--force` - Force rebuild all files

### How It Works

The build system:

1. **Scans** all `.poh` files in your project
2. **Computes** file hashes to detect changes
3. **Parses** `Import` statements to build dependency graph
4. **Determines** which files need rebuilding
5. **Compiles** changed files and their dependents
6. **Caches** results in `.plhub/cache/build_cache.json`

---

## Test Automation

### Running Tests

Run all tests in your `tests/` directory:

```bash
python plhub.py test
```

### Watch Mode for Tests

Automatically re-run tests when code changes:

```bash
python plhub.py test --watch
```

Features:
- Watches both `src/` and `tests/` directories
- Re-runs only relevant tests
- Color-coded output (✅ passed, ❌ failed)
- Summary statistics
- Test timing information

**Output**:
```
🧪 Running 5 test(s)...

✅ test_arithmetic (0.12s)
✅ test_collections (0.08s)
❌ test_advanced (0.15s)
✅ test_functions (0.10s)
✅ test_control_flow (0.09s)

============================================================
TEST SUMMARY
============================================================
Total:    5
Passed:   4 ✅
Failed:   1 ❌
Duration: 0.54s
Success:  80.0%
============================================================

Failed tests:
  ❌ test_advanced
     Error: Variable 'x' not defined

👀 Watching for changes...
```

### Filtering Tests

Run only specific tests:

```bash
python plhub.py test --filter arithmetic
python plhub.py test --filter "test_math|test_logic"
```

### Verbose Output

See detailed test output:

```bash
python plhub.py test --verbose
```

### Test Discovery

Tests are automatically discovered using these rules:

1. Must be in `tests/` directory
2. Must have `.poh` extension  
3. Must have "test" in the filename

Example test structure:
```
tests/
├── test_arithmetic.poh
├── test_collections.poh
├── unit/
│   ├── test_math.poh
│   └── test_strings.poh
└── integration/
    └── test_full_workflow.poh
```

### CI/CD Integration

Generate reports for continuous integration:

```bash
# GitHub Actions format
python plhub.py test --ci --ci-format github --ci-output test-report.md

# JUnit XML format (for Jenkins, GitLab CI, etc.)
python plhub.py test --ci --ci-format junit --ci-output test-results.xml
```

**GitHub Actions Example**:
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
      - name: Run tests
        run: python plhub.py test --ci --ci-format github --ci-output test-report.md
      - name: Upload results
        uses: actions/upload-artifact@v2
        with:
          name: test-results
          path: test-report.md
```

---

## Hot Reload

Development server with automatic reloading on file changes:

```bash
python plhub.py dev
```

### Custom Entry File

Specify a different entry point:

```bash
python plhub.py dev --file examples/demo.poh
```

### How It Works

1. **Starts** your application
2. **Watches** `src/`, `ui/`, and entry file directories
3. **Detects** changes to `.poh` files
4. **Stops** current process gracefully
5. **Restarts** with updated code
6. **Preserves** state (when possible)

**Output**:
```
============================================================
🔥 PohLang Hot Reload Server
============================================================
Project: my_app
Entry:   main.poh
Reloads: 0
============================================================

Press Ctrl+C to stop

🚀 Starting main.poh...

Hello from PohLang!
Running application...

📝 src\utils.poh changed
⏹️  Stopping process...
🔄 Reloading... (#1)
🚀 Starting main.poh...
✅ Reload complete

Hello from PohLang! (updated)
Running application...
```

### State Preservation

The hot reload system can save/restore state between reloads:

- Saved to `.plhub/hotreload_state.json`
- Automatic on graceful shutdown
- Restored on restart

### Debouncing

Changes are debounced (500ms delay) to avoid multiple reloads from rapid file saves.

---

## Debugging

### Start Debug Session

```bash
python plhub.py debug
python plhub.py debug --file src/main.poh
```

### Debug Features

**Breakpoints** (Planned):
```
break src/main.poh:10    # Set breakpoint at line 10
clear src/main.poh:10    # Clear breakpoint
list                      # List all breakpoints
```

**Execution Control** (Planned):
```
run        # Run/continue
step       # Step to next line
next       # Step over function calls
stop       # Stop execution
quit       # Exit debugger
```

**Inspection** (Planned):
```
print <var>      # Print variable value
locals           # Show local variables
stack            # Show call stack
```

**Note**: Full debugger implementation requires PohLang runtime support. Current version provides basic debugging infrastructure.

### Debug Server

The debug server runs on port 5858 by default:

```bash
python plhub.py debug --port 5858
```

---

## VS Code Integration

PLHub automatically creates VS Code configuration files when you create a new project.

### Tasks (`.vscode/tasks.json`)

Available tasks:

1. **PohLang: Run Program** - Run current file
2. **PohLang: Build Project** - Build entire project (default build task)
3. **PohLang: Watch Mode** - Watch and rebuild automatically
4. **PohLang: Run Tests** - Run all tests (default test task)
5. **PohLang: Watch Tests** - Watch and re-run tests
6. **PohLang: Start Dev Server** - Hot reload development server
7. **PohLang: Clean Build** - Clean build artifacts

### Launch Configurations (`.vscode/launch.json`)

Available launch configurations:

1. **PohLang: Run Current File** - Run the currently open file
2. **PohLang: Run Main** - Run src/main.poh
3. **PohLang: Debug Current File** - Debug currently open file
4. **PohLang: Debug Main** - Debug src/main.poh
5. **PohLang: Start Dev Server with Hot Reload** - Launch hot reload server

### Using VS Code Tasks

**Keyboard Shortcuts**:
- `Ctrl+Shift+B` (Windows/Linux) or `Cmd+Shift+B` (Mac) - Run default build task
- `Ctrl+Shift+T` then `T` - Run default test task

**Command Palette**:
1. Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac)
2. Type "Tasks: Run Task"
3. Select your task

### Problem Matchers

Tasks include problem matchers that:
- Parse build/test output
- Display errors in Problems panel
- Enable clicking to jump to error location

---

## CI/CD Integration

### GitHub Actions

Complete workflow example:

```yaml
name: PohLang CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install watchdog
      
      - name: Build project
        run: |
          python plhub.py build
      
      - name: Run tests
        run: |
          python plhub.py test --ci --ci-format github --ci-output test-report.md
      
      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: test-results
          path: test-report.md
      
      - name: Comment test results
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const report = fs.readFileSync('test-report.md', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: report
            });
```

### GitLab CI

```yaml
stages:
  - build
  - test

build:
  stage: build
  script:
    - python plhub.py build
  artifacts:
    paths:
      - build/

test:
  stage: test
  script:
    - python plhub.py test --ci --ci-format junit --ci-output test-results.xml
  artifacts:
    when: always
    reports:
      junit: test-results.xml
```

### Jenkins Pipeline

```groovy
pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                sh 'python plhub.py build'
            }
        }
        
        stage('Test') {
            steps {
                sh 'python plhub.py test --ci --ci-format junit --ci-output test-results.xml'
            }
            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }
    }
}
```

---

## Best Practices

### Development Workflow

1. **Start with hot reload**:
   ```bash
   python plhub.py dev
   ```

2. **Run tests in watch mode** (in another terminal):
   ```bash
   python plhub.py test --watch
   ```

3. **Edit your code** - Changes auto-reload and tests auto-run

4. **Debug when needed**:
   ```bash
   python plhub.py debug
   ```

### Project Structure

Recommended structure for automation:

```
my_project/
├── src/
│   ├── main.poh           # Entry point
│   ├── utils.poh          # Utilities
│   └── lib.poh            # Libraries
├── tests/
│   ├── test_main.poh      # Main tests
│   ├── test_utils.poh     # Utility tests
│   └── integration/
│       └── test_full.poh  # Integration tests
├── ui/
│   ├── widgets/           # UI widgets
│   └── styles/            # Themes
├── .vscode/
│   ├── tasks.json         # VS Code tasks
│   └── launch.json        # Debug configurations
├── .plhub/
│   ├── cache/             # Build cache
│   └── test-results/      # Test results
└── plhub.json             # Project configuration
```

### Performance Tips

1. **Use watch mode** instead of manual rebuilds
2. **Filter tests** during development: `--filter mytest`
3. **Use incremental builds** (automatic in watch mode)
4. **Install watchdog** for better file watching: `pip install watchdog`
5. **Clean occasionally**: `python plhub.py clean` to remove stale artifacts

### Troubleshooting

**Watch mode not detecting changes**:
- Install watchdog: `pip install watchdog`
- Check file permissions
- Verify files have `.poh` extension

**Tests not discovered**:
- Ensure files are in `tests/` directory
- Include "test" in filename
- Check file extension is `.poh`

**Hot reload loops**:
- Check for syntax errors in code
- Verify import paths are correct
- Look for circular dependencies

**Build cache issues**:
- Clean cache: `python plhub.py clean`
- Force rebuild: `python plhub.py build --force`

---

## Dependencies

Optional but recommended:

```bash
pip install watchdog    # For better file watching
```

All automation features work without external dependencies, but `watchdog` provides more efficient file monitoring than polling.

---

## Summary

PLHub automation provides:

✅ **Build Automation** - Watch mode, incremental builds, dependency detection  
✅ **Test Automation** - Auto-discovery, watch mode, CI/CD reports  
✅ **Hot Reload** - Instant feedback during development  
✅ **Debugging** - Breakpoint support and inspection (in progress)  
✅ **VS Code Integration** - Tasks and launch configurations  
✅ **CI/CD Ready** - GitHub Actions, GitLab CI, Jenkins support  

Happy coding! 🚀
