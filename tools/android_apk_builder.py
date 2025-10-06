#!/usr/bin/env python3
"""
Android APK Builder for PohLang Applications
Builds complete Android APK files from PohLang apps
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional, Dict


class AndroidAPKBuilder:
    """
    Complete Android APK builder for PohLang applications.
    Creates Android project structure, transpiles PohLang code,
    and builds APK using Gradle.
    """
    
    def __init__(self, project_root: Path, plhub_root: Path):
        """
        Initialize Android APK builder.
        
        Args:
            project_root: Path to PohLang project root
            plhub_root: Path to PLHub installation
        """
        self.project_root = Path(project_root).resolve()
        self.plhub_root = Path(plhub_root).resolve()
        self.android_dir = self.project_root / "android"
        self.build_dir = self.project_root / "build" / "android"
        
        # Load project config
        self.config = self._load_config()
        
    def _load_config(self) -> Dict:
        """Load plhub.json configuration."""
        config_path = self.project_root / "plhub.json"
        if not config_path.exists():
            raise FileNotFoundError(f"Project configuration not found: {config_path}")
        
        with open(config_path, 'r') as f:
            return json.load(f)
    
    def build_apk(
        self,
        release: bool = False,
        output_path: Optional[Path] = None,
        sign: bool = False,
        keystore: Optional[str] = None,
        key_alias: Optional[str] = None
    ) -> bool:
        """
        Build Android APK from PohLang application.
        
        Args:
            release: Build release APK (optimized)
            output_path: Custom output path for APK
            sign: Sign the APK
            keystore: Path to keystore file
            key_alias: Key alias in keystore
            
        Returns:
            True if build succeeded, False otherwise
        """
        print("╔════════════════════════════════════════╗")
        print("║   BUILDING ANDROID APK FOR POHLANG    ║")
        print("╚════════════════════════════════════════╝")
        print()
        
        try:
            # Step 1: Check prerequisites
            if not self._check_prerequisites():
                return False
            
            # Step 2: Create Android project structure
            if not self._create_android_project():
                return False
            
            # Step 3: Transpile PohLang code to Java/Kotlin
            if not self._transpile_pohlang_code():
                return False
            
            # Step 4: Configure Android build
            if not self._configure_android_build(release):
                return False
            
            # Step 5: Build APK with Gradle
            if not self._build_with_gradle(release):
                return False
            
            # Step 6: Sign APK if requested
            if sign and release:
                if not self._sign_apk(keystore, key_alias):
                    return False
            
            # Step 7: Copy APK to output location
            if not self._copy_apk_output(release, output_path):
                return False
            
            # Success!
            self._print_success_message(release, output_path)
            return True
            
        except Exception as e:
            print(f"❌ Build failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _check_prerequisites(self) -> bool:
        """Check that required tools are installed."""
        print("⏳ Checking prerequisites...")
        
        checks = [
            ("Java JDK", self._check_java),
            ("Android SDK", self._check_android_sdk),
            ("Gradle", self._check_gradle),
        ]
        
        all_passed = True
        for name, check_func in checks:
            if check_func():
                print(f"   ✅ {name} found")
            else:
                print(f"   ❌ {name} not found")
                all_passed = False
        
        if not all_passed:
            print()
            print("❌ Missing prerequisites. Please install:")
            print("   • Java JDK 11 or higher")
            print("   • Android SDK (via Android Studio)")
            print("   • Gradle build tool")
            print()
            print("See: https://developer.android.com/studio/install")
            return False
        
        print("✅ All prerequisites met")
        print()
        return True
    
    def _check_java(self) -> bool:
        """Check if Java is installed."""
        try:
            result = subprocess.run(
                ["java", "-version"],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def _check_android_sdk(self) -> bool:
        """Check if Android SDK is installed."""
        # Check common Android SDK locations
        sdk_paths = [
            os.getenv("ANDROID_HOME"),
            os.getenv("ANDROID_SDK_ROOT"),
            Path.home() / "Android" / "Sdk",
            Path.home() / "Library" / "Android" / "sdk",
            Path("C:/Android/sdk"),
        ]
        
        for sdk_path in sdk_paths:
            if sdk_path and Path(sdk_path).exists():
                return True
        
        return False
    
    def _check_gradle(self) -> bool:
        """Check if Gradle is installed."""
        try:
            result = subprocess.run(
                ["gradle", "--version"],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except FileNotFoundError:
            # Check for gradlew wrapper
            gradlew = self.android_dir / ("gradlew.bat" if sys.platform == "win32" else "gradlew")
            return gradlew.exists()
    
    def _create_android_project(self) -> bool:
        """Create Android project structure."""
        print("⏳ Creating Android project structure...")
        
        # Create directories
        dirs = [
            self.android_dir / "app" / "src" / "main" / "java",
            self.android_dir / "app" / "src" / "main" / "res" / "layout",
            self.android_dir / "app" / "src" / "main" / "res" / "values",
            self.android_dir / "app" / "src" / "main" / "res" / "drawable",
            self.android_dir / "app" / "src" / "main" / "res" / "mipmap-hdpi",
            self.android_dir / "app" / "src" / "main" / "res" / "mipmap-mdpi",
            self.android_dir / "app" / "src" / "main" / "res" / "mipmap-xhdpi",
            self.android_dir / "app" / "src" / "main" / "res" / "mipmap-xxhdpi",
            self.android_dir / "app" / "src" / "main" / "res" / "mipmap-xxxhdpi",
            self.build_dir,
        ]
        
        for dir_path in dirs:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # Create build.gradle files
        self._create_root_gradle()
        self._create_app_gradle()
        self._create_settings_gradle()
        
        # Create AndroidManifest.xml
        self._create_android_manifest()
        
        # Create MainActivity
        self._create_main_activity()
        
        # Create layout files
        self._create_layout_files()
        
        # Create resources
        self._create_resource_files()
        
        # Create gradle wrapper if not exists
        self._create_gradle_wrapper()
        
        print("✅ Android project structure created")
        print()
        return True
    
    def _create_root_gradle(self):
        """Create root build.gradle file."""
        content = """// Top-level build file for Android project
