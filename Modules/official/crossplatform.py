"""
Cross-Platform Abstraction Layer

Provides a unified API that works across all platforms (Windows, macOS, Linux, Android, iOS, Web)
with platform-specific implementations.
"""

from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from Modules.official.platform import get_platform_info, PlatformType, PlatformCapability


class FileSystem:
    """Cross-platform file system operations."""
    
    @staticmethod
    def get_app_directory() -> Path:
        """Get application-specific directory."""
        platform = get_platform_info()
        
        if platform.type == PlatformType.ANDROID:
            from Modules.official.android import get_android_api
            path = get_android_api().get_app_directory()
            return Path(path) if path else Path.home()
        
        elif platform.type == PlatformType.IOS:
            from Modules.official.ios import get_ios_api
            path = get_ios_api().get_documents_directory()
            return Path(path) if path else Path.home()
        
        else:  # Desktop platforms
            return Path.home() / '.pohlang'
    
    @staticmethod
    def get_cache_directory() -> Path:
        """Get cache directory."""
        platform = get_platform_info()
        
        if platform.type == PlatformType.ANDROID:
            # Android cache is in app directory
            return FileSystem.get_app_directory() / 'cache'
        
        elif platform.type == PlatformType.IOS:
            from Modules.official.ios import get_ios_api
            path = get_ios_api().get_cache_directory()
            return Path(path) if path else FileSystem.get_app_directory() / 'cache'
        
        else:  # Desktop
            return FileSystem.get_app_directory() / 'cache'
    
    @staticmethod
    def get_documents_directory() -> Path:
        """Get user documents directory."""
        platform = get_platform_info()
        
        if platform.type == PlatformType.ANDROID:
            from Modules.official.android import get_android_api
            path = get_android_api().get_external_storage_path()
            return Path(path) / 'Documents' if path else Path.home() / 'Documents'
        
        elif platform.type == PlatformType.IOS:
            from Modules.official.ios import get_ios_api
            path = get_ios_api().get_documents_directory()
            return Path(path) if path else Path.home() / 'Documents'
        
        else:  # Desktop
            return Path.home() / 'Documents'


class Location:
    """Cross-platform location services."""
    
    @staticmethod
    def is_available() -> bool:
        """Check if location services are available."""
        return get_platform_info().has_capability(PlatformCapability.LOCATION)
    
    @staticmethod
    def request_permission() -> bool:
        """Request location permission."""
        platform = get_platform_info()
        
        if platform.type == PlatformType.ANDROID:
            from Modules.official.android import get_android_api, AndroidPermission
            return get_android_api().request_permission(AndroidPermission.ACCESS_FINE_LOCATION)
        
        elif platform.type == PlatformType.IOS:
            from Modules.official.ios import get_ios_api
            return get_ios_api().request_location_permission()
        
        return False  # Not available on desktop
    
    @staticmethod
    def get_current_location() -> Optional[Dict[str, float]]:
        """Get current location."""
        if not Location.is_available():
            return None
        
        platform = get_platform_info()
        
        if platform.type == PlatformType.ANDROID:
            from Modules.official.android import get_android_api
            return get_android_api().get_location()
        
        elif platform.type == PlatformType.IOS:
            from Modules.official.ios import get_ios_api
            return get_ios_api().get_location()
        
        return None


class Sensors:
    """Cross-platform sensor access."""
    
    @staticmethod
    def is_available() -> bool:
        """Check if sensors are available."""
        return get_platform_info().has_capability(PlatformCapability.SENSORS)
    
    @staticmethod
    def read_accelerometer() -> Optional[Dict[str, float]]:
        """Read accelerometer data."""
        if not Sensors.is_available():
            return None
        
        platform = get_platform_info()
        
        if platform.type == PlatformType.ANDROID:
            from Modules.official.android import get_android_api
            return get_android_api().read_accelerometer()
        
        elif platform.type == PlatformType.IOS:
            from Modules.official.ios import get_ios_api
            return get_ios_api().read_accelerometer()
        
        return None
    
    @staticmethod
    def read_gyroscope() -> Optional[Dict[str, float]]:
        """Read gyroscope data."""
        if not Sensors.is_available():
            return None
        
        platform = get_platform_info()
        
        if platform.type == PlatformType.IOS:
            from Modules.official.ios import get_ios_api
            return get_ios_api().read_gyroscope()
        
        # Android implementation would be similar
        return None


