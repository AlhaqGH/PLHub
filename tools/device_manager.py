"""
PLHub Device & Emulator Manager
Manages physical devices, emulators, and simulators for all platforms:
- Android devices and emulators (AVD)
- iOS physical devices and simulators
- macOS (local machine)
- Windows (local machine)
- Web browsers
"""

import os
import sys
import json
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


class DeviceType(Enum):
    """Types of devices"""
    PHYSICAL = "physical"
    EMULATOR = "emulator"
    SIMULATOR = "simulator"
    BROWSER = "browser"
    LOCAL = "local"


class DeviceStatus(Enum):
    """Device status"""
    ONLINE = "online"
    OFFLINE = "offline"
    BOOTING = "booting"
    UNAUTHORIZED = "unauthorized"
    UNKNOWN = "unknown"


@dataclass
class Device:
    """Represents a device"""
    id: str
    name: str
    platform: str
    device_type: DeviceType
    status: DeviceStatus
    details: Dict[str, Any]


class DeviceManager:
    """Base class for device managers"""
    
    def list_devices(self) -> List[Device]:
        """List all devices"""
        raise NotImplementedError
    
    def launch_emulator(self, name: str) -> bool:
        """Launch emulator/simulator"""
        raise NotImplementedError
    
    def stop_emulator(self, device_id: str) -> bool:
        """Stop emulator/simulator"""
        raise NotImplementedError
    
    def install_app(self, device_id: str, app_path: Path) -> bool:
        """Install app on device"""
        raise NotImplementedError
    
    def uninstall_app(self, device_id: str, package_name: str) -> bool:
        """Uninstall app from device"""
        raise NotImplementedError
    
    def get_logs(self, device_id: str) -> str:
        """Get device logs"""
        raise NotImplementedError
    
    def _run_command(self, cmd: List[str]) -> tuple[int, str, str]:
        """Run command and capture output"""
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode, result.stdout, result.stderr
        except Exception as e:
            return -1, "", str(e)


