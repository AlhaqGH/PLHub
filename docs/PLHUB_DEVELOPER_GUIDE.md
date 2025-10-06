# PLHub Developer Guide

## Overview

PLHub is the comprehensive development toolkit for PohLang, analogous to what Flutter is to Dart or Cargo is to Rust. It provides project management, runtime integration, package management, and development tools all in one unified environment.

## Architecture

```
PLHub/
├── plhub.py          # Main CLI entry point
├── Runtime/          # PohLang Rust runtime
│   ├── bin/          # Compiled runtime binary (pohlang.exe)
│   ├── Interpreter/  # Python interpreter (fallback)
│   ├── transpiler/   # Dart transpiler
│   └── pohlang_metadata.json
├── templates/        # Project templates
├── CLI/              # CLI utilities
├── Tools/            # Additional development tools
└── Modules/          # Package registry

```

## Key Features

### 1. Runtime Management

PLHub integrates with the PohLang Rust runtime, providing:

- **Automatic Runtime Detection**: Finds runtime in Runtime/bin/, legacy bin/, or PATH
- **Local Build Sync**: `plhub sync-runtime-local` copies your local Rust build
- **Remote Updates**: `plhub update-runtime` downloads official SDK releases
- **Version Tracking**: Metadata tracking with source provenance

### 2. Project Scaffolding

Create and manage PohLang projects with ease:

```bash
# Create a new project
plhub create my_project

# Initialize in existing directory
plhub init --name my_project

# Use templates
plhub create my_project --template console
```

Project structure:
```
my_project/
├── plhub.json        # Project configuration
├── src/
│   └── main.poh      # Main entry point
├── tests/            # Test files
└── examples/         # Example code
```

### 3. Project Configuration (plhub.json)

```json
{
  "name": "my_project",
  "version": "1.0.0",
  "description": "My PohLang project",
  "main": "src/main.poh",
  "dependencies": {},
  "dev_dependencies": {},
  "scripts": {
    "start": "plhub run src/main.poh",
    "build": "plhub build",
    "test": "plhub test"
  }
}
```

### 4. Development Workflow

#### Running Code

```bash
# Run with Rust runtime (preferred)
plhub run src/main.poh

# Run with verbose output
plhub run src/main.poh --verbose

# Run with debugging
plhub run src/main.poh --debug
```

#### Building

```bash
# Build to bytecode (default)
plhub build --target bytecode

# Transpile to Dart
plhub build --target dart

# AOT compilation (future)
plhub build --target native
```

#### Testing

```bash
# Run all tests
plhub test

# Run specific tests
plhub test --filter my_test

# Verbose test output
plhub test --verbose
```

### 5. Environment Health Checks

```bash
# Check environment status
plhub doctor

# Detailed diagnostics
plhub doctor --verbose
```

The `doctor` command checks:
- ✅ Python version and availability
- ✅ PohLang Rust runtime status and version
- ✅ Runtime metadata and installation source
- ✅ Python interpreter fallback
- ✅ Dart SDK (optional, for transpilation)
- ✅ Project configuration
- ✅ Available templates

### 6. Cleaning Build Artifacts

```bash
# Clean build directory and bytecode
plhub clean

# Also clean dependencies
plhub clean --all
```

## Command Reference

### Project Management

| Command | Description | Example |
|---------|-------------|---------|
| `create` | Create new project | `plhub create my_app` |
| `init` | Initialize in current dir | `plhub init` |
| `build` | Build project | `plhub build --target dart` |
| `run` | Run a .poh file | `plhub run main.poh` |
| `test` | Run tests | `plhub test --filter unit` |
| `clean` | Clean artifacts | `plhub clean --all` |

### Runtime Management

| Command | Description | Example |
|---------|-------------|---------|
| `sync-runtime-local` | Copy local Rust build | `plhub sync-runtime-local` |
| `sync-runtime-local --profile release` | Copy release build | `plhub sync-runtime-local --profile release` |
| `update-runtime` | Download SDK release | `plhub update-runtime --version 0.5.0` |
| `doctor` | Health check | `plhub doctor --verbose` |

### Package Management (Coming Soon)

| Command | Description | Example |
|---------|-------------|---------|
| `install` | Install package | `plhub install http` |
| `list packages` | List packages | `plhub list packages` |

### Information

| Command | Description | Example |
|---------|-------------|---------|
| `list examples` | Show examples | `plhub list examples` |
| `list templates` | Show templates | `plhub list templates` |
| `--version` | Show version | `plhub --version` |
| `--help` | Show help | `plhub --help` |

## Templates

### basic
Simple console application with variables and arithmetic.

### console
Interactive console app with menu system and user input.

### web
Placeholder for web application features (experimental).

## Runtime Integration

### Priority Order

1. **Runtime/bin/pohlang.exe** (or pohlang on Unix) - Preferred
2. **bin/pohlang.exe** - Legacy location
3. **PATH environment** - System-wide installation
4. **Python Interpreter** - Fallback if no Rust runtime found