class Notifications:
    """Cross-platform notifications."""
    
    @staticmethod
    def is_available() -> bool:
        """Check if notifications are available."""
        return get_platform_info().has_capability(PlatformCapability.NOTIFICATIONS)
    
    @staticmethod
    def request_permission() -> bool:
        """Request notification permission."""
        platform = get_platform_info()
        
        if platform.type == PlatformType.ANDROID:
            from Modules.official.android import get_android_api, AndroidPermission
            return get_android_api().request_permission(AndroidPermission.POST_NOTIFICATIONS)
        
        elif platform.type == PlatformType.IOS:
            from Modules.official.ios import get_ios_api
            get_ios_api().request_notification_permission()
            return True
        
        return True  # Desktop usually doesn't require permission
    
    @staticmethod
    def show(title: str, message: str, **kwargs) -> bool:
        """Show a notification."""
        if not Notifications.is_available():
            return False
        
        platform = get_platform_info()
        
        if platform.type == PlatformType.ANDROID:
            from Modules.official.android import get_android_api
            return get_android_api().show_notification(title, message)
        
        elif platform.type == PlatformType.IOS:
            from Modules.official.ios import get_ios_api
            return get_ios_api().show_notification(title, message)
        
        else:  # Desktop - could use system notifications
            print(f"Notification: {title} - {message}")
            return True


class Device:
    """Cross-platform device information."""
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        """Get device information."""
        platform = get_platform_info()
        info = platform.to_dict()
        
        # Add platform-specific details
        if platform.type == PlatformType.ANDROID:
            from Modules.official.android import get_android_api
            info.update(get_android_api().get_device_info())
        
        elif platform.type == PlatformType.IOS:
            from Modules.official.ios import get_ios_api
            info.update(get_ios_api().get_device_info())
        
        return info
    
    @staticmethod
    def get_battery() -> Optional[Dict[str, Any]]:
        """Get battery information."""
        platform = get_platform_info()
        
        if platform.type == PlatformType.ANDROID:
            from Modules.official.android import get_android_api
            return get_android_api().get_battery_info()
        
        elif platform.type == PlatformType.IOS:
            from Modules.official.ios import get_ios_api
            return get_ios_api().get_battery_info()
        
        return None


class System:
    """Cross-platform system operations."""
    
    @staticmethod
    def open_url(url: str) -> bool:
        """Open a URL in the default browser."""
        platform = get_platform_info()
        
        if platform.type == PlatformType.ANDROID:
            from Modules.official.android import get_android_api
            return get_android_api().open_url(url)
        
        elif platform.type == PlatformType.IOS:
            from Modules.official.ios import get_ios_api
            return get_ios_api().open_url(url)
        
        else:  # Desktop
            import webbrowser
            webbrowser.open(url)
            return True
    
    @staticmethod
    def share_text(text: str, title: Optional[str] = None) -> bool:
        """Share text using the system share dialog."""
        platform = get_platform_info()
        
        if platform.type == PlatformType.ANDROID:
            from Modules.official.android import get_android_api
            return get_android_api().share_text(text, title or "Share")
        
        elif platform.type == PlatformType.IOS:
            from Modules.official.ios import get_ios_api
            return get_ios_api().share_text(text, title)
        
        else:  # Desktop - copy to clipboard
            try:
                import pyperclip
                pyperclip.copy(text)
                print(f"Text copied to clipboard: {text}")
                return True
            except ImportError:
                print(f"Share: {text}")
                return False


# Convenience exports
__all__ = [
    'FileSystem',
    'Location',
    'Sensors',
    'Notifications',
    'Device',
    'System',
]
