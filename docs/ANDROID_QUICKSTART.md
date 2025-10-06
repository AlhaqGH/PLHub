# 📱 Quick Start: Building Android APKs with PohLang

Get your first Android APK built in 5 minutes!

## ✅ Prerequisites Checklist

Before starting, make sure you have:

- [ ] **Java JDK 11+** installed
  ```bash
  java -version
  ```

- [ ] **Android SDK** installed (via Android Studio)
  ```bash
  # Check if ANDROID_HOME is set
  echo $ANDROID_HOME  # Linux/Mac
  echo $env:ANDROID_HOME  # Windows PowerShell
  ```

- [ ] **Android device** or **emulator** ready
  ```bash
  adb devices
  ```

**Don't have these?** See full setup in [ANDROID_APK_GUIDE.md](ANDROID_APK_GUIDE.md#prerequisites)

## 🚀 5-Minute Quick Start

### Step 1: Open Example Project (30 seconds)

```bash
cd PLHub/Examples/android-calculator
```

### Step 2: Build APK (2-3 minutes)

```bash
plhub build apk
```

You'll see:
```
╔════════════════════════════════════════╗
║   BUILDING ANDROID APK FOR POHLANG    ║
╚════════════════════════════════════════╝

⏳ Checking prerequisites...
   ✅ Java JDK found
   ✅ Android SDK found
   ✅ Gradle found
✅ All prerequisites met

⏳ Creating Android project structure...
✅ Android project structure created

⏳ Transpiling PohLang code...
✅ Transpilation step completed

⏳ Configuring debug build...
✅ Build configuration completed

⏳ Building debug APK with Gradle...
✅ Gradle build completed

⏳ Copying APK to output...
✅ APK copied to: build/android/android-calculator-debug.apk

╔════════════════════════════════════════╗
║       APK BUILD SUCCESSFUL! ✓          ║
╚════════════════════════════════════════╝

📱 App:     android-calculator
📦 Package: com.pohlang.calculator
🏷️  Version: 1.0.0
🔧 Mode:    DEBUG

📄 APK:     android-calculator-debug.apk
📁 Location: C:\...\build\android\android-calculator-debug.apk
💾 Size:    5.23 MB

✨ APK ready to install on Android devices!

📲 To install:
   adb install build/android/android-calculator-debug.apk
```

### Step 3: Install on Device (30 seconds)

```bash
adb install build/android/android-calculator-debug.apk
```

Success message:
```
Performing Streamed Install
Success
```

### Step 4: Run Your App! (10 seconds)

1. Find "PohLang Calculator" on your device
2. Tap to open
3. Use the calculator!

**🎉 Congratulations! You just built and installed your first Android APK with PohLang!**

## 📦 What You Built

```
android-calculator-debug.apk
├── Size: ~5 MB
├── Package: com.pohlang.calculator
├── Min Android: 7.0 (API 24)
├── Target Android: 14 (API 34)
└── Features:
    ├── Basic arithmetic (+ - × ÷)
    ├── Decimal numbers
    ├── Percentage calculation
    ├── Negate function
    └── Clear/reset
```

## 🎯 Next Steps

### Build Release APK (for production)

```bash
plhub build apk --release
```

Release APKs are:
- ✅ Optimized (smaller size)
- ✅ Faster performance
- ✅ Ready for Google Play
- ⚠️ Need signing for distribution

### Create Your Own Android App

```bash
# Create new Android project
cd PLHub
plhub create my-android-app --template android
cd my-android-app

# Edit your app
code src/main.poh

# Build APK
plhub build apk

# Install and test
adb install build/android/my-android-app-debug.apk
```

### Customize the Calculator

Edit `Examples/android-calculator/src/main.poh`:

```pohlang
// Add your own features
function handleSquareRoot(state as CalculatorState):
    state.currentValue = Math.sqrt(state.currentValue)
    state.display = Math.toString(state.currentValue)
```

Rebuild:
```bash
plhub build apk
adb install -r build/android/android-calculator-debug.apk
```

## 🔧 Build Commands Reference

### Basic Builds

```bash
# Debug build (for testing)
plhub build apk

# Release build (optimized)
plhub build apk --release

# Custom output location
plhub build apk -o MyApp.apk

# Verbose output
plhub build apk --verbose
```

### Installation Commands

```bash
# Install APK
adb install app.apk

# Reinstall (update existing)
adb install -r app.apk

# Uninstall app
adb uninstall com.pohlang.calculator

# List installed packages
adb shell pm list packages | grep pohlang
```

### Testing Commands

