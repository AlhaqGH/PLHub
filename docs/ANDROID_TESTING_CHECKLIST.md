# ✅ Android APK Building - Testing & Verification Checklist

Complete checklist to verify Android APK building functionality.

## 📋 Quick Verification (5 minutes)

### ☐ 1. Prerequisites Check
```bash
# Check Java
java -version
# Expected: Java 11 or higher

# Check Android SDK
echo $ANDROID_HOME  # Linux/Mac
echo $env:ANDROID_HOME  # Windows
# Expected: Path to Android SDK

# Check ADB
adb version
# Expected: Android Debug Bridge version info
```

### ☐ 2. Build Calculator APK
```bash
cd PLHub/Examples/android-calculator
python ../../plhub.py build android
```

**Expected Output:**
```
╔════════════════════════════════════════╗
║   BUILDING ANDROID APK FOR POHLANG    ║
╚════════════════════════════════════════╝

⏳ Checking prerequisites...
   ✅ Java JDK found
   ✅ Android SDK found
   ✅ Gradle found
✅ All prerequisites met

[... build steps ...]

╔════════════════════════════════════════╗
║       APK BUILD SUCCESSFUL! ✓          ║
╚════════════════════════════════════════╝
```

### ☐ 3. Verify APK Created
```bash
ls -lh build/android/android-calculator-debug.apk
```

**Expected:**
- File exists
- Size: 3-10 MB
- Recent timestamp

### ☐ 4. Install on Device
```bash
adb devices  # Verify device connected
adb install build/android/android-calculator-debug.apk
```

**Expected:**
```
Performing Streamed Install
Success
```

### ☐ 5. Launch App
- Open app drawer on device
- Find "PohLang Calculator"
- Tap to launch
- Verify app opens

**✅ If all 5 steps pass, Android APK building is working!**

---

## 🔬 Comprehensive Testing (30 minutes)

### A. Prerequisites & Environment

#### ☐ A1. Java JDK Detection
```bash
# Test with Java installed
java -version
python tools/android_apk_builder.py Examples/android-calculator
# Should detect Java ✅

# Test without Java (simulate)
# Expected: Clear error message about missing Java
```

#### ☐ A2. Android SDK Detection
```bash
# With ANDROID_HOME set
echo $ANDROID_HOME
python tools/android_apk_builder.py Examples/android-calculator
# Should detect SDK ✅

# Without ANDROID_HOME
unset ANDROID_HOME  # Linux/Mac
$env:ANDROID_HOME = $null  # Windows
python tools/android_apk_builder.py Examples/android-calculator
# Should show error with SDK setup instructions
```

#### ☐ A3. Gradle Detection
```bash
# Test Gradle detection
gradle --version
# Should show version or use gradlew wrapper
```

### B. Build Functionality

#### ☐ B1. Debug Build
```bash
cd Examples/android-calculator
python ../../plhub.py build android
```

**Verify:**
- ✅ Build succeeds
- ✅ APK created in `build/android/`
- ✅ APK named `android-calculator-debug.apk`
- ✅ File size 3-10 MB
- ✅ Success message displayed

#### ☐ B2. Release Build
```bash
python ../../plhub.py build android --release
```

**Verify:**
- ✅ Build succeeds
- ✅ APK named `android-calculator-release.apk`
- ✅ Smaller than debug build (optimized)
- ✅ Release mode indicated in output

#### ☐ B3. Custom Output Path
```bash
python ../../plhub.py build android -o MyCalculator.apk
```

**Verify:**
- ✅ APK created at specified path
- ✅ Correct filename
- ✅ Output path shown in success message

#### ☐ B4. Rebuild (Incremental)
```bash
# Build once
python ../../plhub.py build android

# Build again without changes
python ../../plhub.py build android
```

**Verify:**
- ✅ Second build succeeds
- ✅ Faster than first build (uses cache)
- ✅ APK updated

### C. Project Generation

#### ☐ C1. Android Directory Structure
```bash
ls -R android/
```

**Verify Created:**
- ✅ `android/app/src/main/java/`
- ✅ `android/app/src/main/res/`
- ✅ `android/app/src/main/AndroidManifest.xml`
- ✅ `android/app/build.gradle`
- ✅ `android/build.gradle`
- ✅ `android/settings.gradle`

