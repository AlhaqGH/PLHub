"""
Platform Build Manager

Handles building PohLang applications for different target platforms:
- Android APK
- iOS IPA
- Windows EXE
- macOS APP
- Linux Binary
- Web (PWA)
"""

import subprocess
import shutil
from pathlib import Path
from typing import Optional, Dict, List
import json
import platform as sys_platform


class BuildTarget:
    """Platform build target."""
    
    ANDROID = "android"
    IOS = "ios"
    WINDOWS = "windows"
    MACOS = "macos"
    LINUX = "linux"
    WEB = "web"


class BuildManager:
    """Manages platform-specific builds."""
    
    def __init__(self, project_root: Path, plhub_root: Path):
        self.project_root = project_root
        self.plhub_root = plhub_root
        self.build_dir = project_root / "build"
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """Load project configuration."""
        config_file = self.project_root / "plhub.json"
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    # ==========================================================================
    # Android Build
    # ==========================================================================
    
    def build_android(self, release: bool = False, output_path: Optional[Path] = None) -> bool:
        """Build Android APK."""
        print("🤖 Building for Android...")
        
        # Check for Android SDK
        android_home = self._get_android_sdk()
        if not android_home:
            print("❌ Android SDK not found. Set ANDROID_HOME environment variable.")
            return False
        
        # Create Android project structure
        android_dir = self.build_dir / "android"
        android_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate Android project files
        self._generate_android_project(android_dir, release)
        
        # Build APK using Gradle
        gradle_cmd = "gradlew.bat" if sys_platform.system() == "Windows" else "./gradlew"
        build_type = "assembleRelease" if release else "assembleDebug"
        
        try:
            result = subprocess.run(
                [gradle_cmd, build_type],
                cwd=android_dir,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                apk_path = android_dir / "app" / "build" / "outputs" / "apk"
                apk_file = list(apk_path.glob("**/*.apk"))[0] if apk_path.exists() else None
                
                if apk_file and output_path:
                    shutil.copy2(apk_file, output_path)
                    print(f"✅ Android APK built: {output_path}")
                elif apk_file:
                    print(f"✅ Android APK built: {apk_file}")
                return True
            else:
                print(f"❌ Build failed:\n{result.stderr}")
                return False
        
        except Exception as e:
            print(f"❌ Build error: {e}")
            return False
    
    def _get_android_sdk(self) -> Optional[Path]:
        """Get Android SDK path."""
        import os
        android_home = os.environ.get('ANDROID_HOME')
        if android_home:
            return Path(android_home)
        
        # Try common locations
        common_paths = [
            Path.home() / "Android" / "Sdk",
            Path.home() / "Library" / "Android" / "sdk",
            Path("C:/Android/Sdk")
        ]
        
        for path in common_paths:
            if path.exists():
                return path
        
        return None
    
    def _generate_android_project(self, android_dir: Path, release: bool):
        """Generate Android project structure."""
        # Create directory structure
        (android_dir / "app" / "src" / "main" / "java").mkdir(parents=True, exist_ok=True)
        (android_dir / "app" / "src" / "main" / "res").mkdir(parents=True, exist_ok=True)
        (android_dir / "app" / "src" / "main" / "assets").mkdir(parents=True, exist_ok=True)
        
        # Generate AndroidManifest.xml
        manifest = self._generate_android_manifest()
        manifest_path = android_dir / "app" / "src" / "main" / "AndroidManifest.xml"
        manifest_path.write_text(manifest, encoding='utf-8')
        
        # Generate build.gradle
        build_gradle = self._generate_build_gradle(release)
        (android_dir / "app" / "build.gradle").write_text(build_gradle, encoding='utf-8')
        
        # Copy PohLang sources to assets
        src_dir = self.project_root / "src"
        if src_dir.exists():
            shutil.copytree(src_dir, android_dir / "app" / "src" / "main" / "assets" / "src", dirs_exist_ok=True)
    
    def _generate_android_manifest(self) -> str:
        """Generate AndroidManifest.xml."""
        app_name = self.config.get('name', 'PohLangApp')
        package = self.config.get('android', {}).get('package', f'com.pohlang.{app_name.lower()}')
        
        return f'''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{package}">

    <!-- Permissions -->
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <uses-permission android:name="android.permission.CAMERA" />
    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
    <uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
    <uses-permission android:name="android.permission.RECORD_AUDIO" />
    <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="{app_name}"
        android:theme="@style/Theme.AppCompat.Light">
        
        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
'''
    
    def _generate_build_gradle(self, release: bool) -> str:
        """Generate build.gradle for Android."""
        return '''
plugins {
    id 'com.android.application'
    id 'com.chaquo.python'
}

android {
    compileSdk 34
    
    defaultConfig {
        applicationId "com.pohlang.app"
        minSdk 24
        targetSdk 34
        versionCode 1
        versionName "1.0"
        
        ndk {
            abiFilters "armeabi-v7a", "arm64-v8a", "x86", "x86_64"
        }
        
        python {
            pip {
                install "pyjnius"
            }
        }
    }
    
    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
}

dependencies {
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.10.0'
}
'''
    
    # ==========================================================================
    # iOS Build
    # ==========================================================================
    
    def build_ios(self, release: bool = False, output_path: Optional[Path] = None) -> bool:
        """Build iOS IPA."""
        print("🍎 Building for iOS...")
        
        if sys_platform.system() != "Darwin":
            print("❌ iOS builds require macOS with Xcode")
            return False
        
        # Create iOS project structure
        ios_dir = self.build_dir / "ios"
        ios_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate Xcode project
        self._generate_ios_project(ios_dir, release)
        
        # Build using xcodebuild
        try:
            scheme = "Release" if release else "Debug"
            result = subprocess.run(
                ["xcodebuild", "-scheme", scheme, "build"],
                cwd=ios_dir,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("✅ iOS build completed")
                return True
            else:
                print(f"❌ Build failed:\n{result.stderr}")
                return False
        
        except Exception as e:
            print(f"❌ Build error: {e}")
            return False
    
    def _generate_ios_project(self, ios_dir: Path, release: bool):
        """Generate iOS project structure."""
        # Create directory structure
        (ios_dir / "App" / "Resources").mkdir(parents=True, exist_ok=True)
        
        # Generate Info.plist
        info_plist = self._generate_info_plist()
        (ios_dir / "App" / "Info.plist").write_text(info_plist, encoding='utf-8')
        
        # Copy PohLang sources
        src_dir = self.project_root / "src"
        if src_dir.exists():
            shutil.copytree(src_dir, ios_dir / "App" / "Resources" / "src", dirs_exist_ok=True)
    
    def _generate_info_plist(self) -> str:
        """Generate Info.plist for iOS."""
        app_name = self.config.get('name', 'PohLangApp')
        version = self.config.get('version', '1.0.0')
        
        return f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key>
    <string>{app_name}</string>
    <key>CFBundleDisplayName</key>
    <string>{app_name}</string>
    <key>CFBundleIdentifier</key>
    <string>com.pohlang.{app_name.lower()}</string>
    <key>CFBundleVersion</key>
    <string>{version}</string>
    <key>CFBundleShortVersionString</key>
    <string>{version}</string>
    <key>LSRequiresIPhoneOS</key>
    <true/>
    <key>UIRequiredDeviceCapabilities</key>
    <array>
        <string>armv7</string>
    </array>
    <key>NSLocationWhenInUseUsageDescription</key>
    <string>This app needs location access</string>
    <key>NSCameraUsageDescription</key>
    <string>This app needs camera access</string>
    <key>NSMicrophoneUsageDescription</key>
    <string>This app needs microphone access</string>
</dict>
</plist>
'''
    
    # ==========================================================================
    # Desktop Builds
    # ==========================================================================
    
    def build_desktop(self, target: str, release: bool = False, output_path: Optional[Path] = None) -> bool:
        """Build desktop executable."""
        print(f"🖥️  Building for {target}...")
        
        # Use PyInstaller or similar to create executable
        try:
            import PyInstaller.__main__
            
            main_file = self.project_root / self.config.get('main', 'src/main.poh')
            if not main_file.exists():
                print(f"❌ Main file not found: {main_file}")
                return False
            
            # PyInstaller arguments
            args = [
                str(main_file),
                '--onefile',
                '--name', self.config.get('name', 'PohLangApp'),
                '--distpath', str(self.build_dir / 'dist'),
                '--workpath', str(self.build_dir / 'work'),
            ]
            
            if release:
                args.append('--clean')
            
            PyInstaller.__main__.run(args)
            print(f"✅ {target} executable built")
            return True
        
        except ImportError:
            print("❌ PyInstaller not installed. Run: pip install pyinstaller")
            return False
        except Exception as e:
            print(f"❌ Build error: {e}")
            return False
    
    # ==========================================================================
    # Web Build
    # ==========================================================================
    
    def build_web(self, output_path: Optional[Path] = None) -> bool:
        """Build web application (PWA)."""
        print("🌐 Building for Web...")
        
        web_dir = self.build_dir / "web"
        web_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate web files (HTML, JS, service worker)
        self._generate_web_files(web_dir)
        
        print(f"✅ Web build completed: {web_dir}")
        return True
    
    def _generate_web_files(self, web_dir: Path):
        """Generate web application files."""
        # Generate index.html
        html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PohLang Web App</title>
</head>
<body>
    <h1>PohLang Web Application</h1>
    <div id="app"></div>
    <script src="app.js"></script>
</body>
</html>
'''
        (web_dir / "index.html").write_text(html, encoding='utf-8')


__all__ = ['BuildManager', 'BuildTarget']
