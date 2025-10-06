"""
PLHub Platform Manager
Manages cross-platform project creation, building, and deployment for:
- Android
- iOS  
- macOS
- Windows
- Web
"""

import os
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
from enum import Enum


class Platform(Enum):
    """Supported platforms"""
    ANDROID = "android"
    IOS = "ios"
    MACOS = "macos"
    WINDOWS = "windows"
    WEB = "web"


class PlatformManager:
    """Manages cross-platform development"""
    
    def __init__(self, plhub_root: Optional[Path] = None):
        self.plhub_root = plhub_root or Path(__file__).parent.parent
        self.templates_dir = self.plhub_root / "templates"
        self.builders = {
            Platform.ANDROID: AndroidBuilder(),
            Platform.IOS: IOSBuilder(),
            Platform.MACOS: MacOSBuilder(),
            Platform.WINDOWS: WindowsBuilder(),
            Platform.WEB: WebBuilder()
        }
    
    def create_project(self, platform: Platform, project_name: str, 
                      output_dir: Path, package_name: Optional[str] = None) -> bool:
        """Create a new platform-specific project"""
        try:
            print(f"Creating {platform.value} project: {project_name}")
            
            # Get template
            template_dir = self.templates_dir / platform.value
            if not template_dir.exists():
                print(f"Error: Template not found for {platform.value}")
                return False
            
            # Load project structure
            structure_file = template_dir / "project_structure.json"
            with open(structure_file, 'r') as f:
                structure = json.load(f)
            
            # Create project directory
            project_dir = output_dir / project_name
            project_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate package name if not provided
            if not package_name:
                package_name = f"com.pohlang.{project_name.lower().replace('-', '_')}"
            
            # Create project structure
            self._create_structure(project_dir, structure['structure'], 
                                  template_dir, project_name, package_name)
            
            print(f"✓ Project created at: {project_dir}")
            print(f"  Platform: {platform.value}")
            print(f"  Package: {package_name}")
            
            # Display next steps
            self._display_next_steps(platform, project_dir)
            
            return True
            
        except Exception as e:
            print(f"Error creating project: {e}")
            return False
    
    def _create_structure(self, base_dir: Path, structure: Dict, 
                         template_dir: Path, app_name: str, package_name: str):
        """Recursively create project structure"""
        for name, content in structure.items():
            # Replace placeholders
            name = name.replace("{{APP_NAME}}", app_name)
            path = base_dir / name
            
            if isinstance(content, dict):
                # Directory
                path.mkdir(parents=True, exist_ok=True)
                self._create_structure(path, content, template_dir, 
                                     app_name, package_name)
            elif isinstance(content, list):
                # Directory with specific files
                path.mkdir(parents=True, exist_ok=True)
                for file in content:
                    file_path = path / file
                    file_path.touch()
            elif content is True:
                # File - copy from template if exists
                template_file = self._find_template_file(template_dir, name)
                if template_file and template_file.exists():
                    content_text = template_file.read_text(encoding='utf-8')
                    # Replace placeholders
                    content_text = content_text.replace("{{APP_NAME}}", app_name)
                    content_text = content_text.replace("{{PACKAGE_NAME}}", package_name)
                    path.write_text(content_text, encoding='utf-8')
                else:
                    path.touch()
    
    def _find_template_file(self, template_dir: Path, filename: str) -> Optional[Path]:
        """Find template file by name"""
        # Try direct path
        direct_path = template_dir / filename
        if direct_path.exists():
            return direct_path
        
        # Search recursively
        for file in template_dir.rglob(filename):
            return file
        
        return None
    
    def _display_next_steps(self, platform: Platform, project_dir: Path):
        """Display platform-specific next steps"""
        print("\n📋 Next Steps:")
        
        if platform == Platform.ANDROID:
            print("  1. Open project in Android Studio")
            print("  2. Sync Gradle files")
            print("  3. Run: plhub platform run android")
            print("  4. Connect device or start emulator")
            
        elif platform == Platform.IOS:
            print("  1. Open {project_dir.name}.xcodeproj in Xcode")
            print("  2. Select target device/simulator")
            print("  3. Run: plhub platform run ios")
            print("  4. Requires macOS with Xcode")
            
        elif platform == Platform.MACOS:
            print("  1. Open {project_dir.name}.xcodeproj in Xcode")
            print("  2. Build for macOS target")
            print("  3. Run: plhub platform run macos")
            
        elif platform == Platform.WINDOWS:
            print("  1. Open project in Visual Studio 2022")
            print("  2. Restore NuGet packages")
            print("  3. Run: plhub platform run windows")
            print("  4. Requires Windows 10/11 with WinUI3 SDK")
            
        elif platform == Platform.WEB:
            print("  1. Install dependencies: npm install")
            print("  2. Start dev server: plhub platform run web")
            print("  3. Open http://localhost:8080")
            print("  4. Hot reload enabled automatically")
    
    def build(self, platform: Platform, project_dir: Path, 
             configuration: str = "debug") -> bool:
        """Build project for specified platform"""
        try:
            builder = self.builders[platform]
            return builder.build(project_dir, configuration)
        except Exception as e:
            print(f"Build error: {e}")
            return False
    
    def run(self, platform: Platform, project_dir: Path, 
           device: Optional[str] = None) -> bool:
        """Run project on specified platform"""
        try:
            builder = self.builders[platform]
            return builder.run(project_dir, device)
        except Exception as e:
            print(f"Run error: {e}")
            return False
    
    def test(self, platform: Platform, project_dir: Path) -> bool:
        """Run tests for specified platform"""
        try:
            builder = self.builders[platform]
            return builder.test(project_dir)
        except Exception as e:
            print(f"Test error: {e}")
            return False
    
    def deploy(self, platform: Platform, project_dir: Path, 
              target: str) -> bool:
        """Deploy project to specified target"""
        try:
            builder = self.builders[platform]
            return builder.deploy(project_dir, target)
        except Exception as e:
            print(f"Deploy error: {e}")
            return False
    
    def list_devices(self, platform: Platform) -> List[Dict[str, Any]]:
        """List available devices for platform"""
        try:
            builder = self.builders[platform]
            return builder.list_devices()
        except Exception as e:
            print(f"Error listing devices: {e}")
            return []
    
    def get_platforms(self) -> List[str]:
        """Get list of supported platforms"""
        return [p.value for p in Platform]


