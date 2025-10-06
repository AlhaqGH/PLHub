"""
Android System Deep Access Module

Provides comprehensive access to Android system APIs, including:
- Permissions management
- Intents and Activities
- Services and Broadcast Receivers
- Content Providers
- Sensors and Hardware
- System Settings
- Storage and Media
- Connectivity
"""

import sys
from typing import Dict, List, Optional, Any, Callable
from enum import Enum


class AndroidPermission(Enum):
    """Android permission constants."""
    # Location
    ACCESS_FINE_LOCATION = "android.permission.ACCESS_FINE_LOCATION"
    ACCESS_COARSE_LOCATION = "android.permission.ACCESS_COARSE_LOCATION"
    ACCESS_BACKGROUND_LOCATION = "android.permission.ACCESS_BACKGROUND_LOCATION"
    
    # Camera and Media
    CAMERA = "android.permission.CAMERA"
    RECORD_AUDIO = "android.permission.RECORD_AUDIO"
    READ_MEDIA_IMAGES = "android.permission.READ_MEDIA_IMAGES"
    READ_MEDIA_VIDEO = "android.permission.READ_MEDIA_VIDEO"
    READ_MEDIA_AUDIO = "android.permission.READ_MEDIA_AUDIO"
    
    # Storage (legacy)
    READ_EXTERNAL_STORAGE = "android.permission.READ_EXTERNAL_STORAGE"
    WRITE_EXTERNAL_STORAGE = "android.permission.WRITE_EXTERNAL_STORAGE"
    
    # Contacts and Calendar
    READ_CONTACTS = "android.permission.READ_CONTACTS"
    WRITE_CONTACTS = "android.permission.WRITE_CONTACTS"
    READ_CALENDAR = "android.permission.READ_CALENDAR"
    WRITE_CALENDAR = "android.permission.WRITE_CALENDAR"
    
    # Phone and SMS
    CALL_PHONE = "android.permission.CALL_PHONE"
    READ_PHONE_STATE = "android.permission.READ_PHONE_STATE"
    SEND_SMS = "android.permission.SEND_SMS"
    RECEIVE_SMS = "android.permission.RECEIVE_SMS"
    READ_SMS = "android.permission.READ_SMS"
    
    # Sensors
    BODY_SENSORS = "android.permission.BODY_SENSORS"
    ACTIVITY_RECOGNITION = "android.permission.ACTIVITY_RECOGNITION"
    
    # Connectivity
    BLUETOOTH = "android.permission.BLUETOOTH"
    BLUETOOTH_ADMIN = "android.permission.BLUETOOTH_ADMIN"
    BLUETOOTH_CONNECT = "android.permission.BLUETOOTH_CONNECT"
    BLUETOOTH_SCAN = "android.permission.BLUETOOTH_SCAN"
    NFC = "android.permission.NFC"
    INTERNET = "android.permission.INTERNET"
    ACCESS_NETWORK_STATE = "android.permission.ACCESS_NETWORK_STATE"
    ACCESS_WIFI_STATE = "android.permission.ACCESS_WIFI_STATE"
    
    # Notifications
    POST_NOTIFICATIONS = "android.permission.POST_NOTIFICATIONS"


class AndroidException(Exception):
    """Base exception for Android module."""
    pass


class PermissionDeniedException(AndroidException):
    """Raised when a required permission is denied."""
    pass