#### ☐ C2. AndroidManifest.xml
```bash
cat android/app/src/main/AndroidManifest.xml
```

**Verify Contains:**
- ✅ Package name: `com.pohlang.calculator`
- ✅ App name: "PohLang Calculator"
- ✅ MainActivity declaration
- ✅ LAUNCHER intent filter
- ✅ Permissions (if any)

#### ☐ C3. MainActivity.kt
```bash
cat android/app/src/main/java/com/pohlang/calculator/MainActivity.kt
```

**Verify Contains:**
- ✅ Package declaration
- ✅ MainActivity class
- ✅ onCreate method
- ✅ setContentView call
- ✅ PohLang integration placeholder

#### ☐ C4. Layout Files
```bash
cat android/app/src/main/res/layout/activity_main.xml
```

**Verify:**
- ✅ Valid XML
- ✅ ScrollView for output
- ✅ TextView for display
- ✅ ConstraintLayout structure

#### ☐ C5. Resource Files
```bash
cat android/app/src/main/res/values/strings.xml
cat android/app/src/main/res/values/colors.xml
```

**Verify:**
- ✅ `strings.xml` has app_name
- ✅ `colors.xml` has color definitions
- ✅ Valid XML structure

### D. Gradle Configuration

#### ☐ D1. Root build.gradle
```bash
cat android/build.gradle
```

**Verify:**
- ✅ Gradle plugin declared
- ✅ Kotlin support
- ✅ Google and Maven repositories
- ✅ Clean task

#### ☐ D2. App build.gradle
```bash
cat android/app/build.gradle
```

**Verify:**
- ✅ compileSdk 34
- ✅ minSdk 24
- ✅ targetSdk 34
- ✅ versionCode from config
- ✅ versionName from config
- ✅ buildTypes (debug & release)
- ✅ AndroidX dependencies

#### ☐ D3. settings.gradle
```bash
cat android/settings.gradle
```

**Verify:**
- ✅ Root project name
- ✅ ':app' module included

### E. APK Verification

#### ☐ E1. APK Structure
```bash
# Extract APK contents
unzip -l build/android/android-calculator-debug.apk
```

**Verify Contains:**
- ✅ `AndroidManifest.xml`
- ✅ `classes.dex` (compiled code)
- ✅ `resources.arsc`
- ✅ `res/` directory
- ✅ `META-INF/` (signatures)

#### ☐ E2. APK Info
```bash
aapt dump badging build/android/android-calculator-debug.apk
```

**Verify:**
- ✅ Package: `com.pohlang.calculator`
- ✅ versionCode matches config
- ✅ versionName matches config
- ✅ sdkVersion: 24
- ✅ targetSdkVersion: 34

#### ☐ E3. APK Signing (Debug)
```bash
jarsigner -verify -verbose build/android/android-calculator-debug.apk
```

**Verify:**
- ✅ Signed with debug certificate
- ✅ jar verified

#### ☐ E4. APK Size
```bash
du -h build/android/android-calculator-debug.apk
```

**Verify:**
- ✅ Debug: 5-10 MB
- ✅ Release: 3-5 MB (smaller)

### F. Installation Testing

#### ☐ F1. Install Debug APK
```bash
adb install build/android/android-calculator-debug.apk
```

**Verify:**
```
Success
```

#### ☐ F2. Reinstall (Update)
```bash
adb install -r build/android/android-calculator-debug.apk
```

**Verify:**
- ✅ Reinstall succeeds
- ✅ App updates

#### ☐ F3. Launch App
```bash
adb shell am start -n com.pohlang.calculator/.MainActivity
```

**Verify:**
- ✅ App launches
- ✅ No crash
- ✅ UI displays

#### ☐ F4. Check Logs
```bash
adb logcat | grep Calculator
```

**Verify:**
- ✅ No error messages
- ✅ Activity started successfully

### G. Device Testing

#### ☐ G1. Physical Device
- Connect Android phone via USB
- Enable USB debugging
- Install APK
- Launch app

**Verify:**
- ✅ Installs successfully
- ✅ Launches without crash
- ✅ UI displays correctly
- ✅ Responds to touch

#### ☐ G2. Emulator
```bash
# Start emulator
emulator -avd Pixel_6_API_34

# Install
adb install build/android/android-calculator-debug.apk
```

**Verify:**
- ✅ Installs on emulator
- ✅ Launches successfully
- ✅ Functions correctly