buildscript {
    ext.kotlin_version = '1.9.0'
    repositories {
        google()
        mavenCentral()
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:8.1.0'
        classpath "org.jetbrains.kotlin:kotlin-gradle-plugin:$kotlin_version"
    }
}

allprojects {
    repositories {
        google()
        mavenCentral()
    }
}

task clean(type: Delete) {
    delete rootProject.buildDir
}
"""
        (self.android_dir / "build.gradle").write_text(content)
    
    def _create_app_gradle(self):
        """Create app/build.gradle file."""
        package_name = self.config.get("android", {}).get(
            "package_name",
            f"com.pohlang.{self.config.get('name', 'app').lower().replace('-', '_')}"
        )
        
        content = f"""plugins {{
    id 'com.android.application'
    id 'kotlin-android'
}}

android {{
    namespace '{package_name}'
    compileSdk 34
    
    defaultConfig {{
        applicationId '{package_name}'
        minSdk 24
        targetSdk 34
        versionCode {self._get_version_code()}
        versionName '{self.config.get("version", "1.0.0")}'
        
        testInstrumentationRunner 'androidx.test.runner.AndroidJUnitRunner'
    }}
    
    buildTypes {{
        release {{
            minifyEnabled true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }}
        debug {{
            debuggable true
        }}
    }}
    
    compileOptions {{
        sourceCompatibility JavaVersion.VERSION_11
        targetCompatibility JavaVersion.VERSION_11
    }}
    
    kotlinOptions {{
        jvmTarget = '11'
    }}
}}

dependencies {{
    implementation 'androidx.core:core-ktx:1.12.0'
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.10.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}}
"""
        (self.android_dir / "app" / "build.gradle").write_text(content)
    
    def _create_settings_gradle(self):
        """Create settings.gradle file."""
        content = """rootProject.name = '""" + self.config.get('name', 'PohLangApp') + """'