class PlatformBuilder:
    """Base class for platform builders"""
    
    def build(self, project_dir: Path, configuration: str) -> bool:
        raise NotImplementedError
    
    def run(self, project_dir: Path, device: Optional[str]) -> bool:
        raise NotImplementedError
    
    def test(self, project_dir: Path) -> bool:
        raise NotImplementedError
    
    def deploy(self, project_dir: Path, target: str) -> bool:
        raise NotImplementedError
    
    def list_devices(self) -> List[Dict[str, Any]]:
        raise NotImplementedError
    
    def _run_command(self, cmd: List[str], cwd: Path) -> bool:
        """Run shell command"""
        try:
            print(f"Running: {' '.join(cmd)}")
            result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
            
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr, file=sys.stderr)
            
            return result.returncode == 0
        except Exception as e:
            print(f"Command error: {e}")
            return False


class AndroidBuilder(PlatformBuilder):
    """Android platform builder"""
    
    def build(self, project_dir: Path, configuration: str) -> bool:
        """Build Android APK/AAB"""
        print(f"Building Android project ({configuration})...")
        
        gradlew = "./gradlew.bat" if sys.platform == "win32" else "./gradlew"
        task = "assembleDebug" if configuration == "debug" else "assembleRelease"
        
        return self._run_command([gradlew, task], project_dir)
    
    def run(self, project_dir: Path, device: Optional[str]) -> bool:
        """Run on Android device/emulator"""
        print("Running Android application...")
        
        gradlew = "./gradlew.bat" if sys.platform == "win32" else "./gradlew"
        cmd = [gradlew, "installDebug"]
        
        if device:
            cmd.extend(["-Pandroid.device=" + device])
        
        if not self._run_command(cmd, project_dir):
            return False
        
        # Launch activity
        package = self._get_package_name(project_dir)
        activity = f"{package}.MainActivity"
        
        adb_cmd = ["adb", "shell", "am", "start", "-n", f"{package}/{activity}"]
        if device:
            adb_cmd = ["adb", "-s", device] + adb_cmd[1:]
        
        return self._run_command(adb_cmd, project_dir)
    
    def test(self, project_dir: Path) -> bool:
        """Run Android tests"""
        print("Running Android tests...")
        
        gradlew = "./gradlew.bat" if sys.platform == "win32" else "./gradlew"
        
        # Run unit tests
        if not self._run_command([gradlew, "test"], project_dir):
            return False
        
        # Run instrumented tests
        return self._run_command([gradlew, "connectedAndroidTest"], project_dir)
    
    def deploy(self, project_dir: Path, target: str) -> bool:
        """Deploy to Google Play"""
        print(f"Deploying Android app to {target}...")
        
        # Build release bundle
        gradlew = "./gradlew.bat" if sys.platform == "win32" else "./gradlew"
        return self._run_command([gradlew, "bundleRelease"], project_dir)
    
    def list_devices(self) -> List[Dict[str, Any]]:
        """List connected Android devices"""
        try:
            result = subprocess.run(["adb", "devices", "-l"], 
                                  capture_output=True, text=True)
            devices = []
            
            for line in result.stdout.split('\n')[1:]:
                if line.strip() and 'device' in line:
                    parts = line.split()
                    devices.append({
                        'id': parts[0],
                        'status': parts[1],
                        'type': 'emulator' if 'emulator' in parts[0] else 'physical'
                    })
            
            return devices
        except Exception as e:
            print(f"Error listing devices: {e}")
            return []
    
    def _get_package_name(self, project_dir: Path) -> str:
        """Extract package name from AndroidManifest.xml"""
        manifest = project_dir / "app" / "src" / "main" / "AndroidManifest.xml"
        if manifest.exists():
            import xml.etree.ElementTree as ET
            tree = ET.parse(manifest)
            return tree.getroot().get('package', 'com.pohlang.app')
        return "com.pohlang.app"


