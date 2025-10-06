"""
Platform Detection and Management Module

Provides unified platform detection and capability management for PohLang applications
across Windows, macOS, Linux, Android, and iOS.
"""

import platform
import sys
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from enum import Enum


class PlatformType(Enum):
    """Enumeration of supported platforms."""
    WINDOWS = "windows"
    MACOS = "macos"
    LINUX = "linux"
    ANDROID = "android"
    IOS = "ios"
    WEB = "web"
    UNKNOWN = "unknown"


class PlatformCapability(Enum):
    """Platform capabilities."""
    FILESYSTEM = "filesystem"
    NETWORK = "network"
    CAMERA = "camera"
    MICROPHONE = "microphone"
    LOCATION = "location"
    NOTIFICATIONS = "notifications"
    SENSORS = "sensors"
    BLUETOOTH = "bluetooth"
    NFC = "nfc"
    BIOMETRIC = "biometric"
    TELEPHONY = "telephony"
    SMS = "sms"
    CONTACTS = "contacts"
    CALENDAR = "calendar"
    PHOTOS = "photos"
    NATIVE_UI = "native_ui"
    BACKGROUND_TASKS = "background_tasks"
    SYSTEM_SETTINGS = "system_settings"


class PlatformInfo:
    """Detailed platform information."""
    
    def __init__(self):
        self.type = self._detect_platform()
        self.system = platform.system()
        self.release = platform.release()
        self.version = platform.version()
        self.machine = platform.machine()
        self.processor = platform.processor()
        self.python_version = platform.python_version()
        self.is_mobile = self.type in [PlatformType.ANDROID, PlatformType.IOS]
        self.is_desktop = self.type in [PlatformType.WINDOWS, PlatformType.MACOS, PlatformType.LINUX]
        self.capabilities = self._detect_capabilities()
    
    def _detect_platform(self) -> PlatformType:
        """Detect the current platform."""
        system = platform.system().lower()
        
        # Check for Android
        if 'ANDROID_ROOT' in os.environ or 'ANDROID_DATA' in os.environ:
            return PlatformType.ANDROID
        
        # Check for iOS (when running under Pythonista or similar)
        if sys.platform == 'ios' or 'iOS' in platform.platform():
            return PlatformType.IOS
        
        # Desktop platforms
        if 'windows' in system:
            return PlatformType.WINDOWS
        elif 'darwin' in system or 'macos' in system:
            return PlatformType.MACOS
        elif 'linux' in system:
            return PlatformType.LINUX
        
        return PlatformType.UNKNOWN
    
    def _detect_capabilities(self) -> Dict[PlatformCapability, bool]:
        """Detect available platform capabilities."""
        caps = {}
        
        # All platforms have filesystem and network
        caps[PlatformCapability.FILESYSTEM] = True
        caps[PlatformCapability.NETWORK] = True
        
        if self.type == PlatformType.ANDROID:
            # Android has most capabilities
            caps[PlatformCapability.CAMERA] = True
            caps[PlatformCapability.MICROPHONE] = True
            caps[PlatformCapability.LOCATION] = True
            caps[PlatformCapability.NOTIFICATIONS] = True
            caps[PlatformCapability.SENSORS] = True
            caps[PlatformCapability.BLUETOOTH] = True
            caps[PlatformCapability.NFC] = True
            caps[PlatformCapability.BIOMETRIC] = True
            caps[PlatformCapability.TELEPHONY] = True
            caps[PlatformCapability.SMS] = True
            caps[PlatformCapability.CONTACTS] = True
            caps[PlatformCapability.CALENDAR] = True
            caps[PlatformCapability.PHOTOS] = True
            caps[PlatformCapability.NATIVE_UI] = True
            caps[PlatformCapability.BACKGROUND_TASKS] = True
            caps[PlatformCapability.SYSTEM_SETTINGS] = True
        
        elif self.type == PlatformType.IOS:
            # iOS has similar capabilities
            caps[PlatformCapability.CAMERA] = True
            caps[PlatformCapability.MICROPHONE] = True
            caps[PlatformCapability.LOCATION] = True
            caps[PlatformCapability.NOTIFICATIONS] = True
            caps[PlatformCapability.SENSORS] = True
            caps[PlatformCapability.BLUETOOTH] = True
            caps[PlatformCapability.NFC] = True
            caps[PlatformCapability.BIOMETRIC] = True
            caps[PlatformCapability.TELEPHONY] = False  # Limited on iOS
            caps[PlatformCapability.SMS] = True  # Via MessageUI
            caps[PlatformCapability.CONTACTS] = True
            caps[PlatformCapability.CALENDAR] = True
            caps[PlatformCapability.PHOTOS] = True
            caps[PlatformCapability.NATIVE_UI] = True
            caps[PlatformCapability.BACKGROUND_TASKS] = True
            caps[PlatformCapability.SYSTEM_SETTINGS] = False
        
        else:  # Desktop platforms
            # Limited mobile-specific features
            caps[PlatformCapability.CAMERA] = True  # Available but different APIs
            caps[PlatformCapability.MICROPHONE] = True
            caps[PlatformCapability.LOCATION] = False
            caps[PlatformCapability.NOTIFICATIONS] = True
            caps[PlatformCapability.SENSORS] = False
            caps[PlatformCapability.BLUETOOTH] = True
            caps[PlatformCapability.NFC] = False
            caps[PlatformCapability.BIOMETRIC] = False
            caps[PlatformCapability.TELEPHONY] = False
            caps[PlatformCapability.SMS] = False
            caps[PlatformCapability.CONTACTS] = False
            caps[PlatformCapability.CALENDAR] = False
            caps[PlatformCapability.PHOTOS] = True
            caps[PlatformCapability.NATIVE_UI] = True
            caps[PlatformCapability.BACKGROUND_TASKS] = True
            caps[PlatformCapability.SYSTEM_SETTINGS] = False
        
        return caps
    
    def has_capability(self, capability: PlatformCapability) -> bool:
        """Check if platform has a specific capability."""
        return self.capabilities.get(capability, False)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            'type': self.type.value,
            'system': self.system,
            'release': self.release,
            'version': self.version,
            'machine': self.machine,
            'processor': self.processor,
            'python_version': self.python_version,
            'is_mobile': self.is_mobile,
            'is_desktop': self.is_desktop,
            'capabilities': {cap.value: available for cap, available in self.capabilities.items()}
        }


# Global platform instance
_platform_info: Optional[PlatformInfo] = None


def get_platform_info() -> PlatformInfo:
    """Get the global platform information instance."""
    global _platform_info
    if _platform_info is None:
        _platform_info = PlatformInfo()
    return _platform_info


def is_android() -> bool:
    """Check if running on Android."""
    return get_platform_info().type == PlatformType.ANDROID


def is_ios() -> bool:
    """Check if running on iOS."""
    return get_platform_info().type == PlatformType.IOS


def is_mobile() -> bool:
    """Check if running on a mobile platform."""
    return get_platform_info().is_mobile


def is_desktop() -> bool:
    """Check if running on a desktop platform."""
    return get_platform_info().is_desktop


def get_platform_type() -> PlatformType:
    """Get the current platform type."""
    return get_platform_info().type


def has_capability(capability: PlatformCapability) -> bool:
    """Check if current platform has a specific capability."""
    return get_platform_info().has_capability(capability)


__all__ = [
    'PlatformType',
    'PlatformCapability',
    'PlatformInfo',
    'get_platform_info',
    'is_android',
    'is_ios',
    'is_mobile',
    'is_desktop',
    'get_platform_type',
    'has_capability',
]