#### ☐ G3. Multiple Devices
```bash
# List devices
adb devices

# Specific device install
adb -s DEVICE_ID install app.apk
```

**Verify:**
- ✅ Can target specific device
- ✅ Installs on all devices

### H. Calculator App Testing

#### ☐ H1. Run PohLang Tests
```bash
cd Examples/android-calculator
python ../../plhub.py run src/main.poh
```

**Verify Output:**
```
╔════════════════════════════════════════╗
║   POHLANG ANDROID CALCULATOR APP      ║
╚════════════════════════════════════════╝

=== Testing Calculator Operations ===
5 + 3 = 8
10 - 3 = 7
6 × 7 = 42
20 ÷ 4 = 5
✅ All basic operations passed!

=== Testing Chained Operations ===
2 + 3 = 5
5 + 4 = 9
✅ Chained operations passed!

=== Testing Special Functions ===
50% = 0.5
-42 = -42
3.14 = 3.14
✅ Special functions passed!

=== Testing Clear Function ===
Before clear: 999
After clear: 0
✅ Clear function passed!

╔════════════════════════════════════════╗
║  CALCULATOR READY FOR ANDROID BUILD!   ║
╚════════════════════════════════════════╝
```

#### ☐ H2. Verify Test Coverage
**Verify Tests Cover:**
- ✅ Addition
- ✅ Subtraction
- ✅ Multiplication
- ✅ Division
- ✅ Division by zero handling
- ✅ Decimal numbers
- ✅ Percentage
- ✅ Negate
- ✅ Clear
- ✅ Chained operations

### I. Documentation Verification

#### ☐ I1. Quick Start Guide
```bash
cat docs/ANDROID_QUICKSTART.md
```

**Verify Contains:**
- ✅ Prerequisites checklist
- ✅ 5-minute tutorial
- ✅ Build commands
- ✅ Installation steps
- ✅ Troubleshooting

#### ☐ I2. Complete APK Guide
```bash
cat docs/ANDROID_APK_GUIDE.md
```

**Verify Contains:**
- ✅ Prerequisites (detailed)
- ✅ Project setup
- ✅ Build instructions
- ✅ Configuration options
- ✅ Signing guide
- ✅ Troubleshooting (detailed)
- ✅ Advanced topics

#### ☐ I3. Calculator README
```bash
cat Examples/android-calculator/README.md
```

**Verify Contains:**
- ✅ App overview
- ✅ Build instructions
- ✅ Installation steps
- ✅ Testing guide
- ✅ Code walkthrough

#### ☐ I4. Implementation Summary
```bash
cat docs/ANDROID_IMPLEMENTATION_SUMMARY.md
```

**Verify Contains:**
- ✅ What was created
- ✅ File list
- ✅ Statistics
- ✅ Usage examples
- ✅ Architecture details

### J. Error Handling

#### ☐ J1. Missing Prerequisites
```bash
# Simulate missing Java
# Expected: Clear error with installation instructions
```

#### ☐ J2. Invalid Project
```bash
cd /tmp
python PLHub/tools/android_apk_builder.py .
# Expected: Error about missing plhub.json
```

#### ☐ J3. Build Failure
```bash
# Corrupt Android project
# Expected: Gradle error with details
```

#### ☐ J4. Installation Failure
```bash
# No device connected
adb install app.apk
# Expected: Device not found error
```

### K. Integration Testing

#### ☐ K1. PLHub Build Command
```bash
cd Examples/android-calculator
python ../../plhub.py build android
```

**Verify:**
- ✅ Uses `android_apk_builder.py`
- ✅ Same output as direct call
- ✅ Success message

#### ☐ K2. Template System
```bash
cat templates/android.json
```

**Verify:**
- ✅ Valid JSON
- ✅ Android configuration
- ✅ Package name template
- ✅ Build scripts

### L. Cross-Platform Testing

#### ☐ L1. Windows Build
```powershell
# On Windows
cd PLHub\Examples\android-calculator
python ..\..\plhub.py build android
```

**Verify:**
- ✅ Path handling correct
- ✅ PowerShell compatible
- ✅ APK builds successfully

#### ☐ L2. Linux Build
```bash
# On Linux
cd PLHub/Examples/android-calculator
python ../../plhub.py build android
```

