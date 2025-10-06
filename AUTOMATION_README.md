# PLHub Automation System

Complete automation for PLHub development, testing, and releases.

## 🚀 Quick Start

### Development Workflow

```bash
# 1. Make changes to PLHub
# Edit plhub.py, add features, fix bugs, etc.

# 2. Update SDK automatically
python tools/update_sdk.py --sync

# 3. Test changes
python plhub.py doctor
python plhub.py create test_project --template basic

# 4. Release new version
python tools/release_automation.py --bump patch --feature "Your Feature"
```

## 📋 Available Tools

### 1. Release Automation (`tools/release_automation.py`)

**Purpose**: Automate the entire release process from version bumping to PyPI publishing.

**Features**:
- ✅ Automatic version bumping (major/minor/patch)
- ✅ Update all version strings across files
- ✅ Generate changelog entries
- ✅ Create SDK package (zip)
- ✅ Git commit, tag, and push
- ✅ Build wheel and source distributions
- ✅ Publish to PyPI (or Test PyPI)
- ✅ Open GitHub release page

**Usage**:

```bash
# Bump patch version (0.5.1 → 0.5.2)
python tools/release_automation.py --bump patch

# Bump minor version with feature name
python tools/release_automation.py --bump minor --feature "New UI System"

# Specific version
python tools/release_automation.py --version 1.0.0 --feature "Stable Release"

# Dry run (preview changes)
python tools/release_automation.py --bump patch --dry-run

# Test on Test PyPI first
python tools/release_automation.py --bump patch --test-pypi

# Skip git operations
python tools/release_automation.py --version 0.5.1 --skip-git --publish-only

# Skip PyPI (just git and GitHub)
python tools/release_automation.py --bump patch --skip-pypi
```

**What it updates**:
- `setup.py` - version
- `plhub.py` - version string
- `plhub-sdk/setup.py` - version
- `plhub-sdk/plhub.py` - version string
- `CHANGELOG.md` - new version entry
- `plhub-sdk/CHANGELOG.md` - new version entry
- `RELEASE_NOTES.md` - release summary
- `plhub-sdk/RELEASE_PACKAGE.md` - package info

### 2. SDK Update Automation (`tools/update_sdk.py`)

**Purpose**: Keep SDK in sync with main PLHub after making changes.