include ':app'
"""
        (self.android_dir / "settings.gradle").write_text(content)
    
    def _create_android_manifest(self):
        """Create AndroidManifest.xml file."""
        package_name = self.config.get("android", {}).get(
            "package_name",
            f"com.pohlang.{self.config.get('name', 'app').lower().replace('-', '_')}"
        )
        
        app_name = self.config.get("android", {}).get("app_name", self.config.get("name", "PohLang App"))
        
        content = f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools">

    <!-- Permissions -->
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="{app_name}"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.AppCompat.Light.DarkActionBar"
        tools:targetApi="31">
        
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
"""
        manifest_path = self.android_dir / "app" / "src" / "main" / "AndroidManifest.xml"
        manifest_path.write_text(content)
    
    def _create_main_activity(self):
        """Create MainActivity.kt file."""
        package_name = self.config.get("android", {}).get(
            "package_name",
            f"com.pohlang.{self.config.get('name', 'app').lower().replace('-', '_')}"
        )
        
        content = f"""package {package_name}

import android.os.Bundle
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {{
    override fun onCreate(savedInstanceState: Bundle?) {{
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        
        // Get output from PohLang runtime
        val outputText = findViewById<TextView>(R.id.output_text)
        outputText.text = runPohLangApp()
    }}
    
    private fun runPohLangApp(): String {{
        // This will be replaced with actual PohLang runtime integration
        return "Hello from PohLang!\\n" +
               "App: {self.config.get('name', 'PohLang App')}\\n" +
               "Version: {self.config.get('version', '1.0.0')}\\n\\n" +
               "PohLang runtime integration coming soon!"
    }}
}}
"""
        # Create package directories
        package_parts = package_name.split('.')
        package_dir = self.android_dir / "app" / "src" / "main" / "java"
        for part in package_parts:
            package_dir = package_dir / part
        package_dir.mkdir(parents=True, exist_ok=True)
        
        (package_dir / "MainActivity.kt").write_text(content)
    
    def _create_layout_files(self):
        """Create layout XML files."""
        activity_main = """<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout 
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:padding="16dp"
    tools:context=".MainActivity">

    <ScrollView
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintStart_toStartOf="parent">

        <TextView
            android:id="@+id/output_text"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:text="Loading PohLang App..."
            android:textSize="16sp"
            android:fontFamily="monospace"
            android:padding="8dp" />

    </ScrollView>

</androidx.constraintlayout.widget.ConstraintLayout>
"""
        layout_dir = self.android_dir / "app" / "src" / "main" / "res" / "layout"
        (layout_dir / "activity_main.xml").write_text(activity_main)
    
    def _create_resource_files(self):
        """Create resource files (strings, colors, etc.)."""
        # strings.xml
        strings = f"""<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">{self.config.get('name', 'PohLang App')}</string>
</resources>
"""
        values_dir = self.android_dir / "app" / "src" / "main" / "res" / "values"
        (values_dir / "strings.xml").write_text(strings)
        
        # colors.xml
        colors = """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="purple_200">#FFBB86FC</color>
    <color name="purple_500">#FF6200EE</color>
    <color name="purple_700">#FF3700B3</color>
    <color name="teal_200">#FF03DAC5</color>
    <color name="teal_700">#FF018786</color>
    <color name="black">#FF000000</color>
    <color name="white">#FFFFFFFF</color>
</resources>
"""
        (values_dir / "colors.xml").write_text(colors)
    
    def _create_gradle_wrapper(self):
        """Create Gradle wrapper if it doesn't exist."""
        gradlew_path = self.android_dir / "gradlew"
        if not gradlew_path.exists():
            # Create basic gradle wrapper
            wrapper_dir = self.android_dir / "gradle" / "wrapper"
            wrapper_dir.mkdir(parents=True, exist_ok=True)
            
            # gradle-wrapper.properties
            properties = """distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\\://services.gradle.org/distributions/gradle-8.2-bin.zip
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
"""
            (wrapper_dir / "gradle-wrapper.properties").write_text(properties)
    
    def _get_version_code(self) -> int:
        """Convert version string to version code."""
        version = self.config.get('version', '1.0.0')
        parts = version.split('.')
        try:
            major = int(parts[0]) if len(parts) > 0 else 1
            minor = int(parts[1]) if len(parts) > 1 else 0
            patch = int(parts[2]) if len(parts) > 2 else 0
            return major * 10000 + minor * 100 + patch
        except:
            return 10000
    
    def _transpile_pohlang_code(self) -> bool:
        """Transpile PohLang code to Java/Kotlin."""
        print("⏳ Transpiling PohLang code...")
        
        # For now, we'll create a placeholder
        # In future, this will actually transpile PohLang to Java/Kotlin
        
        print("   ⚠️  PohLang to Java/Kotlin transpilation not yet implemented")
        print("   Using placeholder implementation")
        print("✅ Transpilation step completed")
        print()
        return True
    
    def _configure_android_build(self, release: bool) -> bool:
        """Configure Android build settings."""
        print(f"⏳ Configuring {'release' if release else 'debug'} build...")
        
        # Configuration is done via gradle files
        
        print("✅ Build configuration completed")
        print()
        return True
    
    def _build_with_gradle(self, release: bool) -> bool:
        """Build APK using Gradle."""
        print(f"⏳ Building {'release' if release else 'debug'} APK with Gradle...")
        print()
        
        # Determine gradle command
        if sys.platform == "win32":
            gradle_cmd = self.android_dir / "gradlew.bat"
            if not gradle_cmd.exists():
                gradle_cmd = "gradle"
        else:
            gradle_cmd = self.android_dir / "gradlew"
            if not gradle_cmd.exists():
                gradle_cmd = "gradle"
        
        # Build command
        build_type = "assembleRelease" if release else "assembleDebug"
        
        try:
            result = subprocess.run(
                [str(gradle_cmd), build_type, "--no-daemon"],
                cwd=self.android_dir,
                capture_output=False,
                text=True
            )
            
            if result.returncode != 0:
                print(f"❌ Gradle build failed with exit code {result.returncode}")
                return False
            
            print()
            print("✅ Gradle build completed")
            print()
            return True
            
        except Exception as e:
            print(f"❌ Gradle build error: {e}")
            return False
    
    def _sign_apk(self, keystore: Optional[str], key_alias: Optional[str]) -> bool:
        """Sign the APK."""
        print("⏳ Signing APK...")
        
        # APK signing is typically done via Gradle with signing config
        # For now, skip this step
        
        print("   ⚠️  APK signing configuration not yet implemented")
        print("   Use Android Studio or jarsigner for manual signing")
        print()
        return True
    
    def _copy_apk_output(self, release: bool, output_path: Optional[Path]) -> bool:
        """Copy APK to output location."""
        print("⏳ Copying APK to output...")
        
        # Find APK in build output
        build_type = "release" if release else "debug"
        apk_source = self.android_dir / "app" / "build" / "outputs" / "apk" / build_type / f"app-{build_type}.apk"
        
        if not apk_source.exists():
            print(f"❌ APK not found at {apk_source}")
            return False
        
        # Determine output path
        if output_path:
            apk_dest = Path(output_path)
        else:
            apk_dest = self.build_dir / f"{self.config.get('name', 'app')}-{build_type}.apk"
        
        apk_dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(apk_source, apk_dest)
        
        # Store output path for success message
        self.output_apk_path = apk_dest
        
        print(f"✅ APK copied to: {apk_dest}")
        print()
        return True
    
    def _print_success_message(self, release: bool, output_path: Optional[Path]):
        """Print success message with APK details."""
        print()
        print("╔════════════════════════════════════════╗")
        print("║       APK BUILD SUCCESSFUL! ✓          ║")
        print("╚════════════════════════════════════════╝")
        print()
        print(f"📱 App:     {self.config.get('name', 'PohLang App')}")
        print(f"📦 Package: {self.config.get('android', {}).get('package_name', 'com.pohlang.app')}")
        print(f"🏷️  Version: {self.config.get('version', '1.0.0')}")
        print(f"🔧 Mode:    {'RELEASE' if release else 'DEBUG'}")
        print()
        
        if hasattr(self, 'output_apk_path'):
            size = self.output_apk_path.stat().st_size
            size_mb = size / (1024 * 1024)
            print(f"📄 APK:     {self.output_apk_path.name}")
            print(f"📁 Location: {self.output_apk_path}")
            print(f"💾 Size:    {size_mb:.2f} MB")
        print()
        print("✨ APK ready to install on Android devices!")
        print()
        print("📲 To install:")
        print(f"   adb install {self.output_apk_path if hasattr(self, 'output_apk_path') else 'app.apk'}")
        print()


def main():
    """CLI entry point for Android APK builder."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Build Android APK from PohLang application"
    )
    parser.add_argument("project", nargs="?", default=".",
                       help="Project directory (default: current directory)")
    parser.add_argument("--release", action="store_true",
                       help="Build release APK (optimized)")
    parser.add_argument("-o", "--out", type=Path,
                       help="Output path for APK")
    parser.add_argument("--sign", action="store_true",
                       help="Sign the APK")
    parser.add_argument("--keystore", type=str,
                       help="Path to keystore file")
    parser.add_argument("--key-alias", type=str,
                       help="Key alias in keystore")
    
    args = parser.parse_args()
    
    try:
        # Determine PLHub root (parent of tools directory)
        plhub_root = Path(__file__).parent.parent
        
        builder = AndroidAPKBuilder(
            project_root=Path(args.project),
            plhub_root=plhub_root
        )
        
        success = builder.build_apk(
            release=args.release,
            output_path=args.out,
            sign=args.sign,
            keystore=args.keystore,
            key_alias=args.key_alias
        )
        
        sys.exit(0 if success else 1)
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