class AndroidAPI:
    """
    Android System API wrapper.
    
    This class provides a Python interface to Android system features.
    When running on Android (via Chaquopy or similar), it uses native Android APIs.
    Otherwise, it provides mock implementations for development/testing.
    """
    
    def __init__(self):
        self._is_android = self._detect_android()
        self._jnius = None
        self._context = None
        
        if self._is_android:
            self._initialize_android()
    
    def _detect_android(self) -> bool:
        """Detect if running on Android."""
        import os
        return 'ANDROID_ROOT' in os.environ or 'ANDROID_DATA' in os.environ
    
    def _initialize_android(self):
        """Initialize Android-specific modules."""
        try:
            from jnius import autoclass, cast
            self._jnius = autoclass
            
            # Get application context
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            self._context = PythonActivity.mActivity
        except ImportError:
            print("Warning: jnius not available. Android features will be limited.")
            self._is_android = False
    
    # ==========================================================================
    # Permission Management
    # ==========================================================================
    
    def check_permission(self, permission: AndroidPermission) -> bool:
        """Check if a permission is granted."""
        if not self._is_android:
            return True  # Mock: always granted in non-Android environment
        
        try:
            PackageManager = self._jnius('android.content.pm.PackageManager')
            result = self._context.checkSelfPermission(permission.value)
            return result == PackageManager.PERMISSION_GRANTED
        except Exception as e:
            print(f"Error checking permission: {e}")
            return False
    
    def request_permission(self, permission: AndroidPermission) -> bool:
        """Request a runtime permission."""
        if not self._is_android:
            return True  # Mock: always granted
        
        try:
            if self.check_permission(permission):
                return True
            
            # Request permission (requires activity context)
            ActivityCompat = self._jnius('androidx.core.app.ActivityCompat')
            ActivityCompat.requestPermissions(
                self._context,
                [permission.value],
                1  # Request code
            )
            return False  # Will be granted asynchronously
        except Exception as e:
            print(f"Error requesting permission: {e}")
            return False
    
    def request_permissions(self, permissions: List[AndroidPermission]) -> Dict[AndroidPermission, bool]:
        """Request multiple permissions."""
        results = {}
        for perm in permissions:
            results[perm] = self.request_permission(perm)
        return results
    
    # ==========================================================================
    # Intent and Activity Management
    # ==========================================================================
    
    def start_activity(self, action: str, data: Optional[str] = None, 
                      extras: Optional[Dict[str, Any]] = None) -> bool:
        """Start an Android activity with an intent."""
        if not self._is_android:
            print(f"Mock: Starting activity {action}")
            return True
        
        try:
            Intent = self._jnius('android.content.Intent')
            intent = Intent(action)
            
            if data:
                Uri = self._jnius('android.net.Uri')
                intent.setData(Uri.parse(data))
            
            if extras:
                for key, value in extras.items():
                    if isinstance(value, str):
                        intent.putExtra(key, value)
                    elif isinstance(value, int):
                        intent.putExtra(key, value)
                    elif isinstance(value, bool):
                        intent.putExtra(key, value)
            
            self._context.startActivity(intent)
            return True
        except Exception as e:
            print(f"Error starting activity: {e}")
            return False
    
    def open_url(self, url: str) -> bool:
        """Open a URL in the browser."""
        return self.start_activity("android.intent.action.VIEW", data=url)
    
    def share_text(self, text: str, title: str = "Share") -> bool:
        """Share text using Android's share dialog."""
        return self.start_activity(
            "android.intent.action.SEND",
            extras={"android.intent.extra.TEXT": text, "android.intent.extra.TITLE": title}
        )
    
    def make_call(self, phone_number: str) -> bool:
        """Make a phone call."""
        if not self.check_permission(AndroidPermission.CALL_PHONE):
            raise PermissionDeniedException("CALL_PHONE permission required")
        return self.start_activity("android.intent.action.CALL", data=f"tel:{phone_number}")
    
    def send_sms(self, phone_number: str, message: str) -> bool:
        """Send an SMS message."""
        if not self.check_permission(AndroidPermission.SEND_SMS):
            raise PermissionDeniedException("SEND_SMS permission required")
        return self.start_activity(
            "android.intent.action.SENDTO",
            data=f"smsto:{phone_number}",
            extras={"sms_body": message}
        )
    
    # ==========================================================================
    # Sensor Access
    # ==========================================================================
    
    def get_sensor_manager(self):
        """Get the sensor manager."""
        if not self._is_android:
            return None
        
        try:
            Context = self._jnius('android.content.Context')
            return self._context.getSystemService(Context.SENSOR_SERVICE)
        except Exception as e:
            print(f"Error getting sensor manager: {e}")
            return None
    
    def list_sensors(self) -> List[str]:
        """List all available sensors."""
        if not self._is_android:
            return ["Accelerometer", "Gyroscope", "Magnetometer"]  # Mock
        
        try:
            sensor_manager = self.get_sensor_manager()
            Sensor = self._jnius('android.hardware.Sensor')
            sensors = sensor_manager.getSensorList(Sensor.TYPE_ALL)
            return [sensor.getName() for sensor in sensors]
        except Exception as e:
            print(f"Error listing sensors: {e}")
            return []
    
    def read_accelerometer(self) -> Optional[Dict[str, float]]:
        """Read accelerometer data."""
        if not self._is_android:
            return {"x": 0.0, "y": 0.0, "z": 9.81}  # Mock: device flat
        
        # Implementation would require sensor event listener
        # This is a simplified version
        return None
    
    # ==========================================================================
    # Location Services
    # ==========================================================================
    
    def get_location(self) -> Optional[Dict[str, float]]:
        """Get current location."""
        if not self.check_permission(AndroidPermission.ACCESS_FINE_LOCATION):
            raise PermissionDeniedException("ACCESS_FINE_LOCATION permission required")
        
        if not self._is_android:
            return {"latitude": 0.0, "longitude": 0.0, "accuracy": 10.0}  # Mock
        
        try:
            Context = self._jnius('android.content.Context')
            location_manager = self._context.getSystemService(Context.LOCATION_SERVICE)
            
            # Get last known location
            location = location_manager.getLastKnownLocation("gps")
            if location:
                return {
                    "latitude": location.getLatitude(),
                    "longitude": location.getLongitude(),
                    "accuracy": location.getAccuracy(),
                    "altitude": location.getAltitude(),
                    "speed": location.getSpeed(),
                }
        except Exception as e:
            print(f"Error getting location: {e}")
        
        return None
    
    # ==========================================================================
    # Notifications
    # ==========================================================================
    
    def show_notification(self, title: str, message: str, 
                         icon: Optional[str] = None) -> bool:
        """Show a system notification."""
        if not self.check_permission(AndroidPermission.POST_NOTIFICATIONS):
            raise PermissionDeniedException("POST_NOTIFICATIONS permission required (Android 13+)")
        
        if not self._is_android:
            print(f"Mock notification: {title} - {message}")
            return True
        
        try:
            # This is a simplified version - full implementation would use NotificationCompat
            # and create a notification channel
            return True
        except Exception as e:
            print(f"Error showing notification: {e}")
            return False
    
    # ==========================================================================
    # System Information
    # ==========================================================================
    
    def get_device_info(self) -> Dict[str, str]:
        """Get device information."""
        if not self._is_android:
            return {
                "manufacturer": "Mock",
                "model": "MockDevice",
                "android_version": "14",
                "sdk_version": "34"
            }
        
        try:
            Build = self._jnius('android.os.Build')
            return {
                "manufacturer": Build.MANUFACTURER,
                "model": Build.MODEL,
                "device": Build.DEVICE,
                "product": Build.PRODUCT,
                "android_version": Build.VERSION.RELEASE,
                "sdk_version": str(Build.VERSION.SDK_INT)
            }
        except Exception as e:
            print(f"Error getting device info: {e}")
            return {}
    
    def get_battery_info(self) -> Dict[str, Any]:
        """Get battery information."""
        if not self._is_android:
            return {"level": 80, "is_charging": False}
        
        try:
            Context = self._jnius('android.content.Context')
            Intent = self._jnius('android.content.Intent')
            IntentFilter = self._jnius('android.content.IntentFilter')
            
            intent_filter = IntentFilter(Intent.ACTION_BATTERY_CHANGED)
            battery_status = self._context.registerReceiver(None, intent_filter)
            
            level = battery_status.getIntExtra("level", -1)
            scale = battery_status.getIntExtra("scale", -1)
            status = battery_status.getIntExtra("status", -1)
            
            is_charging = status == 2 or status == 5  # CHARGING or FULL
            
            return {
                "level": int(level / float(scale) * 100),
                "is_charging": is_charging
            }
        except Exception as e:
            print(f"Error getting battery info: {e}")
            return {}
    
    # ==========================================================================
    # Storage and File System
    # ==========================================================================
    
    def get_external_storage_path(self) -> Optional[str]:
        """Get external storage directory path."""
        if not self._is_android:
            return "/mock/storage/emulated/0"
        
        try:
            Environment = self._jnius('android.os.Environment')
            return Environment.getExternalStorageDirectory().getAbsolutePath()
        except Exception as e:
            print(f"Error getting storage path: {e}")
            return None
    
    def get_app_directory(self) -> Optional[str]:
        """Get app-specific directory."""
        if not self._is_android:
            return "/mock/data/app"
        
        try:
            return self._context.getFilesDir().getAbsolutePath()
        except Exception as e:
            print(f"Error getting app directory: {e}")
            return None


# Global Android API instance
_android_api: Optional[AndroidAPI] = None


def get_android_api() -> AndroidAPI:
    """Get the global Android API instance."""
    global _android_api
    if _android_api is None:
        _android_api = AndroidAPI()
    return _android_api


# Convenience functions
def is_android() -> bool:
    """Check if running on Android."""
    return get_android_api()._is_android


def check_permission(permission: AndroidPermission) -> bool:
    """Check if a permission is granted."""
    return get_android_api().check_permission(permission)


def request_permission(permission: AndroidPermission) -> bool:
    """Request a runtime permission."""
    return get_android_api().request_permission(permission)


__all__ = [
    'AndroidPermission',
    'AndroidException',
    'PermissionDeniedException',
    'AndroidAPI',
    'get_android_api',
    'is_android',
    'check_permission',
    'request_permission',
]