class AndroidDeviceManager(DeviceManager):
    """Manages Android devices and emulators"""
    
    def list_devices(self) -> List[Device]:
        """List Android devices and emulators"""
        devices = []
        
        # Get connected devices
        returncode, stdout, stderr = self._run_command(["adb", "devices", "-l"])
        
        if returncode == 0:
            for line in stdout.split('\n')[1:]:
                if not line.strip() or line.startswith('*'):
                    continue
                
                parts = line.split()
                if len(parts) < 2:
                    continue
                
                device_id = parts[0]
                status_str = parts[1]
                
                # Determine status
                if status_str == "device":
                    status = DeviceStatus.ONLINE
                elif status_str == "offline":
                    status = DeviceStatus.OFFLINE
                elif status_str == "unauthorized":
                    status = DeviceStatus.UNAUTHORIZED
                else:
                    status = DeviceStatus.UNKNOWN
                
                # Determine device type and name
                is_emulator = device_id.startswith("emulator-")
                device_type = DeviceType.EMULATOR if is_emulator else DeviceType.PHYSICAL
                
                # Extract model/name
                name = device_id
                for part in parts[2:]:
                    if part.startswith("model:"):
                        name = part.split(":")[1]
                        break
                
                devices.append(Device(
                    id=device_id,
                    name=name,
                    platform="android",
                    device_type=device_type,
                    status=status,
                    details={}
                ))
        
        return devices
    
    def list_emulators(self) -> List[str]:
        """List available Android emulators (AVDs)"""
        returncode, stdout, stderr = self._run_command(
            ["emulator", "-list-avds"]
        )
        
        if returncode == 0:
            return [line.strip() for line in stdout.split('\n') if line.strip()]
        return []
    
    def launch_emulator(self, name: str) -> bool:
        """Launch Android emulator"""
        print(f"Launching Android emulator: {name}")
        
        # Launch in background
        try:
            subprocess.Popen(
                ["emulator", "-avd", name],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            print("Waiting for emulator to boot...")
            time.sleep(5)  # Wait for boot
            
            # Wait for device to come online
            for i in range(60):  # Wait up to 60 seconds
                devices = self.list_devices()
                for device in devices:
                    if device.device_type == DeviceType.EMULATOR and \
                       device.status == DeviceStatus.ONLINE:
                        print(f"✓ Emulator {name} is online")
                        return True
                time.sleep(1)
            
            print("⚠️  Emulator started but not online yet")
            return True
            
        except Exception as e:
            print(f"Error launching emulator: {e}")
            return False
    
    def stop_emulator(self, device_id: str) -> bool:
        """Stop Android emulator"""
        returncode, _, _ = self._run_command(
            ["adb", "-s", device_id, "emu", "kill"]
        )
        return returncode == 0
    
    def install_app(self, device_id: str, app_path: Path) -> bool:
        """Install APK on Android device"""
        print(f"Installing app on {device_id}...")
        returncode, stdout, stderr = self._run_command(
            ["adb", "-s", device_id, "install", "-r", str(app_path)]
        )
        
        if returncode == 0:
            print("✓ App installed successfully")
            return True
        else:
            print(f"✗ Installation failed: {stderr}")
            return False
    
    def uninstall_app(self, device_id: str, package_name: str) -> bool:
        """Uninstall app from Android device"""
        returncode, _, _ = self._run_command(
            ["adb", "-s", device_id, "uninstall", package_name]
        )
        return returncode == 0
    
    def get_logs(self, device_id: str) -> str:
        """Get Android device logs"""
        returncode, stdout, _ = self._run_command(
            ["adb", "-s", device_id, "logcat", "-d", "-t", "100"]
        )
        return stdout if returncode == 0 else ""


class IOSDeviceManager(DeviceManager):
    """Manages iOS devices and simulators"""
    
    def list_devices(self) -> List[Device]:
        """List iOS devices and simulators"""
        devices = []
        
        # List simulators
        returncode, stdout, stderr = self._run_command(
            ["xcrun", "simctl", "list", "devices", "available", "--json"]
        )
        
        if returncode == 0:
            try:
                data = json.loads(stdout)
                for runtime, device_list in data.get('devices', {}).items():
                    for device_info in device_list:
                        status_str = device_info.get('state', 'Shutdown')
                        
                        if status_str == 'Booted':
                            status = DeviceStatus.ONLINE
                        elif status_str == 'Booting':
                            status = DeviceStatus.BOOTING
                        else:
                            status = DeviceStatus.OFFLINE
                        
                        devices.append(Device(
                            id=device_info['udid'],
                            name=device_info['name'],
                            platform="ios",
                            device_type=DeviceType.SIMULATOR,
                            status=status,
                            details={
                                'runtime': runtime,
                                'isAvailable': device_info.get('isAvailable', True)
                            }
                        ))
            except json.JSONDecodeError:
                pass
        
        # TODO: List physical iOS devices (requires libimobiledevice)
        
        return devices
    
    def launch_emulator(self, name: str) -> bool:
        """Launch iOS simulator"""
        print(f"Launching iOS simulator: {name}")
        
        # Find device by name
        devices = self.list_devices()
        device = next((d for d in devices if d.name == name), None)
        
        if not device:
            print(f"Simulator not found: {name}")
            return False
        
        # Boot simulator
        returncode, _, stderr = self._run_command(
            ["xcrun", "simctl", "boot", device.id]
        )
        
        if returncode == 0 or "Unable to boot device in current state: Booted" in stderr:
            # Open Simulator app
            subprocess.Popen(
                ["open", "-a", "Simulator"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print(f"✓ Simulator {name} launched")
            return True
        else:
            print(f"Error launching simulator: {stderr}")
            return False
    
    def stop_emulator(self, device_id: str) -> bool:
        """Stop iOS simulator"""
        returncode, _, _ = self._run_command(
            ["xcrun", "simctl", "shutdown", device_id]
        )
        return returncode == 0
    
    def install_app(self, device_id: str, app_path: Path) -> bool:
        """Install app on iOS simulator"""
        print(f"Installing app on simulator...")
        returncode, _, stderr = self._run_command(
            ["xcrun", "simctl", "install", device_id, str(app_path)]
        )
        
        if returncode == 0:
            print("✓ App installed successfully")
            return True
        else:
            print(f"✗ Installation failed: {stderr}")
            return False
    
    def uninstall_app(self, device_id: str, package_name: str) -> bool:
        """Uninstall app from iOS simulator"""
        returncode, _, _ = self._run_command(
            ["xcrun", "simctl", "uninstall", device_id, package_name]
        )
        return returncode == 0
    
    def get_logs(self, device_id: str) -> str:
        """Get iOS simulator logs"""
        log_path = Path.home() / "Library" / "Logs" / "CoreSimulator" / device_id
        
        if log_path.exists():
            system_log = log_path / "system.log"
            if system_log.exists():
                return system_log.read_text(encoding='utf-8', errors='ignore')
        
        return ""


class MacOSDeviceManager(DeviceManager):
    """Manages macOS (local machine)"""
    
    def list_devices(self) -> List[Device]:
        """List macOS devices (always just local machine)"""
        return [Device(
            id="local",
            name="Local Mac",
            platform="macos",
            device_type=DeviceType.LOCAL,
            status=DeviceStatus.ONLINE,
            details={}
        )]
    
    def launch_emulator(self, name: str) -> bool:
        """Not applicable for macOS"""
        return True
    
    def stop_emulator(self, device_id: str) -> bool:
        """Not applicable for macOS"""
        return True
    
    def install_app(self, device_id: str, app_path: Path) -> bool:
        """Install macOS app (copy to Applications)"""
        # Would copy .app bundle to /Applications
        return True
    
    def uninstall_app(self, device_id: str, package_name: str) -> bool:
        """Uninstall macOS app"""
        return True
    
    def get_logs(self, device_id: str) -> str:
        """Get macOS logs"""
        returncode, stdout, _ = self._run_command(
            ["log", "show", "--predicate", "processImagePath contains 'PohLang'", 
             "--last", "1h", "--style", "syslog"]
        )
        return stdout if returncode == 0 else ""


class WindowsDeviceManager(DeviceManager):
    """Manages Windows (local machine)"""
    
    def list_devices(self) -> List[Device]:
        """List Windows devices (always just local machine)"""
        return [Device(
            id="local",
            name="Local PC",
            platform="windows",
            device_type=DeviceType.LOCAL,
            status=DeviceStatus.ONLINE,
            details={}
        )]
    
    def launch_emulator(self, name: str) -> bool:
        """Not applicable for Windows"""
        return True
    
    def stop_emulator(self, device_id: str) -> bool:
        """Not applicable for Windows"""
        return True
    
    def install_app(self, device_id: str, app_path: Path) -> bool:
        """Install Windows app"""
        # Would use Windows Package Manager or installer
        return True
    
    def uninstall_app(self, device_id: str, package_name: str) -> bool:
        """Uninstall Windows app"""
        return True
    
    def get_logs(self, device_id: str) -> str:
        """Get Windows Event Logs"""
        # Would query Windows Event Log
        return ""


class WebDeviceManager(DeviceManager):
    """Manages web browsers"""
    
    def list_devices(self) -> List[Device]:
        """List available browsers"""
        browsers = []
        
        if sys.platform == "win32":
            browser_list = [
                ("Chrome", r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
                ("Edge", r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
                ("Firefox", r"C:\Program Files\Mozilla Firefox\firefox.exe")
            ]
        elif sys.platform == "darwin":
            browser_list = [
                ("Safari", "/Applications/Safari.app"),
                ("Chrome", "/Applications/Google Chrome.app"),
                ("Firefox", "/Applications/Firefox.app")
            ]
        else:
            browser_list = [
                ("Chrome", "/usr/bin/google-chrome"),
                ("Firefox", "/usr/bin/firefox")
            ]
        
        for name, path in browser_list:
            if os.path.exists(path):
                browsers.append(Device(
                    id=name.lower(),
                    name=name,
                    platform="web",
                    device_type=DeviceType.BROWSER,
                    status=DeviceStatus.ONLINE,
                    details={'path': path}
                ))
        
        return browsers
    
    def launch_emulator(self, name: str) -> bool:
        """Launch browser"""
        devices = self.list_devices()
        browser = next((d for d in devices if d.id == name.lower()), None)
        
        if not browser:
            print(f"Browser not found: {name}")
            return False
        
        browser_path = browser.details['path']
        url = "http://localhost:8080"
        
        try:
            if sys.platform == "win32":
                os.startfile(browser_path)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", "-a", browser_path, url])
            else:
                subprocess.Popen([browser_path, url])
            
            print(f"✓ Launched {browser.name}")
            return True
        except Exception as e:
            print(f"Error launching browser: {e}")
            return False
    
    def stop_emulator(self, device_id: str) -> bool:
        """Stop browser (close all instances)"""
        # Would need to find and kill browser processes
        return True
    
    def install_app(self, device_id: str, app_path: Path) -> bool:
        """Not applicable for web"""
        return True
    
    def uninstall_app(self, device_id: str, package_name: str) -> bool:
        """Not applicable for web"""
        return True
    
    def get_logs(self, device_id: str) -> str:
        """Get browser console logs (would need browser automation)"""
        return ""


class UnifiedDeviceManager:
    """Unified manager for all platforms"""
    
    def __init__(self):
        self.managers = {
            'android': AndroidDeviceManager(),
            'ios': IOSDeviceManager(),
            'macos': MacOSDeviceManager(),
            'windows': WindowsDeviceManager(),
            'web': WebDeviceManager()
        }
    
    def list_devices(self, platform: str) -> List[Device]:
        """List devices for platform"""
        manager = self.managers.get(platform)
        if not manager:
            raise ValueError(f"Unsupported platform: {platform}")
        
        return manager.list_devices()
    
    def list_all_devices(self) -> Dict[str, List[Device]]:
        """List devices for all platforms"""
        all_devices = {}
        
        for platform, manager in self.managers.items():
            try:
                devices = manager.list_devices()
                all_devices[platform] = devices
            except Exception as e:
                print(f"Error listing {platform} devices: {e}")
                all_devices[platform] = []
        
        return all_devices
    
    def launch_device(self, platform: str, device_name: str) -> bool:
        """Launch emulator/simulator/browser"""
        manager = self.managers.get(platform)
        if not manager:
            raise ValueError(f"Unsupported platform: {platform}")
        
        return manager.launch_emulator(device_name)
    
    def display_devices(self, platform: Optional[str] = None):
        """Display devices in formatted list"""
        if platform:
            platforms_to_show = {platform: self.managers[platform]}
        else:
            platforms_to_show = self.managers
        
        print("\n" + "="*70)
        print("AVAILABLE DEVICES & EMULATORS")
        print("="*70)
        
        for plat, manager in platforms_to_show.items():
            try:
                devices = manager.list_devices()
                
                print(f"\n{plat.upper()}:")
                if not devices:
                    print("  No devices found")
                else:
                    for device in devices:
                        status_icon = "●" if device.status == DeviceStatus.ONLINE else "○"
                        type_label = device.device_type.value.capitalize()
                        print(f"  {status_icon} {device.name:<30} [{type_label}] {device.status.value}")
                        
            except Exception as e:
                print(f"\n{plat.upper()}:")
                print(f"  Error: {e}")
        
        print("\n" + "="*70 + "\n")
