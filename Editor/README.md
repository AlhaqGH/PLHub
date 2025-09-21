# PohLang Editor Integrations

This directory contains editor integrations and IDE support for PohLang development within the PLHub environment.

## Features

### Current
- Basic syntax highlighting definitions
- File association (.poh files)
- Comment and bracket matching

### Planned
- Language Server Protocol (LSP) implementation  
- IntelliSense/autocomplete
- Error highlighting and diagnostics
- Code formatting
- Snippet support
- Debugging integration

## Supported Editors

### VS Code
- **File**: `vscode/` - Extension files for Visual Studio Code
- **Install**: Copy to VS Code extensions directory
- **Features**: Syntax highlighting, file icons

### Sublime Text
- **File**: `sublime/` - Package files for Sublime Text
- **Features**: Syntax definitions, build systems

### Vim/Neovim  
- **File**: `vim/` - Vim plugin files
- **Features**: Syntax highlighting, filetype detection

### Other Editors
- **Emacs**: Basic major mode (planned)
- **Atom**: Grammar and package (planned)
- **IntelliJ**: Plugin support (future)

## Development

### Adding New Editor Support
1. Create directory for editor: `mkdir editor_name/`
2. Add syntax definition files
3. Update this README
4. Test with sample .poh files

### Language Server
The Language Server Protocol implementation will provide:
- Real-time error checking
- Auto-completion based on PohLang grammar
- Function signature help
- Go-to-definition
- Refactoring support

### Testing
Use the examples in `../Examples/` to test editor integrations.

## Installation

```bash
# Install PLHub with editor support
pip install plhub[editor]

# Or install manually by copying files to your editor's extensions directory
```

## Contributing

Help improve PohLang editor support:
- Add new editor integrations
- Improve existing syntax definitions  
- Implement LSP features
- Create code snippets and templates