# PLHub Cross-Platform Development Guide

Complete guide to building PohLang applications for Android, iOS, macOS, Windows, and Web with hot reload, testing, and deployment support.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Platform Setup](#platform-setup)
3. [Project Creation](#project-creation)
4. [Building & Running](#building--running)
5. [Hot Reload Development](#hot-reload-development)
6. [Testing](#testing)
7. [Device Management](#device-management)
8. [Deployment](#deployment)
9. [Platform-Specific Guides](#platform-specific-guides)
10. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Create Your First Cross-Platform App

```bash
# Android
python plhub.py platform create android MyApp
cd MyApp
python plhub.py platform run android --hot-reload

# iOS (macOS only)
python plhub.py platform create ios MyApp
cd MyApp
python plhub.py platform run ios --hot-reload

# macOS (macOS only)
python plhub.py platform create macos MyApp
cd MyApp
python plhub.py platform run macos --hot-reload

# Windows
python plhub.py platform create windows MyApp
cd MyApp
python plhub.py platform run windows --hot-reload

# Web
python plhub.py platform create web MyApp
cd MyApp
python plhub.py platform run web --hot-reload
```

---

## Platform Setup

### Android Setup

**Requirements:**
- Java JDK 11 or higher
- Android Studio (latest stable)
- Android SDK (API 24+)
- Android SDK Build Tools
- Android Emulator or physical device

**Installation:**
```bash
# Install Android Studio
# https://developer.android.com/studio

# Set environment variables (add to ~/.bashrc or ~/.zshrc)
export ANDROID_HOME=$HOME/Android/Sdk
export PATH=$PATH:$ANDROID_HOME/emulator
export PATH=$PATH:$ANDROID_HOME/tools
export PATH=$PATH:$ANDROID_HOME/platform-tools

# Verify installation
adb version
emulator -list-avds
```

**Create Emulator:**
```bash
# Open Android Studio > Tools > Device Manager
# Or use command line:
avdmanager create avd -n Pixel_5 -k "system-images;android-33;google_apis;x86_64"
```

---

### iOS Setup (macOS only)

**Requirements:**
- macOS 13.0 or later
- Xcode 15 or later
- iOS Simulator
- Apple Developer Account (for physical device testing)

**Installation:**
```bash
# Install Xcode from App Store
# Install Command Line Tools
xcode-select --install

# Accept license
sudo xcodebuild -license accept

# Verify installation
xcodebuild -version
xcrun simctl list devices
```

---

### macOS Setup

**Requirements:**
- macOS 13.0 or later
- Xcode 15 or later

**Installation:**
Same as iOS setup above.

---

### Windows Setup

**Requirements:**
- Windows 10/11
- Visual Studio 2022 with:
  - .NET Desktop Development workload
  - Windows App SDK (WinUI3)
- .NET 8.0 SDK

**Installation:**
```powershell
# Install Visual Studio 2022 Community
# https://visualstudio.microsoft.com/

# Install .NET SDK
# https://dotnet.microsoft.com/download

# Verify installation
dotnet --version
```

---

### Web Setup

**Requirements:**
- Node.js 18+ and npm
- Modern web browser (Chrome, Firefox, Safari, Edge)

**Installation:**
```bash
# Install Node.js
# https://nodejs.org/

# Verify installation
node --version
npm --version
```

---

## Project Creation

### Basic Project Creation

```bash
# Create project
python plhub.py platform create <platform> <ProjectName>

# With custom package name (Android/iOS)
python plhub.py platform create android MyApp --package com.example.myapp

# Custom output directory
python plhub.py platform create web MyApp --output ~/projects/
```

### Project Structure

#### Android Project
```
MyApp/
├── app/
│   ├── src/
│   │   ├── main/
│   │   │   ├── poh/                  # PohLang source files
│   │   │   │   ├── MainActivity.poh
│   │   │   │   └── App.poh
│   │   │   ├── res/                  # Resources
│   │   │   └── AndroidManifest.xml
│   │   ├── test/                     # Unit tests
│   │   └── androidTest/              # Instrumented tests
│   └── build.gradle
├── gradle/
├── build.gradle
└── settings.gradle
```

#### iOS Project
```
MyApp/
├── MyApp/
│   ├── App/
│   │   ├── MyAppApp.poh          # App entry point
│   │   ├── AppDelegate.poh
│   │   └── SceneDelegate.poh
│   ├── Views/
│   │   ├── ContentView.poh       # Main UI
│   │   └── MainViewController.poh
│   ├── Services/
│   │   └── HotReloadService.poh  # Hot reload support
│   └── Resources/
│       ├── Assets.xcassets
│       └── Info.plist
├── MyAppTests/
└── MyApp.xcodeproj/
```

#### macOS Project
```
MyApp/
├── MyApp/
│   ├── App/
│   │   ├── MyAppApp.poh
│   │   └── AppDelegate.poh
│   ├── Views/
│   │   ├── ContentView.poh
│   │   └── MainWindow.poh
│   └── Resources/
│       └── MyApp.entitlements
└── MyApp.xcodeproj/
```

#### Windows Project
```
MyApp/
├── MyApp/
│   ├── App.poh
│   ├── MainWindow.poh
│   ├── Views/
│   │   ├── HomePage.poh
│   │   └── SettingsPage.poh
│   ├── Services/
│   │   └── HotReloadService.poh
│   └── Package.appxmanifest
└── MyApp.Tests/
```

#### Web Project
```
MyApp/
├── public/
│   ├── index.html
│   ├── manifest.json
│   └── assets/
├── src/
│   ├── App.poh              # Main app component
│   ├── main.poh             # Entry point
│   ├── components/
│   │   ├── Header.poh
│   │   └── Footer.poh
│   ├── pages/
│   │   ├── Home.poh
│   │   └── About.poh
│   ├── services/
│   │   ├── api.poh
│   │   └── hotreload.poh
│   └── styles/
├── tests/
├── package.json
└── webpack.config.js
```

---

## Building & Running

### Build Commands

```bash
# Debug build
python plhub.py platform build <platform>

# Release build
python plhub.py platform build <platform> --config release

# Specify project directory
python plhub.py platform build android --project-dir ~/MyApp

# Platform-specific examples
python plhub.py platform build android --config debug
python plhub.py platform build ios --config release
python plhub.py platform build windows --config debug
python plhub.py platform build web --config release
```

### Run Commands

```bash
# Run on default device
python plhub.py platform run <platform>

# Run on specific device
python plhub.py platform run android --device emulator-5554
python plhub.py platform run ios --device "iPhone 15"

# Run with hot reload
python plhub.py platform run web --hot-reload

# Specify project directory
python plhub.py platform run macos --project-dir ~/MyApp
```

### Device Selection

```bash
# List all devices
python plhub.py platform devices

# List platform-specific devices
python plhub.py platform devices --platform android
python plhub.py platform devices --platform ios
python plhub.py platform devices --platform web
```

---

## Hot Reload Development

Hot reload allows you to see code changes instantly without restarting your app.

### Enable Hot Reload

```bash
# Run with hot reload flag
python plhub.py platform run <platform> --hot-reload
```

### How It Works

1. **File Watching**: PLHub watches for changes to `.poh` files in your project
2. **Change Detection**: When files are saved, changes are detected within 0.5 seconds
3. **Reload Trigger**: Updated code is sent to the running app
4. **State Preservation**: (Platform-dependent) App state may be preserved during reload

### Platform-Specific Behavior

| Platform | Strategy | State Preservation |
|----------|----------|-------------------|
| **Android** | Incremental | Partial (Activity state) |
| **iOS** | State-Preserve | Yes (View state) |
| **macOS** | State-Preserve | Yes (Window state) |
| **Windows** | Module-Replace | Partial (ViewModel state) |
| **Web** | Module-Replace | Yes (Component state) |

### Hot Reload Configuration

The hot reload server runs on port `8765` by default.

**Firewall Configuration:**
```bash
# Allow hot reload port (if needed)
# Windows
netsh advfirewall firewall add rule name="PLHub Hot Reload" dir=in action=allow protocol=TCP localport=8765

# macOS
# System Preferences > Security & Privacy > Firewall > Firewall Options
# Add exception for Python

# Linux
sudo ufw allow 8765/tcp
```

### Debugging Hot Reload

```bash
# Check hot reload connection
# Server logs will show connected clients

# Android: Check logcat
adb logcat | grep "HotReload"

# iOS: Check console
xcrun simctl spawn booted log stream --predicate 'process == "MyApp"'

# Web: Check browser console
# Open Developer Tools (F12) > Console
```

---

## Testing

PLHub supports comprehensive testing for all platforms.

### Test Types

1. **Unit Tests**: Test individual functions/classes
2. **Integration Tests**: Test component interactions
3. **UI Tests**: Test user interface (iOS/Android)
4. **E2E Tests**: End-to-end testing (Web)

### Run Tests

```bash
# Run all unit tests
python plhub.py platform test <platform>

# Run specific test type
python plhub.py platform test android --type unit
python plhub.py platform test ios --type ui
python plhub.py platform test web --type e2e

# Filter tests by pattern
python plhub.py platform test android --pattern "LoginTest"

# Specify project directory
python plhub.py platform test windows --project-dir ~/MyApp
```

### Platform-Specific Testing

#### Android Testing
```bash
# Unit tests (JUnit)
python plhub.py platform test android --type unit

# Instrumented tests (Espresso)
python plhub.py platform test android --type integration

# Both
python plhub.py platform test android
```

#### iOS/macOS Testing
```bash
# XCTest framework
python plhub.py platform test ios --type unit
python plhub.py platform test macos --type ui
```

#### Windows Testing
```bash
# MSTest framework
python plhub.py platform test windows --type unit
```

#### Web Testing
```bash
# Jest/Vitest unit tests
python plhub.py platform test web --type unit

# E2E tests (Playwright/Cypress)
python plhub.py platform test web --type e2e
```

### Test Results

Results are automatically saved to `test_results/` directory:

```
MyApp/
└── test_results/
    ├── android_20250105_143022.json
    ├── ios_20250105_143055.json
    └── web_20250105_143120.json
```

Results include:
- Total test count
- Passed/Failed/Skipped counts
- Duration
- Success rate
- Individual test details

---

## Device Management

### List Devices

```bash
# All platforms
python plhub.py platform devices

# Specific platform
python plhub.py platform devices --platform android
python plhub.py platform devices --platform ios
```

### Launch Emulators/Simulators

```bash
# Android emulator
python plhub.py platform launch android "Pixel_5_API_33"

# iOS simulator
python plhub.py platform launch ios "iPhone 15"

# Web browser
python plhub.py platform launch web chrome
```

### Android Device Management

```bash
# List Android devices
adb devices -l

# List emulators
emulator -list-avds

# Launch emulator
python plhub.py platform launch android "Pixel_5"

# Install APK
python plhub.py platform run android --device emulator-5554

# View logs
adb logcat
```

### iOS Device Management

```bash
# List simulators
xcrun simctl list devices

# Launch simulator
python plhub.py platform launch ios "iPhone 15"

# Install app on simulator
python plhub.py platform run ios --device "iPhone 15"

# View logs
xcrun simctl spawn booted log stream
```

---

## Deployment

### Android Deployment

```bash
# Build release APK
python plhub.py platform build android --config release

# Build release bundle (for Play Store)
python plhub.py platform deploy android playstore --project-dir ~/MyApp

# Output location
# MyApp/app/build/outputs/apk/release/app-release.apk
# MyApp/app/build/outputs/bundle/release/app-release.aab
```

**Google Play Store Steps:**
1. Create developer account at https://play.google.com/console
2. Create app listing
3. Upload AAB file
4. Complete store listing
5. Submit for review

---

### iOS Deployment

```bash
# Build release archive
python plhub.py platform deploy ios appstore --project-dir ~/MyApp

# Output location
# MyApp/build/MyApp.xcarchive
```

**App Store Steps:**
1. Enroll in Apple Developer Program
2. Create App ID in Developer Portal
3. Create app in App Store Connect
4. Upload archive via Xcode or Transporter
5. Submit for review

---

### macOS Deployment

```bash
# Build release
python plhub.py platform build macos --config release

# Create DMG (manual)
# Or use packaging tools
```

---

### Windows Deployment

```bash
# Build release
python plhub.py platform build windows --config release

# Create installer (manual)
# Or publish to Microsoft Store

# Output location
# MyApp/bin/Release/net8.0-windows/win-x64/
```

**Microsoft Store Steps:**
1. Create developer account
2. Reserve app name
3. Package app (MSIX)
4. Upload and submit

---

### Web Deployment

```bash
# Build production bundle
python plhub.py platform build web --config release

# Deploy to server
python plhub.py platform deploy web netlify
python plhub.py platform deploy web vercel

# Output location
# MyApp/dist/
```

**Deployment Options:**
- **Static Hosting**: Netlify, Vercel, GitHub Pages, AWS S3
- **Cloud Platforms**: Heroku, Firebase Hosting, Azure
- **Custom Server**: nginx, Apache, Node.js server

---

## Platform-Specific Guides

### Android Best Practices

1. **Permissions**: Declare in AndroidManifest.xml
2. **Resources**: Use density-specific assets (hdpi, xhdpi, xxhdpi)
3. **Themes**: Support dark mode
4. **Lifecycle**: Handle Activity lifecycle properly
5. **Testing**: Test on multiple API levels

### iOS Best Practices

1. **Safe Areas**: Respect device safe areas
2. **Dark Mode**: Support both light and dark appearances
3. **Localization**: Use Localizable.strings
4. **Privacy**: Request permissions with NSUsageDescription
5. **Testing**: Test on multiple device sizes

### macOS Best Practices

1. **Menu Bar**: Implement proper menu structure
2. **Window Management**: Handle multiple windows
3. **Sandboxing**: Enable App Sandbox for store distribution
4. **Entitlements**: Declare required capabilities
5. **Testing**: Test on different macOS versions

### Windows Best Practices

1. **WinUI3**: Use modern UI controls
2. **Themes**: Support system theme (light/dark)
3. **Packaging**: Use MSIX for distribution
4. **Notifications**: Implement proper toast notifications
5. **Testing**: Test on Windows 10 and 11

### Web Best Practices

1. **Responsive Design**: Support mobile and desktop
2. **Performance**: Optimize bundle size
3. **SEO**: Meta tags and semantic HTML
4. **Accessibility**: WCAG compliance
5. **Testing**: Cross-browser testing

---

## Troubleshooting

### Common Issues

#### Android

**Problem**: "SDK not found"
```bash
# Solution: Set ANDROID_HOME
export ANDROID_HOME=$HOME/Android/Sdk
export PATH=$PATH:$ANDROID_HOME/platform-tools
```

**Problem**: "Emulator won't start"
```bash
# Solution: Check virtualization
# Windows: Enable Hyper-V or HAXM
# Mac: No action needed
# Linux: Enable KVM
```

**Problem**: "App crashes on startup"
```bash
# Solution: Check logcat
adb logcat | grep "MyApp"
```

#### iOS

**Problem**: "Code signing error"
```bash
# Solution: Select development team in Xcode
# Or disable signing for simulator builds
```

**Problem**: "Simulator not found"
```bash
# Solution: List available simulators
xcrun simctl list devices
# Create new simulator if needed
```

#### Windows

**Problem**: ".NET SDK not found"
```bash
# Solution: Install .NET 8.0 SDK
# https://dotnet.microsoft.com/download
```

**Problem**: "Build fails"
```bash
# Solution: Restore NuGet packages
dotnet restore
```

#### Web

**Problem**: "Module not found"
```bash
# Solution: Install dependencies
npm install
```

**Problem**: "Hot reload not working"
```bash
# Solution: Check dev server is running
# Check firewall allows port 8080
```

### Getting Help

1. **Documentation**: https://github.com/AlhaqGH/PohLang/wiki
2. **Issues**: https://github.com/AlhaqGH/PohLang/issues
3. **Discord**: [Join our community]
4. **Stack Overflow**: Tag `pohlang`

---

## Advanced Topics

### Custom Build Configuration

Create platform-specific configuration files:

**Android**: `app/build.gradle`
**iOS**: `project.pbxproj`
**Windows**: `MyApp.csproj`
**Web**: `webpack.config.js`

### Performance Optimization

1. **Android**: Enable ProGuard/R8
2. **iOS**: Enable bitcode
3. **Windows**: Ahead-of-time compilation
4. **Web**: Code splitting, lazy loading

### CI/CD Integration

```yaml
# Example: GitHub Actions
name: Build and Test
on: [push]
jobs:
  android:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build
        run: python plhub.py platform build android
      - name: Test
        run: python plhub.py platform test android
```

---

## Quick Reference

### Essential Commands

```bash
# Create
python plhub.py platform create <platform> <name>

# Build
python plhub.py platform build <platform>

# Run
python plhub.py platform run <platform> --hot-reload

# Test
python plhub.py platform test <platform>

# Deploy
python plhub.py platform deploy <platform> <target>

# Devices
python plhub.py platform devices
python plhub.py platform launch <platform> <device>
```

### Supported Platforms

- ✅ Android (API 24+)
- ✅ iOS (15.0+)
- ✅ macOS (13.0+)
- ✅ Windows (10/11)
- ✅ Web (Modern browsers)

---

**Version**: PLHub v0.5.0
**Last Updated**: October 5, 2025
**License**: MIT
