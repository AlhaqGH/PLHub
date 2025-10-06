# PohLang + PL-Hub Development Workflow

This document describes the complete development workflow for the PohLang ecosystem, designed to mirror the Dart + Flutter model.

## Ecosystem Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    PohLang Ecosystem                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────┐    ┌─────────────────────────────────┐ │
│  │   PohLang SDK   │    │         PL-Hub SDK             │ │
│  │  (Core Language)│    │   (Development Environment)    │ │
│  │                 │    │                                 │ │
│  │ • Interpreter   │    │ • Embedded PohLang SDK          │ │
│  │ • Transpiler    │    │ • CLI Tools                     │ │
│  │ • Core Runtime  │    │ • Project Management           │ │
│  │ • Language Spec │    │ • Templates & Scaffolding      │ │
│  └─────────────────┘    │ • Package System                │ │
│                         │ • Build System                  │ │
│                         │ • Editor Integration            │ │
│                         └─────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────────────────────────┐
│   Dart SDK      │    │           Flutter SDK               │
│ (Core Language) │    │     (Development Framework)         │
│                 │    │                                     │
│ • Dart VM       │    │ • Embedded Dart SDK                 │
│ • Dart Compiler │    │ • Flutter CLI                       │
│ • Core Libraries│    │ • Widget Framework                  │
│ • Language Spec │    │ • Build System                      │
└─────────────────┘    │ • Development Tools                 │
                       │ • Platform Integration              │
                       └─────────────────────────────────────┘
```

## For End Users

### Installing PohLang (Language Only)
When you only need the PohLang language:

```bash
# Install PohLang SDK
pip install pohlang

# Use directly
pohlang script.poh

# Or in Python
python -c "
import pohlang
interpreter = pohlang.Interpreter()
interpreter.run('Write \"Hello from Python!\"')
"
```

**Use cases:**
- Embedding PohLang in Python applications
- Learning the language basics
- Server-side scripting
- Educational environments with existing tooling

### Installing PL-Hub (Complete Environment)
When you want the full development experience:

```bash
# Install PL-Hub SDK (includes PohLang automatically)
pip install plhub

# Create new projects
plhub create my-app --template console
cd my-app

# Full development workflow
plhub run src/main.poh
plhub transpile src/main.poh --to dart
plhub build --target dart
```

**Use cases:**
- Building complete applications
- Learning programming with guided templates
- Web development
- Cross-platform development (via Dart transpilation)
- Professional development with tooling

## For Developers

### Language Development (PohLang Repository)

**Repository:** `github.com/owner/PohLang`

**Structure:**
```
PohLang/
├── Interpreter/           # Python interpreter implementation
├── transpiler/           # Dart transpiler
├── bin/                  # CLI entrypoints
├── lib/                  # Dart runtime libraries
├── doc/                  # Language documentation
├── examples/             # Language examples
├── tests_python/         # Python interpreter tests
├── tests_dart/           # Dart transpiler tests
└── prepare_release.py    # Release automation
```

**Development workflow:**
```bash
# Setup
git clone https://github.com/owner/PohLang
cd PohLang
python -m pip install -e .

# Language development
# 1. Modify interpreter (Interpreter/)
# 2. Add tests (tests_python/)
# 3. Update documentation (doc/)
# 4. Test changes
python -m pytest tests_python/
python -m Interpreter.run_poh examples/hello.poh

# Transpiler development (requires Dart SDK)
cd transpiler
dart test
dart run bin/transpiler.dart ../examples/hello.poh

# Release language
python prepare_release.py
# Or push tag: git tag pohlang-v0.5.1 && git push origin pohlang-v0.5.1
```

### Environment Development (PL-Hub Repository)

**Repository:** `github.com/owner/PLHub`

**Structure:**
```
PLHub/
├── CLI/                  # Command-line interface
├── Editor/               # Editor integrations
├── Examples/             # Example projects
├── templates/            # Project templates
├── docs/                 # PL-Hub documentation
├── tools/                # Development tools
├── Tests/                # PL-Hub tests
├── Runtime/              # Embedded PohLang (auto-generated)
│   ├── Interpreter/      # From PohLang/Interpreter/
│   ├── transpiler/       # From PohLang/transpiler/
│   └── bin/              # From PohLang/bin/
└── plhub.py             # Main CLI entry point
```

**Development workflow:**
```bash
# Setup
git clone https://github.com/owner/PLHub
cd PLHub
python -m pip install -e .

# Environment development
# 1. Modify CLI (CLI/, plhub.py)
# 2. Add templates (templates/)
# 3. Update docs (docs/)
# 4. Add tests (Tests/)
python -m unittest discover -s Tests

# Integration testing (requires PohLang sibling repo)
python plhub.py release --pohlang-path ../PohLang --dry-run

# Release environment
python plhub.py release
# Or push tag: git tag plhub-v2.0.1 && git push origin plhub-v2.0.1
```

## Release Coordination

### 1. PohLang Release First
```bash
# In PohLang repo
cd PohLang
# Update version in Interpreter/__init__.py
# Update pyproject.toml
# Run tests, update docs
git commit -am "Release v0.5.1"
git tag pohlang-v0.5.1
git push origin pohlang-v0.5.1
```

### 2. PL-Hub Integration Release
```bash
# In PL-Hub repo (after PohLang release is live)
cd PLHub
# Update setup.py version
python plhub.py release --pohlang-ref pohlang-v0.5.1
git commit -am "Release v2.0.1 with PohLang v0.5.1"
git tag plhub-v2.0.1
git push origin plhub-v2.0.1
```

### 3. Automated Release (Preferred)
```bash
# PohLang (triggers GitHub Actions)
git tag pohlang-v0.5.1 && git push origin pohlang-v0.5.1