### Syncing Local Builds

During development:

```bash
# Build runtime
cd PohLang/runtime
cargo build

# Sync to PLHub
cd ../../PLHub
python plhub.py sync-runtime-local

# Or with release build
python plhub.py sync-runtime-local --profile release
```

### Metadata Tracking

Runtime metadata is stored in `Runtime/pohlang_metadata.json`:

```json
{
  "pohlang_version": "0.5.0",
  "source_repo": "https://github.com/AlhaqGH/PohLang",
  "build_profile": "debug",
  "installed_binary": "Runtime/bin/pohlang.exe",
  "installed_at": "2025-10-05T12:00:00.000000Z",
  "source": "local_build"
}
```

## Best Practices

### 1. Always Use Start Program/End Program

All .poh files should be wrapped:

```poh
Start Program

# Your code here
Write "Hello, World!"

End Program
```

### 2. Use Comments

Both `#` and `//` are supported for comments:

```poh
Start Program

# This is a comment
// This is also a comment

Write "Hello"  # Inline comments work too

End Program
```

### 3. Organize Projects

Recommended structure:

```
my_project/
├── src/
│   ├── main.poh
│   └── lib.poh
├── tests/
│   ├── test_main.poh
│   └── test_lib.poh
├── examples/
│   └── demo.poh
└── plhub.json
```

### 4. Use `doctor` for Troubleshooting

Before reporting issues, run:

```bash
plhub doctor --verbose
```

This provides diagnostic information about your environment.

### 5. Keep Runtime Updated

Sync your runtime after changes:

```bash
# After building PohLang runtime
plhub sync-runtime-local

# Check version
plhub doctor
```

## Development vs Production

### Development

```bash
# Use debug build for faster iteration
cargo build --manifest-path ../PohLang/runtime/Cargo.toml
plhub sync-runtime-local

# Run with verbose output
plhub run src/main.poh --verbose
```

### Production

```bash
# Use release build for performance
cargo build --release --manifest-path ../PohLang/runtime/Cargo.toml
plhub sync-runtime-local --profile release

# Build optimized bytecode
plhub build --target bytecode
```

## Troubleshooting

### Runtime Not Found

```bash
$ plhub run main.poh
Error: PohLang Rust runtime not found

# Solution:
$ plhub sync-runtime-local
# Or download release
$ plhub update-runtime
```

### Python Interpreter Fallback

If you see "Warning: failed to run with Rust runtime", PLHub is using the Python interpreter. For better performance:

1. Build the Rust runtime: `cargo build --manifest-path ../PohLang/runtime/Cargo.toml`
2. Sync it: `plhub sync-runtime-local`
3. Verify: `plhub doctor`

### Build Failures

```bash
# Clean and rebuild
plhub clean --all
cargo build --manifest-path ../PohLang/runtime/Cargo.toml
plhub sync-runtime-local
```

### Template Syntax Errors

All templates now include `Start Program`/`End Program` wrappers. If you have old templates:

```poh
# Add wrapper
Start Program

# ... your existing code ...

End Program
```

## Advanced Usage

### Custom Templates

Create templates in `templates/my_template.poh`:

```poh
Start Program

# My Custom Template
Write "Custom template starter"

# Template-specific code here

End Program
```

### CI/CD Integration

```yaml
# Example GitHub Actions workflow
- name: Setup PLHub
  run: |
    python plhub.py update-runtime --version latest
    python plhub.py doctor

- name: Build and Test
  run: |
    python plhub.py build
    python plhub.py test
```

### Multiple Runtimes

PLHub can work with different runtime versions:

```bash
# Development version
plhub sync-runtime-local --pohlang-path ./PohLang-dev

# Stable version
plhub update-runtime --version 0.5.0
```

## Contributing

To contribute to PLHub:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with `plhub doctor` and `plhub test`
5. Submit a pull request

## See Also

- [PohLang Guide](../PohLang/PohLang_Guide.md) - Language documentation
- [Runtime Design](../PohLang/runtime/DESIGN.md) - Runtime architecture
- [Grammar Spec](../PohLang/spec/Grammar.md) - Language grammar
- [Vocabulary Spec](../PohLang/spec/Vocabulary.md) - Keyword reference

## Version History

### v0.5.0 (Current)
- ✅ Integrated Rust runtime support
- ✅ Added `doctor` command for environment health checks
- ✅ Added `init` command for project initialization
- ✅ Added `test` and `clean` commands
- ✅ Enhanced `sync-runtime-local` with metadata tracking
- ✅ Updated templates with Start Program/End Program wrappers
- ✅ Added # comment support in parser
- ✅ Improved error messages and diagnostics

### Future Plans
- Package manager with dependency resolution
- Hot reload during development
- Interactive REPL
- Language server protocol support
- VS Code extension integration
- Web-based playground
