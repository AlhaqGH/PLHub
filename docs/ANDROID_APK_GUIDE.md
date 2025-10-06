# Android APK Building Guide for PohLang

Complete guide to building Android APK files from PohLang applications.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Android Project Setup](#android-project-setup)
- [Building APKs](#building-apks)
- [APK Configuration](#apk-configuration)
- [Signing and Release](#signing-and-release)
- [Installation and Testing](#installation-and-testing)
- [Troubleshooting](#troubleshooting)
- [Advanced Topics](#advanced-topics)

## 🔧 Prerequisites

### Required Software

1. **Java Development Kit (JDK) 11 or higher**
   ```bash
   java -version
   ```

2. **Android SDK** (via Android Studio)
   - Download from: https://developer.android.com/studio
   - Install Android SDK Platform-Tools
   - Set `ANDROID_HOME` environment variable

3. **Gradle Build Tool**
   - Bundled with Android Studio
   - Or install separately: https://gradle.org/

### Environment Setup

#### Windows (PowerShell)
```powershell
# Set Android SDK path
$env:ANDROID_HOME = "C:\Users\YourName\AppData\Local\Android\Sdk"
$env:PATH += ";$env:ANDROID_HOME\platform-tools"
```

#### Linux/macOS
```bash
export ANDROID_HOME=$HOME/Android/Sdk
export PATH=$PATH:$ANDROID_HOME/platform-tools
```

### Verify Installation

```bash
# Check Java
java -version

# Check Android SDK
adb version

# Check Gradle (if installed)
gradle --version
```

## 🚀 Quick Start

### 1. Create Android Project

Create a new PohLang project configured for Android:

```bash
cd PLHub
python plhub.py new android-app --template android
cd android-app
```

Or convert existing project:

```bash
cd your-pohlang-project
python ../PLHub/plhub.py android init
```

### 2. Build Debug APK

```bash
# Build debug APK (unsigned, for testing)
python ../PLHub/plhub.py build android

# Or using Android APK builder directly
python ../PLHub/tools/android_apk_builder.py .
```

### 3. Build Release APK

```bash
# Build release APK (optimized)
python ../PLHub/plhub.py build android --release

# Specify output location
python ../PLHub/plhub.py build android --release -o MyApp.apk
```

### 4. Install on Device

```bash
# Install APK on connected device/emulator
adb install build/android/android-app-debug.apk

# Or use PLHub
python ../PLHub/plhub.py run android
```

## 📦 Android Project Setup

### Project Structure

```
your-android-app/
├── plhub.json              # Project configuration
├── src/
│   └── main.poh            # Main PohLang entry point
├── assets/                 # App assets (images, etc.)
│   ├── icon.png
│   └── splash.png
├── android/                # Generated Android project
│   ├── app/
│   │   ├── src/
│   │   │   └── main/
│   │   │       ├── java/
│   │   │       ├── res/
│   │   │       └── AndroidManifest.xml
│   │   └── build.gradle
│   ├── build.gradle
│   └── settings.gradle
└── build/
    └── android/
        └── your-app.apk    # Output APK
```

### plhub.json Configuration

```json
{
  "name": "my-android-app",
  "version": "1.0.0",
  "type": "android",
  "description": "My Android app built with PohLang",
  
  "target": {
    "platform": "android",
    "minSdk": 24,
    "targetSdk": 34,
    "compileSdk": 34
  },
  
  "android": {
    "package_name": "com.yourcompany.myapp",
    "app_name": "My App",
    "icon": "assets/icon.png",
    "splash": "assets/splash.png",
    
    "permissions": [
      "INTERNET",
      "ACCESS_NETWORK_STATE",
      "CAMERA",
      "ACCESS_FINE_LOCATION"
    ],
    
    "orientation": "portrait",
    "theme": "AppCompat.Light.DarkActionBar"
  },
  
  "build": {
    "sourceDir": "src",
    "outputDir": "build/android",
    "entry": "src/main.poh"
  }
}
```

## 🔨 Building APKs

### Debug Build

Debug builds are for development and testing:

```bash
# Basic debug build
python plhub.py build android

# With verbose output
python plhub.py build android --verbose

# Specify output location
python plhub.py build android -o dist/app-debug.apk
```

**Debug build features:**
- No code optimization
- Includes debugging symbols
- Self-signed with debug certificate
- Larger file size
- Instant Run support

### Release Build

Release builds are optimized for distribution:

```bash
# Build release APK
python plhub.py build android --release

# With custom output
python plhub.py build android --release -o releases/myapp-v1.0.0.apk
```

**Release build features:**
- Code optimization (ProGuard/R8)
- No debugging symbols
- Smaller file size
- Must be signed for distribution

### Build Modes Comparison

| Feature | Debug | Release |
|---------|-------|---------|
| Optimization | None | Full |
| Debugging | Enabled | Disabled |
| Size | Larger | Smaller |
| Performance | Slower | Faster |
| Signing | Debug cert | Production cert |
| Distribution | Testing only | Google Play ready |

## ⚙️ APK Configuration

### Package Name

The package name uniquely identifies your app:

```json
{
  "android": {
    "package_name": "com.yourcompany.appname"
  }
}
```

**Requirements:**
- Lowercase letters, numbers, underscores
- Must contain at least one dot
- Starts with letter
- Example: `com.example.myapp`

### App Permissions

Declare required permissions in `plhub.json`:

```json
{
  "android": {
    "permissions": [
      "INTERNET",                  // Network access
      "ACCESS_NETWORK_STATE",      // Check network status
      "CAMERA",                    // Camera access
      "ACCESS_FINE_LOCATION",      // GPS location
      "ACCESS_COARSE_LOCATION",    // Network location
      "RECORD_AUDIO",              // Microphone access
      "READ_EXTERNAL_STORAGE",     // Read files
      "WRITE_EXTERNAL_STORAGE",    // Write files
      "VIBRATE",                   // Vibration
      "POST_NOTIFICATIONS"         // Show notifications (Android 13+)
    ]
  }
}
```

### Version Configuration

```json
{
  "version": "1.2.3",
  "android": {
    "versionCode": 10203
  }
}
```

**Version Code Rules:**
- Increment for each release
- Must be integer
- Google Play requires increasing codes
- Convention: `major * 10000 + minor * 100 + patch`
  - v1.2.3 → 10203
  - v2.0.0 → 20000

### App Icon

Provide app icons in different resolutions:

```
assets/
├── icon-mdpi.png      (48x48)
├── icon-hdpi.png      (72x72)
├── icon-xhdpi.png     (96x96)
├── icon-xxhdpi.png    (144x144)
└── icon-xxxhdpi.png   (192x192)
```

Or use single icon:
```json
{
  "android": {
    "icon": "assets/icon.png"
  }
}
```

### Splash Screen

```json
{
  "android": {
    "splash": "assets/splash.png",
    "splash_duration": 2000
  }
}
```

## 🔐 Signing and Release

### Generate Keystore

Create a keystore for signing release APKs:

```bash
# Generate keystore
keytool -genkey -v -keystore my-release-key.jks \
  -alias my-app-key \
  -keyalg RSA -keysize 2048 -validity 10000

# You'll be prompted for:
# - Keystore password
# - Key password
# - Personal information
```

**⚠️ Important:**
- Keep keystore file secure
- Remember passwords
- Backup keystore (cannot be recovered if lost)

### Sign Release APK

```bash
# Build unsigned release APK
python plhub.py build android --release

# Sign APK
jarsigner -verbose -sigalg SHA256withRSA -digestalg SHA-256 \
  -keystore my-release-key.jks \
  build/android/app-release.apk \
  my-app-key

# Verify signature
jarsigner -verify -verbose -certs \
  build/android/app-release.apk
```

### Optimize APK (zipalign)

```bash
# Align APK for optimal loading
zipalign -v 4 \
  build/android/app-release.apk \
  build/android/app-release-aligned.apk
```

### Complete Release Process

```bash
# 1. Build release APK
python plhub.py build android --release

# 2. Sign APK
jarsigner -keystore my-release-key.jks \
  build/android/app-release.apk my-app-key

# 3. Optimize APK
zipalign -f -v 4 \
  build/android/app-release.apk \
  build/android/app-release-final.apk

# 4. Verify
apksigner verify build/android/app-release-final.apk
```

## 📲 Installation and Testing

### Install on Physical Device

1. **Enable Developer Options on device:**
   - Go to Settings > About Phone
   - Tap "Build Number" 7 times
   - Go back to Settings > System > Developer Options
   - Enable "USB Debugging"

2. **Connect device via USB**

3. **Install APK:**
   ```bash
   # List connected devices
   adb devices
   
   # Install APK
   adb install build/android/app-debug.apk
   
   # Reinstall (update existing app)
   adb install -r build/android/app-debug.apk
   ```

### Install on Emulator

```bash
# Start emulator
emulator -avd Pixel_6_API_34

# Install APK
adb install build/android/app-debug.apk
```

### Run and Debug

```bash
# Install and launch
adb install -r build/android/app-debug.apk
adb shell am start -n com.yourpackage.name/.MainActivity

# View logs
adb logcat | grep "YourAppTag"

# Clear app data
adb shell pm clear com.yourpackage.name

# Uninstall
adb uninstall com.yourpackage.name
```

## 🔍 Troubleshooting

### Build Failures

#### "ANDROID_HOME not set"
```bash
# Windows
$env:ANDROID_HOME = "C:\Users\YourName\AppData\Local\Android\Sdk"

# Linux/macOS
export ANDROID_HOME=$HOME/Android/Sdk
```

#### "Java version incompatible"
```bash
# Check Java version
java -version

# Install JDK 11 or higher
# Download from: https://adoptium.net/
```

#### "Gradle build failed"
```bash
# Clean Gradle cache
cd android
./gradlew clean

# Or delete build directories
rm -rf android/app/build
rm -rf android/build
```

#### "SDK licenses not accepted"
```bash
# Accept all SDK licenses
$ANDROID_HOME/tools/bin/sdkmanager --licenses
```

### APK Installation Failures

#### "App not installed"
```bash
# Uninstall existing version
adb uninstall com.yourpackage.name

# Reinstall
adb install build/android/app-debug.apk
```

#### "INSTALL_PARSE_FAILED_NO_CERTIFICATES"
```bash
# APK not signed properly
# For debug: rebuild
python plhub.py build android

# For release: sign APK
jarsigner -keystore my-key.jks app.apk my-alias
```

#### "INSTALL_FAILED_INSUFFICIENT_STORAGE"
```bash
# Clear space on device
adb shell pm list packages | grep yourapp
adb shell pm clear com.yourpackage.name
```

### Runtime Issues

#### App Crashes on Launch
```bash
# View crash logs
adb logcat -v time > crash.log

# Look for stack traces
adb logcat | grep "AndroidRuntime"
```

#### Permission Denied Errors
```bash
# Check manifest has permissions
# Rebuild APK after adding permissions to plhub.json
python plhub.py build android
```

## 🔬 Advanced Topics

### Multi-APK Architecture

Generate separate APKs for different architectures:

```json
{
  "android": {
    "abi_filters": ["armeabi-v7a", "arm64-v8a", "x86", "x86_64"],
    "split_apks": true
  }
}
```

### Android App Bundle (AAB)

Build AAB for Google Play:

```bash
# Build AAB (not yet implemented)
python plhub.py build android --bundle
```

### ProGuard/R8 Optimization

Configure code shrinking:

```json
{
  "android": {
    "minify": true,
    "proguard_rules": [
      "-keep class com.yourpackage.** { *; }",
      "-dontwarn javax.annotation.**"
    ]
  }
}
```

### Native Libraries

Include native libraries:

```json
{
  "android": {
    "native_libs": {
      "armeabi-v7a": ["libs/armeabi-v7a/libmylib.so"],
      "arm64-v8a": ["libs/arm64-v8a/libmylib.so"]
    }
  }
}
```

### Build Variants

Define custom build variants:

```json
{
  "android": {
    "build_variants": {
      "free": {
        "package_suffix": ".free",
        "app_name": "My App Free"
      },
      "premium": {
        "package_suffix": ".premium",
        "app_name": "My App Premium"
      }
    }
  }
}
```

## 📚 Additional Resources

### Official Documentation
- [Android Developer Guide](https://developer.android.com/guide)
- [Android Studio](https://developer.android.com/studio)
- [Gradle Build Tool](https://gradle.org/guides/)

### PohLang Resources
- [PohLang Guide](../PohLang_Guide.md)
- [Complete App Building Guide](COMPLETE_APP_GUIDE.md)
- [Platform Builder Reference](../tools/platform_builder.py)

### Tutorials
- [Publishing on Google Play](https://developer.android.com/studio/publish)
- [App Signing](https://developer.android.com/studio/publish/app-signing)
- [Testing on Devices](https://developer.android.com/studio/run/device)

## 🎯 Next Steps

1. **Build your first Android APK:**
   ```bash
   python plhub.py new android-hello
   cd android-hello
   python ../plhub.py build android
   ```

2. **Test on device:**
   ```bash
   adb install build/android/android-hello-debug.apk
   ```

3. **Prepare for release:**
   - Create keystore
   - Build release APK
   - Sign and optimize
   - Test thoroughly

4. **Publish to Google Play:**
   - Create developer account
   - Prepare store listing
   - Upload APK/AAB
   - Release to production

---

**🎉 You're ready to build Android apps with PohLang!**

For more help:
- Check [Troubleshooting](#troubleshooting) section
- Visit PohLang documentation
- Join community forums