# Wait for PohLang release to complete, then PL-Hub
git tag plhub-v2.0.1 && git push origin plhub-v2.0.1
```

## Testing Strategy

### PohLang Testing (Language Correctness)
```bash
# Unit tests for interpreter
python -m pytest tests_python/test_interpreter.py

# Integration tests for language features
python -m pytest tests_python/test_integration.py

# Transpiler tests
cd transpiler && dart test

# Smoke tests
echo 'Write "Hello"' > test.poh
python -m Interpreter.run_poh test.poh
dart run bin/pohlang.dart test.poh --no-run
```

### PL-Hub Testing (Environment Integration)
```bash
# PL-Hub functionality tests
python -m unittest discover -s Tests

# CLI integration tests
python plhub.py --version
python plhub.py list templates
python plhub.py run Examples/hello_world.poh

# Project workflow tests
python plhub.py create test-project --template console
cd test-project
python ../plhub.py run src/main.poh
python ../plhub.py build --target dart
```

### Cross-Repository Testing
```bash
# Test PL-Hub with development PohLang
cd PLHub
python plhub.py release --pohlang-path ../PohLang --skip-tests --no-push
python -m unittest discover -s Tests
```

## Continuous Integration

### PohLang CI (Language Testing)
- **Trigger:** Push to main, PR, tag `pohlang-v*`
- **Jobs:**
  1. **Test Matrix:** Python 3.9-3.12
  2. **Interpreter Tests:** pytest on tests_python/
  3. **Transpiler Tests:** dart test (if Dart available)
  4. **Build:** Create wheel/sdist and Dart SDK bundle
  5. **Release:** Upload to PyPI and GitHub Releases

### PL-Hub CI (Environment Testing)  
- **Trigger:** Push to main, PR, tag `plhub-v*`
- **Jobs:**
  1. **Integration:** Download latest PohLang release
  2. **Test Matrix:** Python 3.9-3.12 with integrated PohLang
  3. **PL-Hub Tests:** unittest on Tests/
  4. **CLI Tests:** Smoke test all commands
  5. **Build:** Create Python package and SDK bundles
  6. **Release:** Upload to PyPI and GitHub Releases

## Version Compatibility

### Support Matrix
| PL-Hub Version | PohLang Version | Python | Dart | Status |
|----------------|-----------------|--------|------|--------|
| 2.0.x          | 0.5.x           | 3.9+   | 2.17+ | Current |
| 1.x.x          | 0.4.x           | 3.8+   | 2.15+ | Legacy |

### Compatibility Policy
- **PL-Hub** supports the latest stable PohLang by default
- **PL-Hub** may support N-1 PohLang for critical updates
- **Breaking changes** in PohLang trigger major PL-Hub version
- **Python compatibility** follows PohLang requirements

## Distribution Channels

### PyPI (Primary)
```bash
# Language only
pip install pohlang

# Complete environment
pip install plhub
```

### GitHub Releases (SDK Bundles)
- **PohLang SDK:** `pohlang-v*.tar.gz` (includes Dart transpiler)
- **PL-Hub SDK:** `plhub-sdk-v*.tar.gz` (standalone installer)

### Package Managers (Future)
- **Homebrew:** `brew install pohlang` / `brew install plhub`
- **Chocolatey:** `choco install pohlang` / `choco install plhub`
- **APT/YUM:** Distribution packages

## Migration from Other Languages

### From Python
```bash
# Install PL-Hub
pip install plhub

# Create Python-style project
plhub create my-script --template basic

# PohLang is more English-like
# Python: print("Hello")
# PohLang: Write "Hello"
```

### From Dart/Flutter
```bash
# Install PL-Hub (like Flutter)
pip install plhub

# Create project (like flutter create)
plhub create my-app --template console

# Build to Dart (performance)
plhub build --target dart

# PohLang transpiles to readable Dart
```

### From JavaScript/Node
```bash
# PL-Hub provides similar workflow
plhub create my-app
cd my-app
plhub run src/main.poh  # like node index.js
plhub build             # like npm build
```

## Best Practices

### For Language Contributors
1. **Test thoroughly:** Both Python and Dart paths
2. **Update docs:** Language changes need documentation
3. **Consider compatibility:** Breaking changes need major version
4. **Coordinate releases:** Inform PL-Hub maintainers

### For Environment Contributors  
1. **Test integration:** Always test with latest PohLang
2. **Maintain templates:** Keep examples working
3. **Document CLI changes:** Update reference docs
4. **Consider user impact:** Breaking CLI changes need major version

### For Release Managers
1. **Test releases:** Use staging/test environments
2. **Coordinate timing:** PohLang first, then PL-Hub
3. **Monitor feedback:** Watch for integration issues
4. **Maintain compatibility:** Support matrix and migration guides

## Troubleshooting

### "Command not found" after installation
```bash
# Check installation
pip show pohlang
pip show plhub

# Check PATH
which pohlang
which plhub

# Reinstall if needed
pip install --force-reinstall plhub
```

### Version mismatches
```bash
# Check versions
pohlang --version
plhub --version
cat ~/.local/lib/python*/site-packages/plhub/Runtime/pohlang_metadata.json

# Update to latest
pip install --upgrade plhub
```

### Development setup issues
```bash
# Reset development environment
cd PohLang && pip install -e .
cd PLHub && pip install -e .

# Test basic functionality
python -m Interpreter.run_poh examples/hello.poh
python plhub.py run Examples/hello_world.poh
```

This workflow ensures that PohLang and PL-Hub maintain the same professional relationship as Dart and Flutter, with clear separation of concerns and coordinated releases.