**Features**:
- ✅ Verify sync status (show what's out of sync)
- ✅ Sync individual files or all files
- ✅ Sync directories (CLI, tools, templates, docs, Examples)
- ✅ Hash-based change detection
- ✅ Force overwrite option

**Usage**:

```bash
# Check sync status
python tools/update_sdk.py --verify

# Sync all files
python tools/update_sdk.py --sync

# Force sync (overwrite everything)
python tools/update_sdk.py --sync --force

# Sync specific files
python tools/update_sdk.py --sync --files plhub.py README.md

# Sync specific directory
python tools/update_sdk.py --sync --files tools

# Generate sync report
python tools/update_sdk.py --report
```

**What it syncs**:
- Files: `plhub.py`, `setup.py`, `README.md`, `CHANGELOG.md`, `LICENSE`, `requirements.txt`
- Directories: `CLI/`, `tools/`, `templates/`, `docs/`, `Examples/`

### 3. Build Automation (`tools/build_automation.py`)

**Purpose**: Automated build system with watch mode and incremental compilation.

**Features**:
- ✅ Watch mode (auto-rebuild on file changes)
- ✅ Incremental builds (only rebuild changed files)
- ✅ Dependency detection
- ✅ SHA256-based change tracking
- ✅ Build caching

**Usage**:

```bash
# Build project
python plhub.py build

# Build with watch mode
python plhub.py watch

# Build for release
python plhub.py build --release

# Build for debug
python plhub.py build --debug
```

### 4. Test Automation (`tools/test_runner.py`)

**Purpose**: Comprehensive test runner with watch mode and CI/CD integration.

**Features**:
- ✅ Auto-discover tests
- ✅ Watch mode (continuous testing)
- ✅ CI/CD report generation
- ✅ Test statistics
- ✅ Colored output

**Usage**:

```bash
# Run tests
python plhub.py test

# Watch mode
python plhub.py test --watch

# Generate CI/CD reports
python plhub.py test --ci
```

## 🔄 Complete Development Cycle

### 1. Feature Development

```bash
# Create feature branch
git checkout -b feature/new-ui

# Make changes
# Edit plhub.py, add new commands, etc.

# Update SDK
python tools/update_sdk.py --sync

# Test locally
python plhub.py doctor
python plhub.py test

# Commit changes
git add .
git commit -m "Add new UI system"
git push origin feature/new-ui
```

### 2. Release Process

```bash
# Merge to main
git checkout main
git merge feature/new-ui

# Automated release
python tools/release_automation.py --bump minor --feature "New UI System"

# This will:
# 1. ✅ Update version to 0.6.0
# 2. ✅ Update all files
# 3. ✅ Create SDK package
# 4. ✅ Git commit and tag
# 5. ✅ Push to GitHub
# 6. ✅ Build distributions
# 7. ✅ Publish to PyPI
# 8. ✅ Open GitHub release page

# Complete GitHub release
# 1. Review pre-filled information
# 2. Attach SDK zip
# 3. Click "Publish release"

# Verify
pip install --upgrade plhub
plhub --version
```

### 3. Hotfix Process

```bash
# Create hotfix branch
git checkout -b hotfix/critical-bug

# Fix bug
# Edit files

# Update SDK
python tools/update_sdk.py --sync

# Test
python plhub.py test

# Quick patch release
python tools/release_automation.py --bump patch --feature "Critical Bug Fix"
```

## 🎯 Best Practices

### Before Every Release

1. **Verify SDK Sync**
   ```bash
   python tools/update_sdk.py --verify
   ```

2. **Run Tests**
   ```bash
   python plhub.py test
   ```

3. **Test Installation**
   ```bash
   pip install -e .
   plhub doctor
   ```

4. **Review Changes**
   ```bash
   git diff
   git log --oneline -10
   ```

### Version Numbering

Follow [Semantic Versioning](https://semver.org/):

- **Major** (1.0.0): Breaking changes, major features
- **Minor** (0.6.0): New features, backward compatible
- **Patch** (0.5.2): Bug fixes, minor improvements

### Release Types

```bash
# Patch: Bug fixes
python tools/release_automation.py --bump patch

# Minor: New features
python tools/release_automation.py --bump minor --feature "Feature Name"

# Major: Breaking changes
python tools/release_automation.py --bump major --feature "Major Redesign"
```

## 🛠️ Manual Override

If you need manual control:

```bash
# Update version manually in setup.py and other files

# Just build and publish
python tools/release_automation.py --publish-only

# Or step by step:
python setup.py sdist bdist_wheel
python -m twine upload dist/*
```

## 🔍 Troubleshooting

### "twine not found"

```bash
pip install twine
```

### "Git push failed"

```bash
# Check remote
git remote -v

# Configure credentials
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# Retry manually
git push origin main
git push origin v0.5.1
```

### "PyPI upload failed"

```bash
# Use API token instead of password
# Create token at: https://pypi.org/manage/account/token/

# Configure in ~/.pypirc:
[pypi]
username = __token__
password = pypi-YOUR-TOKEN-HERE
```

### "SDK out of sync"

```bash
# Force sync everything
python tools/update_sdk.py --sync --force
```

## 📦 What Gets Published

### PyPI Package
- Python wheel (`.whl`)
- Source distribution (`.tar.gz`)
- Install with: `pip install plhub`

### SDK Package
- Zip file: `plhub-sdk-X.Y.Z.zip`
- SHA256 checksum
- Complete standalone SDK
- Attached to GitHub release

### GitHub Release
- Release notes from `RELEASE_NOTES.md`
- SDK zip attachment
- Git tag
- Changelog

## 🎓 Learning Resources

- **Development Workflow**: See `docs/development_workflow.md`
- **CLI Reference**: See `docs/cli_reference.md`
- **Getting Started**: See `docs/getting_started.md`
- **Release Checklist**: See `RELEASE_CHECKLIST.md`

## 🤝 Contributing

When adding new features:

1. Update main PLHub files
2. Run `python tools/update_sdk.py --sync`
3. Test thoroughly
4. Update documentation
5. Use release automation for versioning

## 📞 Support

- **Issues**: https://github.com/AlhaqGH/PLHub/issues
- **Discussions**: https://github.com/AlhaqGH/PLHub/discussions
- **Email**: contact@pohlang.org

---

**Automation makes releases easy, fast, and reliable!** 🚀