```bash
# Run app after install
adb shell am start -n com.pohlang.calculator/.MainActivity

# View logs
adb logcat | grep Calculator

# Take screenshot
adb shell screencap /sdcard/screenshot.png
adb pull /sdcard/screenshot.png
```

## 🐛 Quick Troubleshooting

### "ANDROID_HOME not set"

**Windows (PowerShell):**
```powershell
$env:ANDROID_HOME = "C:\Users\YourName\AppData\Local\Android\Sdk"
```

**Linux/macOS:**
```bash
export ANDROID_HOME=$HOME/Android/Sdk
```

### "No devices/emulators found"

```bash
# Check connected devices
adb devices

# If no devices listed:
# 1. Enable USB Debugging on phone
# 2. Or start emulator from Android Studio
```

### "Gradle build failed"

```bash
# Clean and rebuild
cd android
./gradlew clean
cd ..
plhub build apk
```

### "App not installed"

```bash
# Uninstall old version first
adb uninstall com.pohlang.calculator

# Then reinstall
adb install build/android/android-calculator-debug.apk
```

## 📚 Learn More

### Full Documentation

- **[Android APK Guide](ANDROID_APK_GUIDE.md)** - Complete APK building guide
  - Prerequisites setup
  - Project configuration
  - Signing and release
  - Publishing to Google Play

- **[Complete App Guide](COMPLETE_APP_GUIDE.md)** - Building complete applications
  - Console apps
  - Web apps
  - Desktop apps
  - Mobile apps

- **[PohLang Guide](../../PohLang/PohLang_Guide.md)** - PohLang language reference

### Example Apps

- **[Calculator](../Examples/android-calculator/)** - Calculator app
- **[Todo Manager](../Examples/complete-apps/todo-manager/)** - Task management
- **[Number Game](../Examples/complete-apps/number-game/)** - Guessing game

### Video Tutorials (Coming Soon)

- [ ] Building Your First Android APK
- [ ] Customizing Android Apps
- [ ] Publishing to Google Play

## 💡 Tips for Success

### Development Workflow

1. **Edit PohLang code** in `src/main.poh`
2. **Build APK** with `plhub build apk`
3. **Install** with `adb install -r build/android/*.apk`
4. **Test** on device
5. **Repeat** until perfect!

### Best Practices

✅ **DO:**
- Test on debug builds first
- Use `-r` flag to reinstall quickly
- Check `adb logcat` for errors
- Build release for production

❌ **DON'T:**
- Distribute debug APKs
- Forget to increment version
- Skip testing on real devices
- Ignore security warnings

### Performance Tips

- Use **release builds** for better performance
- Enable **ProGuard** for smaller APKs
- Test on **multiple Android versions**
- Optimize **images and assets**

## 🎉 Success Stories

### What You Can Build

- 📱 **Mobile Apps** - Games, utilities, productivity
- 🧮 **Calculators** - Scientific, financial, unit converters
- 📝 **Todo Lists** - Task managers, note apps
- 🎮 **Games** - Puzzle games, arcade games
- 📊 **Data Apps** - Trackers, analyzers, visualizers
- 🛠️ **Tools** - Custom utilities and helpers

### Publishing Checklist

Before publishing to Google Play:

- [ ] Test on multiple devices
- [ ] Build release APK
- [ ] Sign with production keystore
- [ ] Create app icon (512×512)
- [ ] Write store description
- [ ] Take screenshots (phone + tablet)
- [ ] Create feature graphic
- [ ] Set pricing and distribution
- [ ] Submit for review

## 🆘 Get Help

### Having Issues?

1. **Check** [Troubleshooting](#quick-troubleshooting) section above
2. **Read** [Full Android Guide](ANDROID_APK_GUIDE.md)
3. **Search** existing issues on GitHub
4. **Ask** in community forums

### Common Questions

**Q: How big is the APK?**
A: Debug builds ~5-10 MB, release builds ~3-5 MB (optimized)

**Q: What Android versions are supported?**
A: Android 7.0 (API 24) and higher (covers 99%+ of devices)

**Q: Can I publish to Google Play?**
A: Yes! Build release APK, sign it, and upload to Google Play Console

**Q: How long does building take?**
A: First build: 2-5 minutes. Subsequent builds: 30-60 seconds

**Q: Do I need Android Studio?**
A: Only for Android SDK. You can build APKs from command line!

## ✨ You're Ready!

You now know how to:
- ✅ Build Android APKs from PohLang
- ✅ Install apps on devices
- ✅ Test and debug
- ✅ Create your own Android apps

**Start building amazing Android apps with PohLang!** 🚀

---

**Next:** [Full Android APK Guide](ANDROID_APK_GUIDE.md) | [Create Your Own App](#create-your-own-android-app)