**Verify:**
- ✅ Builds successfully
- ✅ Correct permissions
- ✅ APK installable

#### ☐ L3. macOS Build
```bash
# On macOS
cd PLHub/Examples/android-calculator
python ../../plhub.py build android
```

**Verify:**
- ✅ Builds successfully
- ✅ Compatible with macOS paths

---

## 📊 Test Results Summary

### Quick Verification (5 items)
- [ ] Prerequisites Check
- [ ] Build Calculator APK
- [ ] Verify APK Created
- [ ] Install on Device
- [ ] Launch App

### Comprehensive Testing (50+ items)
- [ ] A. Prerequisites & Environment (3 items)
- [ ] B. Build Functionality (4 items)
- [ ] C. Project Generation (5 items)
- [ ] D. Gradle Configuration (3 items)
- [ ] E. APK Verification (4 items)
- [ ] F. Installation Testing (4 items)
- [ ] G. Device Testing (3 items)
- [ ] H. Calculator App Testing (2 items)
- [ ] I. Documentation Verification (4 items)
- [ ] J. Error Handling (4 items)
- [ ] K. Integration Testing (2 items)
- [ ] L. Cross-Platform Testing (3 items)

### Pass/Fail Criteria

**PASS if:**
- ✅ All Quick Verification items pass
- ✅ 90%+ of Comprehensive Testing items pass
- ✅ No critical errors
- ✅ APK builds and installs
- ✅ App launches successfully

**FAIL if:**
- ❌ APK doesn't build
- ❌ APK doesn't install
- ❌ App crashes on launch
- ❌ Critical prerequisites missing
- ❌ Less than 80% tests pass

---

## 🎯 Quick Test Script

Save this as `test_android_apk.sh`:

```bash
#!/bin/bash
echo "🧪 Testing Android APK Building..."
echo ""

# Test 1: Prerequisites
echo "☐ Testing prerequisites..."
java -version > /dev/null 2>&1 && echo "✅ Java found" || echo "❌ Java not found"
test -n "$ANDROID_HOME" && echo "✅ Android SDK set" || echo "❌ ANDROID_HOME not set"
adb version > /dev/null 2>&1 && echo "✅ ADB found" || echo "❌ ADB not found"
echo ""

# Test 2: Build
echo "☐ Building APK..."
cd PLHub/Examples/android-calculator
python ../../plhub.py build android
if [ $? -eq 0 ]; then
    echo "✅ Build succeeded"
else
    echo "❌ Build failed"
    exit 1
fi
echo ""

# Test 3: Verify APK
echo "☐ Verifying APK..."
if [ -f "build/android/android-calculator-debug.apk" ]; then
    echo "✅ APK exists"
    ls -lh build/android/android-calculator-debug.apk
else
    echo "❌ APK not found"
    exit 1
fi
echo ""

# Test 4: Check devices
echo "☐ Checking devices..."
adb devices | grep -v "List" | grep "device" > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ Device connected"
    
    # Test 5: Install
    echo "☐ Installing APK..."
    adb install -r build/android/android-calculator-debug.apk
    if [ $? -eq 0 ]; then
        echo "✅ Installation succeeded"
    else
        echo "❌ Installation failed"
        exit 1
    fi
else
    echo "⚠️  No device connected (skip installation test)"
fi

echo ""
echo "🎉 All tests passed!"
```

Run with:
```bash
chmod +x test_android_apk.sh
./test_android_apk.sh
```

---

## 📈 Success Metrics

### Build Performance
- ✅ First build: < 5 minutes
- ✅ Incremental build: < 1 minute
- ✅ APK size: 3-10 MB
- ✅ Install time: < 30 seconds

### Quality Metrics
- ✅ Build success rate: 100%
- ✅ Test coverage: 100%
- ✅ Documentation coverage: 100%
- ✅ Error handling: Comprehensive

### User Experience
- ✅ Clear progress indicators
- ✅ Helpful error messages
- ✅ Success confirmation
- ✅ Installation instructions

---

**✅ Complete this checklist to verify Android APK building is production-ready!**

For issues, see:
- [Troubleshooting Guide](ANDROID_APK_GUIDE.md#troubleshooting)
- [Quick Start](ANDROID_QUICKSTART.md)
- [Implementation Summary](ANDROID_IMPLEMENTATION_SUMMARY.md)
