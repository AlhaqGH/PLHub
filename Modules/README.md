# PohLang Modules & Packages

This directory contains the PLHub package registry and module ecosystem for PohLang.

## Structure

```
Modules/
├─ community/          # Community-contributed packages
├─ official/           # Official PLHub modules
├─ local/              # Local development packages
├─ templates/          # Module templates
└─ registry.json       # Package registry metadata
```

## Package Types

### Official Modules
Core modules maintained by the PohLang team:
- **math**: Mathematical operations and utilities
- **strings**: String manipulation functions
- **io**: File and I/O operations
- **web**: Web and HTTP utilities
- **data**: Data structures and algorithms

### Community Packages
Third-party packages contributed by the community:
- Installable via `plhub install <package_name>`
- Hosted in community/ directory
- Follow PLHub package standards

### Local Packages
Development packages for local projects:
- Private modules not published to registry
- Project-specific utilities
- Testing and experimental code

## Creating a Package

### 1. Create Package Structure
```bash
# Use PLHub template
plhub create-package my_package

# Or manually create
mkdir Modules/local/my_package
cd Modules/local/my_package
```

### 2. Package Files
```
my_package/
├─ plhub-package.json  # Package metadata
├─ README.md           # Documentation
├─ src/                # Source .poh files
│  ├─ main.poh        # Main entry point
│  └─ utils.poh       # Utility functions
├─ examples/           # Usage examples
└─ tests/              # Package tests
```

### 3. Package Configuration (`plhub-package.json`)
```json
{
  "name": "my_package",
  "version": "1.0.0", 
  "description": "My awesome PohLang package",
  "author": "Your Name",
  "main": "src/main.poh",
  "keywords": ["utility", "helper"],
  "dependencies": {},
  "pohlang_version": ">=0.5.0"
}
```

## Installing Packages

```bash
# Install from registry
plhub install math_utils

# Install local package
plhub install ./Modules/local/my_package

# List installed packages
plhub list packages
```

## Using Packages

In your PohLang code:
```pohLang
# Import package functions
Import "math_utils"

# Use package functions
Set result to math_utils.square(5)
Write "5 squared is " plus result
```

## Publishing Packages

### To Community Registry
1. Test your package thoroughly
2. Follow naming conventions
3. Submit PR to PLHub repository
4. Package will be reviewed and added

### Package Standards
- Clear documentation and examples
- Follow PohLang naming conventions
- Include comprehensive tests  
- Use semantic versioning
- MIT or compatible license

## Development

### Creating Module Templates
Add new templates to `templates/` for different package types:
- `basic`: Simple utility package
- `library`: Complex library with multiple modules
- `tool`: Command-line tool package

### Registry Management
The `registry.json` file contains metadata for all available packages:
- Package names and versions
- Dependencies and compatibility
- Installation instructions
- Popularity metrics