# PL-Hub SDK Release Playbook

This playbook covers the complete release process for the PL-Hub SDK (the development environment).

## Overview

PL-Hub SDK is the complete development environment that provides:
- Embedded PohLang interpreter and transpiler
- CLI tools for project management
- Templates and scaffolding
- Package management system
- Build system for multiple targets
- Editor integrations

Think: **PL-Hub SDK** is like **Flutter SDK** - the complete development environment.

## Release Dependencies

PL-Hub releases depend on PohLang SDK releases:
1. PohLang SDK is released first (core language)
2. PL-Hub SDK integrates the latest PohLang SDK
3. PL-Hub SDK is released with embedded PohLang

## Release Types

### Automatic Release (Recommended)
Triggered by GitHub Actions when you push a `plhub-v*` tag.

### Manual Release
For hotfixes or custom PohLang integration.

## Pre-Release Checklist

### 1. PohLang Integration
- [ ] Determine PohLang version to integrate (usually latest stable)
- [ ] Test PohLang SDK compatibility
- [ ] Update any PL-Hub code for PohLang API changes

### 2. Version Management
- [ ] Update `setup.py` with new PL-Hub version
- [ ] Update `plhub.py` version string
- [ ] Update `README.md` if needed

### 3. Testing
- [ ] Run PL-Hub test suite: `python -m unittest discover -s Tests`
- [ ] Test CLI commands:
   ```bash
   python plhub.py --version
   python plhub.py list templates
   python plhub.py run Examples/hello_world.poh
   python plhub.py transpile Examples/hello_world.poh --to dart
   ```
- [ ] Test project creation and building
- [ ] Test integration workflow manually

### 4. Documentation
- [ ] Update CLI reference docs
- [ ] Update README with new features
- [ ] Verify all examples work

## Release Process

### Option A: Automated Release (GitHub Actions)

1. **Trigger release workflow:**
   ```bash
   # Method 1: Push tag (uses latest PohLang)
   git tag plhub-v2.0.0
   git push origin plhub-v2.0.0
   
   # Method 2: Manual dispatch (specify PohLang version)
   # Go to GitHub Actions → PL-Hub SDK Release → Run workflow
   # Specify PL-Hub version and PohLang version
   ```

2. **Monitor workflow stages:**
   - **integrate-pohlang**: Downloads and integrates PohLang SDK
   - **test**: Runs tests with integrated PohLang
   - **build-sdk**: Creates distribution packages and SDK bundles
   - **release**: Publishes to GitHub and PyPI

3. **Verify release artifacts:**
   - Check GitHub Releases page
   - Test Python package: `pip install plhub==X.Y.Z`
   - Download and test SDK bundle
   - Verify PyPI publication

### Option B: Manual Release

1. **Integrate PohLang:**
   ```bash
   # Using local script
   python plhub.py release --pohlang-path ../PohLang --skip-tests --no-push
   
   # Or specify remote PohLang version
   python plhub.py release --pohlang-ref v0.5.0
   ```

2. **Test integration:**
   ```bash
   python -m unittest discover -s Tests -v
   python plhub.py run Examples/hello_world.poh
   ```

3. **Build distributions:**
   ```bash
   python -m build
   ```

4. **Create SDK bundle:**
   ```bash
   # This is automated by the release script
   # Creates plhub-sdk.tar.gz and plhub-sdk.zip
   ```

5. **Upload to PyPI:**
   ```bash
   python -m twine upload dist/*
   ```

6. **Create GitHub release:**
   - Tag: `plhub-vX.Y.Z`
   - Upload Python wheel/source
   - Upload SDK bundles
   - Include PohLang version in release notes

## Integration Workflow Details

The integration process copies these from PohLang to PL-Hub:

```
PohLang/Interpreter/     → PLHub/Runtime/Interpreter/
PohLang/transpiler/      → PLHub/Runtime/transpiler/
PohLang/bin/             → PLHub/Runtime/bin/
```

Plus creates metadata:
```json
{
  "pohlang_version": "0.5.0",
  "source_repo": "https://github.com/owner/PohLang",
  "source_tag": "pohlang-v0.5.0",
  "integrated_at": "2025-09-21T12:00:00Z",
  "integrated_by": "GitHub Actions"
}
```

