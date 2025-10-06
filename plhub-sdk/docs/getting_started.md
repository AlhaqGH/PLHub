# Getting Started with PLHub

Welcome to PL-Hub, the comprehensive development environment for PohLang!

## What is PLHub?

PLHub is to PohLang what Flutter is to Dart - a complete development ecosystem that provides:

- **Project Management**: Create, build, and manage PohLang projects
- **Package System**: Install and manage dependencies
- **Development Tools**: CLI tools, editor support, and build systems
- **Templates**: Quick-start templates for different project types

## Installation

### Prerequisites
1. **Python 3.9+**: Required for PLHub tools
2. **PohLang**: The core language implementation

### Install PohLang Core
```bash
pip install pohlang
```

### Install PLHub
```bash
git clone https://github.com/AlhaqGH/PLHub
cd PLHub
pip install -e .
```

## Quick Start

### 1. Create Your First Project
```bash
# Create a new console application
plhub create my_first_app --template console

# Navigate to the project
cd my_first_app
```

### 2. Explore the Project Structure
```
my_first_app/
├─ src/
│  └─ main.poh          # Your main program file
├─ examples/            # Example programs
├─ tests/               # Test files
├─ plhub.json          # Project configuration
└─ README.md           # Project documentation
```

### 3. Run Your Program
```bash
# Run using PLHub
plhub run src/main.poh

# Or run directly with PohLang
pohlang src/main.poh
```

### 4. Edit Your Program
Open `src/main.poh` in your favorite editor:

```pohLang
Write "Welcome to your PohLang console application!"

Ask for name
Write "Hello " plus name plus "!"

Set count to 0
Repeat 3
    Set count to count plus 1
    Write "Loop iteration: " plus count
End

Write "Thanks for using PohLang!"
```

## Available Commands

### Project Management
```bash
# Create new project
plhub create <project_name> [--template basic|console|web]

# Run a program
plhub run <file.poh>

# Build project
plhub build [--target dart|python]
```

### Package Management
```bash
# Install a package
plhub install <package_name>

# List installed packages
plhub list packages

# List available packages
plhub list examples
```

### Templates
```bash
# List available templates
plhub list templates

# Create project with specific template
plhub create web_app --template web
```

## Project Configuration

The `plhub.json` file contains your project settings:

```json
{
  "name": "my_project",
  "version": "1.0.0",
  "description": "My PohLang project",
  "main": "src/main.poh",
  "dependencies": {
    "math_utils": "^1.0.0"
  },
  "dev_dependencies": {}
}
```

## Editor Support

PLHub includes editor support for:
- **VS Code**: Syntax highlighting and language support
- **Sublime Text**: Basic syntax definitions
- **Vim**: Syntax highlighting
- More editors coming soon!

### VS Code Setup
1. Copy `Editor/vscode/` to your VS Code extensions directory
2. Reload VS Code
3. Open any `.poh` file to see syntax highlighting

## Examples

PLHub comes with examples in the `Examples/` directory:

```bash
# Run a simple example
plhub run Examples/hello_world.poh

# Explore more examples
plhub list examples
```

## Next Steps

- **Learn PohLang**: Check out the [PohLang Guide](../PohLang/PohLang_Guide.md)
- **Create Packages**: Read the [Package Development Guide](package_development.md)
- **Editor Setup**: Configure your editor with [Editor Setup Guide](editor_setup.md)
- **Advanced Features**: Explore [Build System](build_system.md) and deployment

## Getting Help

- **Documentation**: Browse the `docs/` directory
- **Examples**: Check `Examples/` for sample programs
- **Issues**: Report problems on [GitHub Issues](https://github.com/AlhaqGH/PLHub/issues)
- **Community**: Join discussions on [GitHub Discussions](https://github.com/AlhaqGH/PLHub/discussions)

Happy coding with PohLang and PLHub! 🚀