# Complete Application Building Guide for PohLang & PLHub

## 🎯 Overview

This guide walks you through building **complete, production-ready applications** using PohLang and PLHub, from initial creation to final deployment.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Application Types](#application-types)
3. [Complete Workflow](#complete-workflow)
4. [Console Applications](#console-applications)
5. [Web Applications](#web-applications)
6. [Desktop Applications](#desktop-applications)
7. [Mobile Applications](#mobile-applications)
8. [Testing & Quality Assurance](#testing-quality-assurance)
9. [Building & Packaging](#building-packaging)
10. [Deployment](#deployment)
11. [Best Practices](#best-practices)

---

## Prerequisites

### Required Tools

```bash
# 1. Install PLHub (includes PohLang runtime)
pip install plhub

# 2. Verify installation
python plhub.py doctor

# 3. Check runtime status
python plhub.py doctor --verbose
```

### Optional Platform SDKs

Depending on your target platform:

- **Android**: Android Studio, SDK 21+
- **iOS/macOS**: Xcode 14+
- **Windows**: Visual Studio 2022, WinUI3 SDK
- **Web**: Node.js 16+, npm/yarn
- **Desktop**: Platform-specific build tools

---

## Application Types

PLHub supports building complete applications for multiple platforms:

### 1. Console Applications
- Command-line tools
- Batch processors
- System utilities
- Data processing scripts

### 2. Web Applications
- Progressive Web Apps (PWA)
- Single Page Applications (SPA)
- Static websites
- Web APIs

### 3. Desktop Applications
- Windows (WinUI3/UWP)
- macOS (AppKit/SwiftUI)
- Linux (GTK)
- Cross-platform (Electron-style)

### 4. Mobile Applications
- Android (Material Design)
- iOS (SwiftUI)
- Cross-platform responsive

---

## Complete Workflow

Every complete application follows this workflow:

```
1. CREATE    → Initialize project with template
2. DEVELOP   → Write code, add features
3. TEST      → Unit tests, integration tests
4. BUILD     → Compile to target platform
5. PACKAGE   → Create distributable
6. DEPLOY    → Publish to users
```

### Visual Workflow Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                    Complete App Lifecycle                     │
└──────────────────────────────────────────────────────────────┘

  [CREATE]          [DEVELOP]         [TEST]           [BUILD]
     │                  │                │                │
     ▼                  ▼                ▼                ▼
  plhub.py          Edit code       plhub.py         plhub.py
   create            in IDE           test             build
     │                  │                │                │
     └──────────────────┴────────────────┴────────────────┘
                           │
                           ▼
                  [PACKAGE & DEPLOY]
                           │
            ┌──────────────┼──────────────┐
            │              │              │
            ▼              ▼              ▼
        Installer    App Store     Web Host
```

---

## Console Applications

### Step 1: Create Project

```bash
# Create a new console application
python plhub.py create calculator --template console
cd calculator

# Project structure created:
# calculator/
# ├── src/
# │   ├── main.poh           # Main entry point
# │   ├── logic.poh          # Business logic
# │   └── helpers.poh        # Helper functions
# ├── tests/
# │   └── test_main.poh      # Unit tests
# ├── assets/
# │   └── config.json        # Configuration
# ├── plhub.json             # Project configuration
# └── README.md              # Documentation
```

### Step 2: Develop Features

Edit `src/main.poh`:

```pohlang
Start Program

# Import modules
Import "logic" from "./logic.poh"
Import "helpers" from "./helpers.poh"

# Display header
Call display_header from helpers

# Main application loop
Set running to True

While running is True
    # Show menu
    Write "=== Calculator ==="
    Write "1. Add"
    Write "2. Subtract"
    Write "3. Multiply"
    Write "4. Divide"
    Write "5. Exit"
    Write ""
    
    Ask for choice
    
    If choice is "5"
        Set running to False
    Otherwise
        # Get numbers
        Ask for num1
        Ask for num2
        
        # Perform calculation
        If choice is "1"
            Set result to Call add from logic with num1, num2
        End If
        
        If choice is "2"
            Set result to Call subtract from logic with num1, num2
        End If
        
        If choice is "3"
            Set result to Call multiply from logic with num1, num2
        End If
        
        If choice is "4"
            Set result to Call divide from logic with num1, num2
        End If
        
        # Display result
        Write "Result: " plus result
        Write ""
    End If
End While

Write "Goodbye!"

End Program
```

Edit `src/logic.poh`:

```pohlang
Start Program

# Math operations module

Function add with a, b
    Return a plus b
End Function

Function subtract with a, b
    Return a minus b
End Function

Function multiply with a, b
    Return a times b
End Function

Function divide with a, b
    If b is 0
        Write "Error: Division by zero"
        Return 0
    End If
    Return a divided by b
End Function

End Program
```

Edit `src/helpers.poh`:

```pohlang
Start Program

# Helper functions

Function display_header
    Write "================================"
    Write "    Advanced Calculator v1.0    "
    Write "================================"
    Write ""
End Function

Function validate_number with input
    # Add validation logic
    Return True
End Function

End Program
```

### Step 3: Test

Create `tests/test_main.poh`:

```pohlang
Start Program

Import "logic" from "../src/logic.poh"

# Test addition
Set result to Call add from logic with 5, 3
If result is 8
    Write "✓ Addition test passed"
Otherwise
    Write "✗ Addition test failed"
End If

# Test division by zero
Set result to Call divide from logic with 10, 0
If result is 0
    Write "✓ Division by zero handled"
Otherwise
    Write "✗ Division by zero test failed"
End If

Write "All tests completed"

End Program
```

Run tests:

```bash
python plhub.py test
# Or run specific test
python plhub.py run tests/test_main.poh
```

### Step 4: Build

```bash
# Build to bytecode (fast execution)
python plhub.py build --target bytecode --release

# Or build native executable (future)
python plhub.py build --target native --release

# Output: build/calculator.pbc or build/calculator.exe
```

### Step 5: Package

```bash
# Create distributable package
python plhub.py package --platform windows --out dist/

# Creates:
# dist/
# ├── calculator.exe      # Executable
# ├── config.json         # Configuration
# ├── README.txt          # User guide
# └── LICENSE.txt         # License
```

### Step 6: Deploy

```bash
# Local installation
python plhub.py install --local dist/calculator.exe

# Or upload to distribution server
python plhub.py publish dist/calculator --registry https://packages.pohlang.org
```

---

## Web Applications

### Step 1: Create Web Project

```bash
python plhub.py create my-webapp --template web
cd my-webapp
```

### Step 2: Project Structure

```
my-webapp/
├── src/
│   ├── main.poh              # Application logic
│   ├── routes.poh            # Route handlers
│   └── components/
│       ├── header.poh
│       ├── footer.poh
│       └── page.poh
├── public/
│   ├── index.html            # HTML template
│   ├── styles.css            # Stylesheets
│   └── assets/               # Images, fonts
├── tests/
│   └── test_routes.poh
├── plhub.json                # Project config
├── webpack.config.js         # Build config
└── package.json              # Web dependencies
```

### Step 3: Develop Web App

Edit `src/main.poh`:

```pohlang
Start Program

# Web application main entry

Import "routes" from "./routes.poh"
Import "header" from "./components/header.poh"

# Initialize web server
Set port to 8080
Set host to "localhost"

Write "Starting web server on " plus host plus ":" plus port

# Define routes
Call setup_routes from routes

# Start server (conceptual - actual implementation in transpiled code)
Call start_server with host, port

Write "Server running! Visit http://localhost:8080"

End Program
```

### Step 4: Build for Web

```bash
# Build web application
python plhub.py build --target web --release

# Output: build/web/
# ├── index.html           # Optimized HTML
# ├── main.js              # Transpiled + bundled JS
# ├── styles.css           # Minified CSS
# └── assets/              # Optimized assets
```

### Step 5: Test Web App

```bash
# Run development server with hot reload
python plhub.py dev --port 8080

# Run in browser
# Visit http://localhost:8080

# Run automated tests
python plhub.py test --platform web
```

### Step 6: Deploy Web App

```bash
# Deploy to static hosting
python plhub.py deploy --target netlify
python plhub.py deploy --target vercel
python plhub.py deploy --target github-pages

# Or deploy to custom server
python plhub.py deploy --target custom --server user@example.com:/var/www
```

---

## Desktop Applications

### Windows Desktop App

```bash
# Create Windows desktop application
python plhub.py create notes-app --template windows-desktop
cd notes-app

# Build
python plhub.py build --target windows --release

# Package as MSIX
python plhub.py package --format msix --out dist/

# Deploy to Microsoft Store
python plhub.py deploy --target ms-store --config store.json
```

### macOS Desktop App

```bash
# Create macOS application
python plhub.py create notes-app --template macos-desktop
cd notes-app

# Build
python plhub.py build --target macos --release

# Package as DMG
python plhub.py package --format dmg --out dist/

# Deploy to Mac App Store
python plhub.py deploy --target mac-app-store --config appstore.json
```

### Linux Desktop App

```bash
# Create Linux application
python plhub.py create notes-app --template linux-desktop
cd notes-app

# Build
python plhub.py build --target linux --release

# Package as AppImage
python plhub.py package --format appimage --out dist/

# Or package as DEB
python plhub.py package --format deb --out dist/
```

---

## Mobile Applications

### Android Mobile App

```bash
# Create Android application
python plhub.py create todo-app --template android
cd todo-app

# Project structure
# todo-app/
# ├── src/
# │   └── main.poh
# ├── android/
# │   ├── app/
# │   ├── build.gradle
# │   └── AndroidManifest.xml
# └── plhub.json

# Develop your app
# ... edit src/main.poh ...

# Build debug APK
python plhub.py build --target android --debug

# Build release AAB for Play Store
python plhub.py build --target android --release --format aab

# Test on device
python plhub.py run --target android --device <device-id>

# Deploy to Play Store
python plhub.py deploy --target play-store --config playstore.json
```

### iOS Mobile App

```bash
# Create iOS application
python plhub.py create todo-app --template ios
cd todo-app

# Project structure
# todo-app/
# ├── src/
# │   └── main.poh
# ├── ios/
# │   ├── App/
# │   ├── Info.plist
# │   └── Assets.xcassets
# └── plhub.json

# Build debug
python plhub.py build --target ios --debug

# Build release for App Store
python plhub.py build --target ios --release

# Test on simulator
python plhub.py run --target ios --simulator "iPhone 14"

# Test on device
python plhub.py run --target ios --device <device-id>

# Deploy to App Store
python plhub.py deploy --target app-store --config appstore.json
```

---

## Testing & Quality Assurance

### Unit Testing

Create comprehensive test suites:

```pohlang
Start Program

# Unit test example

Import "calculator" from "../src/calculator.poh"

# Test suite
Set passed to 0
Set failed to 0

# Test 1: Addition
Set result to Call add from calculator with 2, 3
If result is 5
    Set passed to passed plus 1
    Write "✓ Test 1 passed: Addition"
Otherwise
    Set failed to failed plus 1
    Write "✗ Test 1 failed: Addition"
End If

# Test 2: Edge case
Set result to Call add from calculator with 0, 0
If result is 0
    Set passed to passed plus 1
    Write "✓ Test 2 passed: Zero addition"
Otherwise
    Set failed to failed plus 1
    Write "✗ Test 2 failed: Zero addition"
End If

# Summary
Write ""
Write "Tests passed: " plus passed
Write "Tests failed: " plus failed

If failed is 0
    Write "All tests passed! ✓"
Otherwise
    Write "Some tests failed! ✗"
End If

End Program
```

Run tests:

```bash
# Run all tests
python plhub.py test

# Run specific test file
python plhub.py test tests/calculator_test.poh

# Run with coverage
python plhub.py test --coverage

# Watch mode (auto-run on changes)
python plhub.py test --watch
```

### Integration Testing

```bash
# Test full application flow
python plhub.py test --type integration

# Test with real dependencies
python plhub.py test --integration --db-enabled
```

### End-to-End Testing

```bash
# E2E tests for web apps
python plhub.py test --type e2e --browser chrome

# E2E tests for mobile apps
python plhub.py test --type e2e --device android-emulator
```

---

## Building & Packaging

### Build Configuration

Edit `plhub.json`:

```json
{
  "name": "my-app",
  "version": "1.0.0",
  "main": "src/main.poh",
  "dependencies": {
    "math-utils": "^1.0.0",
    "string-helpers": "^2.1.0"
  },
  "build": {
    "targets": ["windows", "macos", "linux"],
    "optimize": true,
    "minify": true,
    "bundle": true
  },
  "package": {
    "name": "My Application",
    "author": "Your Name",
    "description": "Complete application built with PohLang",
    "icon": "assets/icon.png",
    "license": "MIT"
  }
}
```

### Build Commands

```bash
# Development build (fast, with debug symbols)
python plhub.py build --debug

# Production build (optimized, minified)
python plhub.py build --release

# Build for specific platform
python plhub.py build --target windows --release
python plhub.py build --target macos --release
python plhub.py build --target linux --release

# Build for all platforms
python plhub.py build --all-platforms --release

# Custom output directory
python plhub.py build --release --out custom-build/
```

### Packaging Options

```bash
# Create installer package
python plhub.py package --format installer

# Create portable executable
python plhub.py package --format portable

# Create app bundle
python plhub.py package --format bundle

# Include dependencies
python plhub.py package --include-deps

# Code signing
python plhub.py package --sign --cert my-cert.p12
```

---

## Deployment

### Deployment Targets

#### 1. Local Installation

```bash
# Install on local machine
python plhub.py install --local build/my-app.exe

# Creates desktop shortcut
python plhub.py install --local --create-shortcut

# Add to system PATH
python plhub.py install --local --add-to-path
```

#### 2. Web Hosting

```bash
# Deploy to Netlify
python plhub.py deploy --target netlify
# Follow prompts for authentication and site selection

# Deploy to Vercel
python plhub.py deploy --target vercel

# Deploy to GitHub Pages
python plhub.py deploy --target github-pages --repo username/repo

# Deploy to custom server via SSH
python plhub.py deploy --target ssh --host example.com --user deploy --path /var/www/myapp
```

#### 3. App Stores

```bash
# Google Play Store (Android)
python plhub.py deploy --target play-store \
  --aab build/app-release.aab \
  --track production \
  --config playstore-config.json

# Apple App Store (iOS/macOS)
python plhub.py deploy --target app-store \
  --ipa build/app.ipa \
  --config appstore-config.json

# Microsoft Store (Windows)
python plhub.py deploy --target ms-store \
  --msix build/app.msix \
  --config msstore-config.json
```

#### 4. Package Registries

```bash
# Publish to PohLang package registry
python plhub.py publish --registry official

# Publish to custom registry
python plhub.py publish --registry https://my-registry.com
```

### Continuous Deployment

Create `.github/workflows/deploy.yml`:

```yaml
name: Build and Deploy

on:
  push:
    branches: [main]
    tags: ['v*']

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install PLHub
        run: pip install plhub
      
      - name: Run tests
        run: python plhub.py test
      
      - name: Build application
        run: python plhub.py build --release --all-platforms
      
      - name: Package
        run: python plhub.py package --format installer
      
      - name: Deploy
        run: python plhub.py deploy --target netlify
        env:
          NETLIFY_AUTH_TOKEN: ${{ secrets.NETLIFY_TOKEN }}
```

---

## Best Practices

### 1. Project Organization

```
my-app/
├── src/                    # Source code
│   ├── main.poh           # Main entry point
│   ├── models/            # Data models
│   ├── views/             # UI components
│   ├── controllers/       # Business logic
│   └── utils/             # Helper functions
├── tests/                  # Test files
│   ├── unit/              # Unit tests
│   ├── integration/       # Integration tests
│   └── e2e/               # End-to-end tests
├── assets/                 # Static resources
│   ├── images/
│   ├── fonts/
│   └── data/
├── docs/                   # Documentation
│   ├── API.md
│   ├── USAGE.md
│   └── CONTRIBUTING.md
├── build/                  # Build output (git-ignored)
├── dist/                   # Distribution packages (git-ignored)
├── plhub.json             # Project configuration
├── .gitignore             # Git ignore rules
├── README.md              # Project readme
└── LICENSE                # License file
```

### 2. Code Quality

```pohlang
Start Program

# Use clear variable names
Set user_age to 25        # Good
Set x to 25               # Bad

# Add comments for complex logic
# Calculate compound interest over n years
Set amount to principal times power of (1 plus rate), years

# Break complex operations into functions
Function calculate_total_price with items, tax_rate
    Set subtotal to sum of items
    Set tax to subtotal times tax_rate
    Return subtotal plus tax
End Function

# Validate inputs
Function divide with a, b
    If b is 0
        Write "Error: Cannot divide by zero"
        Return 0
    End If
    Return a divided by b
End Function

End Program
```

### 3. Version Control

```bash
# Initialize git repository
git init
git add .
git commit -m "Initial commit"

# Use semantic versioning
# v1.0.0 - Major.Minor.Patch

# Tag releases
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

### 4. Documentation

Always include:

- **README.md**: Project overview, installation, usage
- **CHANGELOG.md**: Version history and changes
- **LICENSE**: Software license
- **API.md**: API documentation for libraries
- **CONTRIBUTING.md**: Contribution guidelines

### 5. Error Handling

```pohlang
Start Program

# Proper error handling

Function load_config with filename
    # Try to load file
    If file_exists filename
        Set config to load_file filename
        Return config
    Otherwise
        Write "Error: Configuration file not found: " plus filename
        Write "Using default configuration"
        Return default_config
    End If
End Function

# Validate user input
Function get_positive_number
    Ask for number
    
    If number less than 0
        Write "Error: Please enter a positive number"
        Return Call get_positive_number  # Retry
    End If
    
    Return number
End Function

End Program
```

### 6. Performance Optimization

```pohlang
Start Program

# Cache expensive computations
Set fibonacci_cache to {}

Function fibonacci with n
    # Check cache first
    If contains n in fibonacci_cache
        Return fibonacci_cache at n
    End If
    
    # Compute and cache
    If n less than 2
        Set result to n
    Otherwise
        Set a to Call fibonacci with n minus 1
        Set b to Call fibonacci with n minus 2
        Set result to a plus b
    End If
    
    Set fibonacci_cache at n to result
    Return result
End Function

End Program
```

---

## Example: Complete Real-World Application

### Todo List Manager

Full source code for a complete, production-ready todo list application:

#### Project Structure

```
todo-manager/
├── src/
│   ├── main.poh
│   ├── todo.poh
│   ├── storage.poh
│   └── ui.poh
├── tests/
│   ├── test_todo.poh
│   └── test_storage.poh
├── assets/
│   ├── icon.png
│   └── config.json
├── plhub.json
└── README.md
```

#### src/main.poh

```pohlang
Start Program

Import "todo" from "./todo.poh"
Import "storage" from "./storage.poh"
Import "ui" from "./ui.poh"

# Load existing todos
Set todos to Call load_todos from storage

# Main application loop
Set running to True

While running is True
    # Display UI
    Call display_header from ui
    Call display_todos from ui with todos
    Call display_menu from ui
    
    # Get user choice
    Ask for choice
    
    # Handle actions
    If choice is "1"
        # Add new todo
        Ask for title
        Ask for description
        Set new_todo to Call create_todo from todo with title, description
        Set todos to append new_todo to todos
        Call save_todos from storage with todos
        Write "Todo added successfully!"
        
    Otherwise If choice is "2"
        # Mark todo as complete
        Ask for index
        Set todos to Call mark_complete from todo with todos, index
        Call save_todos from storage with todos
        Write "Todo marked as complete!"
        
    Otherwise If choice is "3"
        # Delete todo
        Ask for index
        Set todos to Call delete_todo from todo with todos, index
        Call save_todos from storage with todos
        Write "Todo deleted!"
        
    Otherwise If choice is "4"
        # Exit
        Set running to False
        
    Otherwise
        Write "Invalid choice. Please try again."
    End If
    
    Write ""
End While

Write "Goodbye!"

End Program
```

#### Build and Deploy

```bash
# Test
python plhub.py test

# Build for Windows
python plhub.py build --target windows --release

# Package
python plhub.py package --format installer --out dist/

# Deploy
python plhub.py install --local dist/todo-manager-setup.exe
```

---

## Troubleshooting

### Build Issues

```bash
# Check environment
python plhub.py doctor --verbose

# Clean build cache
python plhub.py clean

# Rebuild from scratch
python plhub.py clean && python plhub.py build --release
```

### Dependency Issues

```bash
# Update dependencies
python plhub.py update

# Reinstall dependencies
python plhub.py install --force

# Check dependency conflicts
python plhub.py doctor --check-deps
```

### Runtime Issues

```bash
# Run with verbose logging
python plhub.py run src/main.poh --verbose

# Enable debug mode
python plhub.py run src/main.poh --debug

# Check runtime version
python plhub.py doctor --check-runtime
```

---

## Resources

- **Documentation**: [docs/README.md](README.md)
- **Examples**: [Examples/](../Examples/)
- **Templates**: [templates/](../templates/)
- **Community**: https://community.pohlang.org
- **Support**: support@pohlang.org

---

## Summary

This guide covered:

✅ **Complete workflows** for all application types  
✅ **Step-by-step instructions** from creation to deployment  
✅ **Real-world examples** with full source code  
✅ **Best practices** for production applications  
✅ **Testing strategies** for quality assurance  
✅ **Build and packaging** for distribution  
✅ **Deployment options** for all platforms  

**You now have everything needed to build complete, production-ready applications with PohLang and PLHub!** 🚀