class IOSBuilder(PlatformBuilder):
    """iOS platform builder"""
    
    def build(self, project_dir: Path, configuration: str) -> bool:
        """Build iOS app"""
        print(f"Building iOS project ({configuration})...")
        
        xcodeproj = list(project_dir.glob("*.xcodeproj"))[0]
        scheme = xcodeproj.stem
        
        cmd = [
            "xcodebuild",
            "-project", str(xcodeproj),
            "-scheme", scheme,
            "-configuration", configuration.capitalize(),
            "-sdk", "iphoneos",
            "build"
        ]
        
        return self._run_command(cmd, project_dir)
    
    def run(self, project_dir: Path, device: Optional[str]) -> bool:
        """Run on iOS device/simulator"""
        print("Running iOS application...")
        
        # Build first
        if not self.build(project_dir, "debug"):
            return False
        
        # Launch simulator
        xcodeproj = list(project_dir.glob("*.xcodeproj"))[0]
        scheme = xcodeproj.stem
        
        destination = f"platform=iOS Simulator,name={device}" if device else "platform=iOS Simulator"
        
        cmd = [
            "xcodebuild",
            "-project", str(xcodeproj),
            "-scheme", scheme,
            "-destination", destination,
            "run"
        ]
        
        return self._run_command(cmd, project_dir)
    
    def test(self, project_dir: Path) -> bool:
        """Run iOS tests"""
        print("Running iOS tests...")
        
        xcodeproj = list(project_dir.glob("*.xcodeproj"))[0]
        scheme = xcodeproj.stem
        
        cmd = [
            "xcodebuild",
            "-project", str(xcodeproj),
            "-scheme", scheme,
            "-destination", "platform=iOS Simulator",
            "test"
        ]
        
        return self._run_command(cmd, project_dir)
    
    def deploy(self, project_dir: Path, target: str) -> bool:
        """Deploy to App Store"""
        print(f"Deploying iOS app to {target}...")
        
        # Build archive
        xcodeproj = list(project_dir.glob("*.xcodeproj"))[0]
        scheme = xcodeproj.stem
        archive_path = project_dir / "build" / f"{scheme}.xcarchive"
        
        cmd = [
            "xcodebuild",
            "-project", str(xcodeproj),
            "-scheme", scheme,
            "-configuration", "Release",
            "-archivePath", str(archive_path),
            "archive"
        ]
        
        return self._run_command(cmd, project_dir)
    
    def list_devices(self) -> List[Dict[str, Any]]:
        """List iOS simulators and devices"""
        try:
            result = subprocess.run(["xcrun", "simctl", "list", "devices", "available"],
                                  capture_output=True, text=True)
            devices = []
            
            for line in result.stdout.split('\n'):
                if '(' in line and ')' in line:
                    name = line.split('(')[0].strip()
                    udid = line.split('(')[1].split(')')[0]
                    devices.append({
                        'name': name,
                        'udid': udid,
                        'type': 'simulator'
                    })
            
            return devices
        except Exception as e:
            print(f"Error listing devices: {e}")
            return []


class MacOSBuilder(PlatformBuilder):
    """macOS platform builder"""
    
    def build(self, project_dir: Path, configuration: str) -> bool:
        """Build macOS app"""
        print(f"Building macOS project ({configuration})...")
        
        xcodeproj = list(project_dir.glob("*.xcodeproj"))[0]
        scheme = xcodeproj.stem
        
        cmd = [
            "xcodebuild",
            "-project", str(xcodeproj),
            "-scheme", scheme,
            "-configuration", configuration.capitalize(),
            "build"
        ]
        
        return self._run_command(cmd, project_dir)
    
    def run(self, project_dir: Path, device: Optional[str]) -> bool:
        """Run macOS app"""
        print("Running macOS application...")
        
        # Build first
        if not self.build(project_dir, "debug"):
            return False
        
        # Find and launch app
        build_dir = project_dir / "build" / "Debug"
        app = list(build_dir.glob("*.app"))[0]
        
        cmd = ["open", str(app)]
        return self._run_command(cmd, project_dir)
    
    def test(self, project_dir: Path) -> bool:
        """Run macOS tests"""
        print("Running macOS tests...")
        
        xcodeproj = list(project_dir.glob("*.xcodeproj"))[0]
        scheme = xcodeproj.stem
        
        cmd = [
            "xcodebuild",
            "-project", str(xcodeproj),
            "-scheme", scheme,
            "test"
        ]
        
        return self._run_command(cmd, project_dir)
    
    def deploy(self, project_dir: Path, target: str) -> bool:
        """Deploy macOS app"""
        print(f"Deploying macOS app to {target}...")
        
        # Build release
        return self.build(project_dir, "release")
    
    def list_devices(self) -> List[Dict[str, Any]]:
        """List macOS devices (always just local machine)"""
        return [{'name': 'Local Mac', 'type': 'physical'}]