## Post-Release Tasks

### 1. Verification
- [ ] Test PyPI installation: `pip install plhub==X.Y.Z`
- [ ] Test SDK bundle downloads and installation
- [ ] Verify all CLI commands work with new version
- [ ] Test project creation and building

### 2. Communication
- [ ] Update PL-Hub website/docs
- [ ] Announce new version with embedded PohLang version
- [ ] Update installation instructions
- [ ] Notify community about new features

### 3. Documentation Updates
- [ ] Update getting started guides
- [ ] Update CLI reference if commands changed
- [ ] Update examples if needed

## Version Numbering

PL-Hub uses semantic versioning independent of PohLang:
- **Major**: Breaking CLI changes, major architecture changes
- **Minor**: New features, new PohLang integration
- **Patch**: Bug fixes, PohLang hotfixes

Examples:
- `2.0.0` - Major PL-Hub architecture update
- `2.1.0` - New CLI commands, PohLang 0.6.0 integration
- `2.1.1` - Bug fixes, PohLang 0.6.1 integration

## Distribution Formats

PL-Hub is distributed in multiple formats:

### 1. Python Package (PyPI)
```bash
pip install plhub
```
- Includes embedded PohLang
- Requires Python 3.9+
- Best for Python developers

### 2. Standalone SDK Bundle
```bash
# Download plhub-sdk-X.Y.Z.tar.gz
tar -xzf plhub-sdk-X.Y.Z.tar.gz
cd plhub-sdk
./install.sh  # Linux/Mac
install.bat   # Windows
```
- Self-contained installation
- Includes Python dependencies
- Best for non-Python developers

## Troubleshooting

### Integration Failures
```bash
# Check PohLang availability
curl -s https://api.github.com/repos/owner/PohLang/releases/latest

# Manual integration test
python plhub.py release --pohlang-path ../PohLang --dry-run
```

### Test Failures After Integration
```bash
# Check integrated components
ls -la Runtime/Interpreter/
cat Runtime/pohlang_metadata.json

# Test specific integration
python -c "
import sys
sys.path.insert(0, 'Runtime')
from Interpreter.poh_interpreter import Interpreter
print('Integration OK')
"
```

### Build Failures
```bash
# Clean build
rm -rf build/ dist/ *.egg-info/

# Check packaging
python -m build
python -m twine check dist/*
```

### CLI Test Failures
```bash
# Test individual commands
python plhub.py --version
python plhub.py list examples
PYTHONPATH=. python -m CLI.cli run Examples/hello_world.poh
```

## Emergency Procedures

### Critical Bug in Integrated PohLang
1. **Quick hotfix release:**
   ```bash
   # Integrate fixed PohLang version
   python plhub.py release --pohlang-ref pohlang-v0.5.1
   # Release as patch version
   ```

2. **Yank problematic release from PyPI**
3. **Update SDK bundle downloads**

### Integration Corruption
1. **Reset Runtime directory:**
   ```bash
   rm -rf Runtime/Interpreter Runtime/transpiler Runtime/bin
   git checkout HEAD -- Runtime/
   ```

2. **Re-run integration:**
   ```bash
   python plhub.py release --pohlang-path ../PohLang
   ```

## Files Modified During Release

- `setup.py` - PL-Hub version
- `plhub.py` - Version string  
- `Runtime/Interpreter/` - Embedded PohLang interpreter
- `Runtime/transpiler/` - Embedded Dart transpiler
- `Runtime/bin/` - Embedded PohLang tools
- `Runtime/pohlang_metadata.json` - Integration metadata
- Git tags - `plhub-vX.Y.Z`

## Developer Workflow Comparison

| Task | Dart/Flutter | PohLang/PL-Hub |
|------|-------------|----------------|
| Install language | `dart-sdk` | `pip install pohlang` |
| Install environment | `flutter-sdk` | `pip install plhub` |
| Create project | `flutter create` | `plhub create` |
| Run project | `flutter run` | `plhub run` |
| Build project | `flutter build` | `plhub build` |
| Package manager | `pub` | `plhub install` |

## Contact

For release issues, contact:
- GitHub Issues: Create issue with `release` label
- Maintainers: See AUTHORS.md
- Discord: #plhub-releases channel