# PLHub CLI Reference

Complete reference for all PLHub command-line tools.

## Main Commands

### `plhub create`
Create a new PohLang project.

```bash
plhub create <project_name> [OPTIONS]
```

**Options:**
- `--template <name>`: Project template (basic, console, web)
- `--force`: Overwrite existing directory

**Examples:**
```bash
plhub create my_app
plhub create calculator --template console
plhub create website --template web
```

### `plhub run`
Run a PohLang program.

```bash
plhub run <file.poh> [OPTIONS]
```

**Options:**
- `--debug`: Enable debug output
- `--verbose`: Enable verbose output

**Examples:**
```bash
plhub run src/main.poh
plhub run Examples/hello_world.poh --verbose
plhub run test.poh --debug
```

### `plhub build`
Build the current project.

```bash
plhub build [OPTIONS]
```

**Options:**
- `--target <platform>`: Build target (dart, python)
- `--output <dir>`: Output directory
- `--release`: Build in release mode

**Examples:**
```bash
plhub build
plhub build --target dart
plhub build --target python --release
```

### `plhub install`
Install a package.

```bash
plhub install <package_name> [OPTIONS]
```

**Options:**
- `--save-dev`: Install as development dependency
- `--global`: Install globally
- `--version <ver>`: Specific version

**Examples:**
```bash
plhub install math_utils
plhub install test_framework --save-dev
plhub install web_framework --version 2.1.0
```

### `plhub list`
List available items.

```bash
plhub list <type>
```

**Types:**
- `examples`: Available example programs
- `templates`: Project templates
- `packages`: Installed packages

**Examples:**
```bash
plhub list examples
plhub list templates
plhub list packages
```

### `plhub transpile`
Transpile a PohLang file to another target language.

```bash
plhub transpile <file.poh> [OPTIONS]
```

**Options:**
- `--to <target>`: Target language (currently only `dart`)
- `--out-dir <dir>`: Output directory (default: `build`)

**Examples:**
```bash
plhub transpile src/main.poh --to dart
plhub transpile script.poh --to dart --out-dir generated
```

### `plhub release`
Run automated release process (for maintainers).

```bash
plhub release [OPTIONS]
```

**Options:**
- `--dry-run`: Run integration and tests without building or tagging
- `--no-push`: Do not push git tags/commits
- `--tag <name>`: Override git tag name
- `--pohlang-path <path>`: Path to PohLang repo (default: `../PohLang`)
- `--skip-tests`: Skip running PL-Hub tests
- `--pohlang-ref <ref>`: Git ref to checkout (default: `latest-tag`)

**Examples:**
```bash
plhub release --dry-run
plhub release --pohlang-ref main --no-push
plhub release --tag plhub-v2.1.0
```

### `plhub init`
Initialize a new project in current directory.

```bash
plhub init [OPTIONS]
```

**Options:**
- `--template <name>`: Template to use
- `--name <name>`: Project name

### `plhub test`
Run project tests.

```bash
plhub test [OPTIONS]
```

**Options:**
- `--verbose`: Verbose test output
- `--pattern <glob>`: Test file pattern

### `plhub clean`
Clean build artifacts.

```bash
plhub clean [OPTIONS]
```

**Options:**
- `--all`: Clean everything including dependencies

### `plhub info`
Show project information.

```bash
plhub info [OPTIONS]
```

**Options:**
- `--json`: Output as JSON

### `plhub update`
Update packages.

```bash
plhub update [package_name]
```

### `plhub publish`
Publish package to registry.

```bash
plhub publish [OPTIONS]
```

**Options:**
- `--registry <url>`: Custom registry URL
- `--dry-run`: Show what would be published

## Global Options

All commands support these global options:

- `--help, -h`: Show help
- `--version, -v`: Show version
- `--config <file>`: Use custom config file
- `--verbose`: Enable verbose output
- `--quiet`: Suppress output

## Configuration

PLHub can be configured via:

1. **Project config**: `plhub.json` in project root
2. **Global config**: `~/.plhub/config.json`
3. **Environment variables**: `PLHUB_*` variables

### Project Configuration (`plhub.json`)
```json
{
  "name": "my_project",
  "version": "1.0.0",
  "description": "My PohLang project",
  "main": "src/main.poh",
  "scripts": {
    "start": "plhub run src/main.poh",
    "build": "plhub build --target dart",
    "test": "plhub test"
  },
  "dependencies": {},
  "dev_dependencies": {}
}
```

### Global Configuration (`~/.plhub/config.json`)
```json
{
  "default_template": "console",
  "auto_install_deps": true,
  "registry_url": "https://packages.plhub.org",
  "editor": "code",
  "build_target": "dart"
}
```

## Environment Variables

- `PLHUB_HOME`: PLHub installation directory
- `PLHUB_CACHE`: Cache directory
- `PLHUB_REGISTRY`: Package registry URL
- `POHLANG_PATH`: PohLang installation path

## Exit Codes

- `0`: Success
- `1`: General error
- `2`: Command not found
- `64`: Usage error
- `70`: Internal error

## Examples

### Complete Workflow
```bash
# Create new project
plhub create calculator --template console
cd calculator

# Install dependencies  
plhub install math_utils

# Edit your code
# ... edit src/main.poh ...

# Test your code
plhub run src/main.poh

# Build for production
plhub build --target dart --release

# Run tests
plhub test

# Publish (if creating a package)
plhub publish
```

### Package Development
```bash
# Create package project
plhub create my_package --template basic

# Develop your package
# ... edit src/ files ...

# Test locally
plhub install ./

# Publish to registry
plhub publish
```