class WindowsBuilder(PlatformBuilder):
    """Windows platform builder"""
    
    def build(self, project_dir: Path, configuration: str) -> bool:
        """Build Windows app"""
        print(f"Building Windows project ({configuration})...")
        
        csproj = list(project_dir.glob("*.csproj"))[0]
        
        cmd = [
            "dotnet", "build",
            str(csproj),
            "-c", configuration.capitalize()
        ]
        
        return self._run_command(cmd, project_dir)
    
    def run(self, project_dir: Path, device: Optional[str]) -> bool:
        """Run Windows app"""
        print("Running Windows application...")
        
        csproj = list(project_dir.glob("*.csproj"))[0]
        
        cmd = [
            "dotnet", "run",
            "--project", str(csproj)
        ]
        
        return self._run_command(cmd, project_dir)
    
    def test(self, project_dir: Path) -> bool:
        """Run Windows tests"""
        print("Running Windows tests...")
        
        test_proj = list(project_dir.glob("*.Tests/*.csproj"))[0]
        
        cmd = [
            "dotnet", "test",
            str(test_proj)
        ]
        
        return self._run_command(cmd, project_dir)
    
    def deploy(self, project_dir: Path, target: str) -> bool:
        """Deploy Windows app"""
        print(f"Deploying Windows app to {target}...")
        
        csproj = list(project_dir.glob("*.csproj"))[0]
        
        cmd = [
            "dotnet", "publish",
            str(csproj),
            "-c", "Release",
            "-r", "win-x64",
            "--self-contained"
        ]
        
        return self._run_command(cmd, project_dir)
    
    def list_devices(self) -> List[Dict[str, Any]]:
        """List Windows devices (always just local machine)"""
        return [{'name': 'Local PC', 'type': 'physical'}]


class WebBuilder(PlatformBuilder):
    """Web platform builder"""
    
    def build(self, project_dir: Path, configuration: str) -> bool:
        """Build web app"""
        print(f"Building web project ({configuration})...")
        
        # Install dependencies if needed
        if not (project_dir / "node_modules").exists():
            if not self._run_command(["npm", "install"], project_dir):
                return False
        
        # Build
        script = "build" if configuration == "release" else "build:dev"
        return self._run_command(["npm", "run", script], project_dir)
    
    def run(self, project_dir: Path, device: Optional[str]) -> bool:
        """Run web dev server"""
        print("Starting web development server...")
        
        # Install dependencies if needed
        if not (project_dir / "node_modules").exists():
            if not self._run_command(["npm", "install"], project_dir):
                return False
        
        print("Starting server at http://localhost:8080")
        print("Hot reload enabled. Press Ctrl+C to stop.")
        
        return self._run_command(["npm", "run", "dev"], project_dir)
    
    def test(self, project_dir: Path) -> bool:
        """Run web tests"""
        print("Running web tests...")
        
        return self._run_command(["npm", "run", "test"], project_dir)
    
    def deploy(self, project_dir: Path, target: str) -> bool:
        """Deploy web app"""
        print(f"Deploying web app to {target}...")
        
        # Build production
        if not self.build(project_dir, "release"):
            return False
        
        print(f"Build artifacts ready in: {project_dir / 'dist'}")
        print(f"Deploy to {target} using your preferred method")
        
        return True
    
    def list_devices(self) -> List[Dict[str, Any]]:
        """List web browsers"""
        browsers = []
        
        if sys.platform == "win32":
            browsers = [
                {'name': 'Chrome', 'type': 'browser'},
                {'name': 'Edge', 'type': 'browser'},
                {'name': 'Firefox', 'type': 'browser'}
            ]
        elif sys.platform == "darwin":
            browsers = [
                {'name': 'Safari', 'type': 'browser'},
                {'name': 'Chrome', 'type': 'browser'},
                {'name': 'Firefox', 'type': 'browser'}
            ]
        else:
            browsers = [
                {'name': 'Chrome', 'type': 'browser'},
                {'name': 'Firefox', 'type': 'browser'}
            ]
        
        return browsers
