# PohLang Hub - Complete Development Environment

![PohLang Hub](https://img.shields.io/badge/PLHub-v0.2.3-blue.svg)
![VS Code](https://img.shields.io/badge/VS%20Code-Extension-green.svg)
![PohLang](https://img.shields.io/badge/PohLang-v0.6.0-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**The complete PohLang development environment for VS Code** - Project management, package tools, SDK updates, and full IDE integration for building PohLang applications.

> **Note**: This extension requires the [PohLang Language Support extension](https://marketplace.visualstudio.com/items?itemName=pohlang.pohlang) for syntax highlighting and IntelliSense.

## 🎯 What's New in v0.2.3

### 🔧 Extension Separation (October 2025)
- **Clean Architecture**: Language support moved to separate extension
- **No Conflicts**: Prevents VS Code crashes from duplicate registrations
- **Better Performance**: Each extension focuses on its core responsibility
- **Requires**: Install both extensions for full functionality

### 🚨 Phase 5: Error Handling (v0.6.0 Runtime)
Complete error handling system with natural English messages:

```pohlang
# Try-catch-finally blocks
try this:
    Make result = divide 10 by 0
if error of type "MathError" as e:
    Write "Math problem: " + error message of e
finally:
    Write "Cleanup complete"
end try

# Custom error types
make error type "ValidationError"
throw error "ValidationError" with message "Invalid input"
```

**7 Built-in Error Types**: RuntimeError, TypeError, MathError, FileError, JsonError, NetworkError, ValidationError

## ✨ Features

### 🏗️ Project Management
- **Create Projects**: Scaffold new PohLang applications with templates
- **Workspace Support**: Multi-root workspace compatibility
- **Project Templates**: Pre-configured project structures
- **Dependency Management**: Track and manage project dependencies

### 📦 Package & SDK Management
- **Auto-Update**: Automatically fetch latest PohLang runtime and PLHub SDK
- **Version Tracking**: Display installed SDK versions
- **Manual Updates**: Control when to update interpreter
- **GitHub Integration**: Direct download from official releases
- **Configurable Repos**: Point to custom forks if needed

### ⚡ Code Execution
- **Run File** (Ctrl+F5): Execute current `.poh` file with v0.5.4 runtime
- **Error Handling**: Natural English error messages with file locations
- **Integrated Terminal**: View output directly in VS Code
- **Environment Examples**: Test installation with sample code
- **Background Processes**: Support for long-running programs

### 🔧 Development Tools
- **Full Language Support**: Syntax highlighting, IntelliSense, snippets (requires PohLang extension)
- **Real-time Diagnostics**: Error detection as you type
- **Project Scaffolding**: Quick project setup with best practices
- **Configuration Management**: Customize SDK behavior per workspace

### 🎨 IDE Integration
- **Command Palette**: All features accessible via Ctrl+Shift+P
- **Context Menus**: Right-click .poh files to run
- **Status Bar**: SDK version indicators
- **Settings Panel**: Full configuration UI
- **Multi-Platform**: Windows, macOS, Linux support

## 📥 Installation

### From VS Code Marketplace
1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X)
3. Search for "PohLang Hub"
4. Click Install
5. **Recommended**: Also install "PohLang Language Support" for full IDE features

### Manual Installation
```bash
# Download the .vsix file
code --install-extension pohlang-hub-0.2.0.vsix
```

## 🚀 Getting Started

### 1. Install Both Extensions
For the best experience, install both:
- **PohLang Language Support** - Syntax, IntelliSense, snippets
- **PohLang Hub** (this extension) - Projects, packages, tools

### 2. Create Your First Project
```
Ctrl+Shift+P → "PL-Hub: Create Project"
```
- Choose a directory
- Enter project name
- Start coding in `src/main.poh`

### 3. Write PohLang Code with Error Handling
```pohlang
# Modern PohLang with error handling
Make function main:
    try this:
        Make name = Ask for "What's your name? "
        
        If name equals "":
            throw error "ValidationError" with message "Name cannot be empty"
        end if
        
        Write "Hello, " + name + "!"
        
    if error of type "ValidationError" as e:
        Write "Validation failed: " + error message of e
        
    if error as e:
        Write "Something went wrong: " + error message of e
        
    finally:
        Write "Program complete"
    end try
end function

# Run it
main()
```

### 4. Run Your Code
- Press **Ctrl+F5** to execute
- View output in integrated terminal
- See natural English error messages if anything goes wrong

## 🎮 Commands

| Command | Description | Shortcut |
|---------|-------------|----------|
| `PL-Hub: Run File` | Execute current .poh file | Ctrl+F5 |
| `PL-Hub: Create Project` | Create new PohLang project | - |
| `PL-Hub: Update Language` | Download latest interpreter | - |
| `PL-Hub: Run Environment Example` | Test installation | - |
| `PL-Hub: Show SDK Versions` | Display installed versions | - |

## ⚙️ Configuration

### Settings (File → Preferences → Settings → PohLang Hub)

```json
{
  // GitHub repositories for releases
  "pohlangHub.pohlangRepo": "AlhaqGH/PohLang",
  "pohlangHub.plhubRepo": "AlhaqGH/PLHub",
  
  // Auto-update behavior
  "pohlangHub.autoUpdate": true,
  "pohlangHub.updateIntervalDays": 7,
  
  // Optional: Pin to specific version
  "pohlangHub.sdkTagOverride": "",
  
  // Optional: GitHub token for higher rate limits
  "pohlangHub.githubToken": ""
}
```

### Key Settings:
- **autoUpdate**: Automatically check for SDK updates
- **updateIntervalDays**: How often to check (0 = every run)
- **sdkTagOverride**: Pin to specific git tag (e.g., "v0.5.4")
- **githubToken**: Personal access token for API rate limits

## 🎯 Extension Architecture

**PohLang Hub** is the **full development environment** - like the Flutter extension:
- ✅ Project management and scaffolding
- ✅ Package and SDK management
- ✅ Build and deployment tools
- ✅ Auto-update functionality
- ✅ Developer workflows

**PohLang Language Support** is the **language basics** - like the Dart extension:
- ✅ Syntax highlighting
- ✅ IntelliSense and completion
- ✅ Code snippets
- ✅ Basic code execution
- ✅ Integrated runtime

**Use both together** for the complete PohLang IDE experience!

## 🔧 Requirements

- **VS Code**: 1.70.0 or higher
- **Node.js**: Included with VS Code
- **PohLang Runtime**: v0.5.4 (auto-downloaded by extension)
- **Optional**: PohLang Language Support extension (recommended)

## 🛠️ Development

### Setup
```bash
git clone https://github.com/pohlang/PLHub-VS-Code-extension.git
cd PLHub-VS-Code-extension
npm install
npm run compile
```

### Build & Package
```bash
# Compile TypeScript
npm run compile

# Package extension
npx vsce package

# Install locally
code --install-extension pohlang-hub-0.2.0.vsix
```

### Testing
```bash
# Run extension in dev mode
code .
# Press F5 to launch Extension Development Host
```

## 📂 Project Structure

```
PLHub-VS-Code-extension/
├── src/
│   ├── extension.ts              # Main entry point
│   ├── commands/                 # VS Code commands
│   │   ├── runFile.ts           # File execution
│   │   ├── createProject.ts     # Project scaffolding
│   │   ├── updateLanguage.ts    # SDK updates
│   │   └── showSDKVersions.ts   # Version display
│   ├── language/                 # Language support
│   │   ├── diagnostics.ts       # Error detection
│   │   └── completion.ts        # IntelliSense
│   └── utils/                    # Utilities
│       ├── processUtils.ts      # Process management
│       └── fetchLatestSDKs.ts   # SDK downloads
├── bin/
│   └── pohlang.exe              # PohLang v0.5.4 runtime
├── images/
│   └── PLHUB.png                # Extension icon
├── syntaxes/
│   └── pohlang.tmLanguage.json  # Syntax grammar
├── snippets/
│   └── pohlang.json             # Code snippets
├── package.json                  # Extension manifest
└── README.md                     # This file
```

## 🐛 Troubleshooting

### Runtime Not Found
The extension automatically downloads the runtime. If issues occur:
1. Run "PL-Hub: Update Language" from Command Palette
2. Check `pohlangHub.pohlangRepo` setting is correct
3. Verify internet connection

### Auto-Update Not Working
1. Check `pohlangHub.autoUpdate` is enabled
2. Verify `updateIntervalDays` setting
3. Try manual update: "PL-Hub: Update Language"

### GitHub Rate Limit
If you hit API rate limits:
1. Create a GitHub Personal Access Token
2. Add to `pohlangHub.githubToken` setting
3. Rate limit increases from 60 to 5000 requests/hour

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Make changes and test thoroughly
4. Commit: `git commit -am 'Add feature'`
5. Push: `git push origin feature-name`
6. Create Pull Request

## 📄 License

MIT License - see [LICENSE](https://github.com/pohlang/PLHub/blob/HEAD/LICENSE) file for details

## 🔗 Resources

- **PohLang Runtime**: [github.com/AlhaqGH/PohLang](https://github.com/AlhaqGH/PohLang)
- **PLHub SDK**: [github.com/AlhaqGH/PLHub](https://github.com/AlhaqGH/PLHub)
- **Documentation**: [PohLang Guide](https://github.com/AlhaqGH/PohLang/blob/main/doc/PohLang_Guide.md)
- **Issues**: [github.com/AlhaqGH/PLHub/issues](https://github.com/AlhaqGH/PLHub/issues)
- **Discussions**: [github.com/AlhaqGH/PLHub/discussions](https://github.com/AlhaqGH/PLHub/discussions)

## 📊 Changelog

See [CHANGELOG.md](https://github.com/pohlang/PLHub/blob/HEAD/CHANGELOG.md) for version history and detailed updates.

---

**Build powerful PohLang applications with the complete development environment! 🚀**

*For language support only, use the PohLang Language Support extension alongside this one.*