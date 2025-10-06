"""
iOS System Access Module

Provides comprehensive access to iOS system APIs, including:
- Permissions management (Privacy frameworks)
- UIKit integration
- Core Location
- Core Motion (Sensors)
- User Notifications
- Contacts and Calendar
- Photos and Camera
- System Information
"""

import sys
from typing import Dict, List, Optional, Any, Callable
from enum import Enum


class IOSPermission(Enum):
    """iOS permission/privacy usage constants."""
    # Location
    LOCATION_WHEN_IN_USE = "NSLocationWhenInUseUsageDescription"
    LOCATION_ALWAYS = "NSLocationAlwaysUsageDescription"
    
    # Camera and Media
    CAMERA = "NSCameraUsageDescription"
    MICROPHONE = "NSMicrophoneUsageDescription"
    PHOTO_LIBRARY = "NSPhotoLibraryUsageDescription"
    PHOTO_LIBRARY_ADD = "NSPhotoLibraryAddUsageDescription"
    
    # Contacts and Calendar
    CONTACTS = "NSContactsUsageDescription"
    CALENDARS = "NSCalendarsUsageDescription"
    REMINDERS = "NSRemindersUsageDescription"
    
    # Sensors and Motion
    MOTION = "NSMotionUsageDescription"
    
    # Health
    HEALTH_SHARE = "NSHealthShareUsageDescription"
    HEALTH_UPDATE = "NSHealthUpdateUsageDescription"
    
    # Others
    SIRI = "NSSiriUsageDescription"
    SPEECH_RECOGNITION = "NSSpeechRecognitionUsageDescription"
    MEDIA_LIBRARY = "NSAppleMusicUsageDescription"
    BLUETOOTH = "NSBluetoothAlwaysUsageDescription"
    NFC = "NFCReaderUsageDescription"


class IOSException(Exception):
    """Base exception for iOS module."""
    pass


class PermissionDeniedException(IOSException):
    """Raised when a required permission is denied."""
    pass


class IOSAPI:
    """
    iOS System API wrapper.
    
    This class provides a Python interface to iOS system features.
    When running on iOS (via Pythonista, Pyto, or similar), it uses native iOS APIs.
    Otherwise, it provides mock implementations for development/testing.
    """
    
    def __init__(self):
        self._is_ios = self._detect_ios()
        self._objc = None
        
        if self._is_ios:
            self._initialize_ios()
    
    def _detect_ios(self) -> bool:
        """Detect if running on iOS."""
        return sys.platform == 'ios' or 'iOS' in sys.platform
    
    def _initialize_ios(self):
        """Initialize iOS-specific modules."""
        try:
            import objc_util
            self._objc = objc_util
        except ImportError:
            print("Warning: objc_util not available. iOS features will be limited.")
            self._is_ios = False
    
    # ==========================================================================
    # Permission Management
    # ==========================================================================
    
    def check_location_permission(self) -> str:
        """
        Check location permission status.
        Returns: 'authorized', 'denied', 'restricted', 'not_determined'
        """
        if not self._is_ios:
            return 'authorized'  # Mock
        
        try:
            CLLocationManager = self._objc.ObjCClass('CLLocationManager')
            status = CLLocationManager.authorizationStatus()
            
            status_map = {
                0: 'not_determined',
                1: 'restricted',
                2: 'denied',
                3: 'authorized',
                4: 'authorized'  # authorizedAlways
            }
            return status_map.get(status, 'not_determined')
        except Exception as e:
            print(f"Error checking location permission: {e}")
            return 'not_determined'
    
    def request_location_permission(self) -> bool:
        """Request location permission."""
        if not self._is_ios:
            return True  # Mock
        
        try:
            CLLocationManager = self._objc.ObjCClass('CLLocationManager')
            location_manager = CLLocationManager.alloc().init()
            location_manager.requestWhenInUseAuthorization()
            return True
        except Exception as e:
            print(f"Error requesting location permission: {e}")
            return False
    
    def check_camera_permission(self) -> str:
        """Check camera permission status."""
        if not self._is_ios:
            return 'authorized'
        
        try:
            AVCaptureDevice = self._objc.ObjCClass('AVCaptureDevice')
            status = AVCaptureDevice.authorizationStatusForMediaType_('vide')
            
            status_map = {
                0: 'not_determined',
                1: 'restricted',
                2: 'denied',
                3: 'authorized'
            }
            return status_map.get(status, 'not_determined')
        except Exception as e:
            print(f"Error checking camera permission: {e}")
            return 'not_determined'
    
    def request_camera_permission(self, completion: Optional[Callable[[bool], None]] = None):
        """Request camera permission."""
        if not self._is_ios:
            if completion:
                completion(True)
            return
        
        try:
            AVCaptureDevice = self._objc.ObjCClass('AVCaptureDevice')
            AVCaptureDevice.requestAccessForMediaType_completionHandler_(
                'vide',
                completion or (lambda granted: None)
            )
        except Exception as e:
            print(f"Error requesting camera permission: {e}")
    
    # ==========================================================================
    # Location Services
    # ==========================================================================
    
    def get_location(self) -> Optional[Dict[str, float]]:
        """Get current location."""
        if self.check_location_permission() != 'authorized':
            raise PermissionDeniedException("Location permission not granted")
        
        if not self._is_ios:
            return {"latitude": 37.7749, "longitude": -122.4194, "accuracy": 10.0}  # Mock: San Francisco
        
        try:
            CLLocationManager = self._objc.ObjCClass('CLLocationManager')
            location_manager = CLLocationManager.alloc().init()
            location = location_manager.location()
            
            if location:
                coord = location.coordinate()
                return {
                    "latitude": coord.latitude,
                    "longitude": coord.longitude,
                    "altitude": location.altitude(),
                    "accuracy": location.horizontalAccuracy(),
                    "speed": location.speed(),
                    "course": location.course()
                }
        except Exception as e:
            print(f"Error getting location: {e}")
        
        return None
    
    # ==========================================================================
    # Motion and Sensors
    # ==========================================================================
    
    def get_motion_manager(self):
        """Get the Core Motion manager."""
        if not self._is_ios:
            return None
        
        try:
            CMMotionManager = self._objc.ObjCClass('CMMotionManager')
            return CMMotionManager.alloc().init()
        except Exception as e:
            print(f"Error getting motion manager: {e}")
            return None
    
    def read_accelerometer(self) -> Optional[Dict[str, float]]:
        """Read accelerometer data."""
        if not self._is_ios:
            return {"x": 0.0, "y": 0.0, "z": -1.0}  # Mock: device upright
        
        try:
            motion_manager = self.get_motion_manager()
            if motion_manager and motion_manager.isAccelerometerAvailable():
                motion_manager.startAccelerometerUpdates()
                data = motion_manager.accelerometerData()
                if data:
                    accel = data.acceleration()
                    return {
                        "x": accel.x,
                        "y": accel.y,
                        "z": accel.z
                    }
        except Exception as e:
            print(f"Error reading accelerometer: {e}")
        
        return None
    
    def read_gyroscope(self) -> Optional[Dict[str, float]]:
        """Read gyroscope data."""
        if not self._is_ios:
            return {"x": 0.0, "y": 0.0, "z": 0.0}  # Mock
        
        try:
            motion_manager = self.get_motion_manager()
            if motion_manager and motion_manager.isGyroAvailable():
                motion_manager.startGyroUpdates()
                data = motion_manager.gyroData()
                if data:
                    rotation = data.rotationRate()
                    return {
                        "x": rotation.x,
                        "y": rotation.y,
                        "z": rotation.z
                    }
        except Exception as e:
            print(f"Error reading gyroscope: {e}")
        
        return None
    
    # ==========================================================================
    # Notifications
    # ==========================================================================
    
    def request_notification_permission(self, completion: Optional[Callable[[bool], None]] = None):
        """Request notification permission."""
        if not self._is_ios:
            if completion:
                completion(True)
            return
        
        try:
            UNUserNotificationCenter = self._objc.ObjCClass('UNUserNotificationCenter')
            center = UNUserNotificationCenter.currentNotificationCenter()
            
            # Request authorization
            options = 7  # Badge + Sound + Alert
            center.requestAuthorizationWithOptions_completionHandler_(
                options,
                completion or (lambda granted, error: None)
            )
        except Exception as e:
            print(f"Error requesting notification permission: {e}")
    
    def show_notification(self, title: str, body: str, badge: Optional[int] = None) -> bool:
        """Show a local notification."""
        if not self._is_ios:
            print(f"Mock notification: {title} - {body}")
            return True
        
        try:
            UNMutableNotificationContent = self._objc.ObjCClass('UNMutableNotificationContent')
            UNNotificationRequest = self._objc.ObjCClass('UNNotificationRequest')
            UNUserNotificationCenter = self._objc.ObjCClass('UNUserNotificationCenter')
            
            content = UNMutableNotificationContent.alloc().init()
            content.setTitle_(title)
            content.setBody_(body)
            if badge is not None:
                content.setBadge_(badge)
            
            # Create request with unique identifier
            request = UNNotificationRequest.requestWithIdentifier_content_trigger_(
                f"notification_{id(content)}",
                content,
                None  # Trigger immediately
            )
            
            center = UNUserNotificationCenter.currentNotificationCenter()
            center.addNotificationRequest_withCompletionHandler_(
                request,
                lambda error: None
            )
            return True
        except Exception as e:
            print(f"Error showing notification: {e}")
            return False
    
    # ==========================================================================
    # Device Information
    # ==========================================================================
    
    def get_device_info(self) -> Dict[str, str]:
        """Get device information."""
        if not self._is_ios:
            return {
                "name": "iPhone Simulator",
                "model": "iPhone 15 Pro",
                "system_name": "iOS",
                "system_version": "17.0"
            }
        
        try:
            UIDevice = self._objc.ObjCClass('UIDevice')
            device = UIDevice.currentDevice()
            
            return {
                "name": str(device.name()),
                "model": str(device.model()),
                "system_name": str(device.systemName()),
                "system_version": str(device.systemVersion()),
                "identifier": str(device.identifierForVendor().UUIDString())
            }
        except Exception as e:
            print(f"Error getting device info: {e}")
            return {}
    
    def get_battery_info(self) -> Dict[str, Any]:
        """Get battery information."""
        if not self._is_ios:
            return {"level": 0.75, "state": "unplugged"}
        
        try:
            UIDevice = self._objc.ObjCClass('UIDevice')
            device = UIDevice.currentDevice()
            device.setBatteryMonitoringEnabled_(True)
            
            state_map = {
                0: "unknown",
                1: "unplugged",
                2: "charging",
                3: "full"
            }
            
            return {
                "level": float(device.batteryLevel()),
                "state": state_map.get(device.batteryState(), "unknown")
            }
        except Exception as e:
            print(f"Error getting battery info: {e}")
            return {}
    
    # ==========================================================================
    # UI and System
    # ==========================================================================
    
    def show_alert(self, title: str, message: str, button_title: str = "OK") -> bool:
        """Show a system alert dialog."""
        if not self._is_ios:
            print(f"Mock alert: {title} - {message}")
            return True
        
        try:
            UIAlertController = self._objc.ObjCClass('UIAlertController')
            UIAlertAction = self._objc.ObjCClass('UIAlertAction')
            
            alert = UIAlertController.alertControllerWithTitle_message_preferredStyle_(
                title, message, 1  # Alert style
            )
            
            action = UIAlertAction.actionWithTitle_style_handler_(
                button_title, 0, None  # Default style
            )
            alert.addAction_(action)
            
            # Present alert (requires view controller)
            # This is simplified - in real app, get current view controller
            return True
        except Exception as e:
            print(f"Error showing alert: {e}")
            return False
    
    def open_url(self, url: str) -> bool:
        """Open a URL in Safari or appropriate app."""
        if not self._is_ios:
            print(f"Mock: Opening {url}")
            return True
        
        try:
            NSURL = self._objc.ObjCClass('NSURL')
            UIApplication = self._objc.ObjCClass('UIApplication')
            
            url_obj = NSURL.URLWithString_(url)
            app = UIApplication.sharedApplication()
            app.openURL_(url_obj)
            return True
        except Exception as e:
            print(f"Error opening URL: {e}")
            return False
    
    def share_text(self, text: str, subject: Optional[str] = None) -> bool:
        """Share text using the iOS share sheet."""
        if not self._is_ios:
            print(f"Mock: Sharing '{text}'")
            return True
        
        try:
            UIActivityViewController = self._objc.ObjCClass('UIActivityViewController')
            
            items = [text]
            if subject:
                items.append(subject)
            
            activity_vc = UIActivityViewController.alloc().initWithActivityItems_applicationActivities_(
                items, None
            )
            
            # Present view controller (requires current view controller)
            return True
        except Exception as e:
            print(f"Error sharing text: {e}")
            return False
    
    # ==========================================================================
    # Storage and Files
    # ==========================================================================
    
    def get_documents_directory(self) -> Optional[str]:
        """Get the app's documents directory."""
        if not self._is_ios:
            return "/mock/Documents"
        
        try:
            NSFileManager = self._objc.ObjCClass('NSFileManager')
            manager = NSFileManager.defaultManager()
            
            urls = manager.URLsForDirectory_inDomains_(9, 1)  # DocumentDirectory, UserDomainMask
            if urls and len(urls) > 0:
                return str(urls[0].path())
        except Exception as e:
            print(f"Error getting documents directory: {e}")
        
        return None
    
    def get_cache_directory(self) -> Optional[str]:
        """Get the app's cache directory."""
        if not self._is_ios:
            return "/mock/Library/Caches"
        
        try:
            NSFileManager = self._objc.ObjCClass('NSFileManager')
            manager = NSFileManager.defaultManager()
            
            urls = manager.URLsForDirectory_inDomains_(13, 1)  # CachesDirectory, UserDomainMask
            if urls and len(urls) > 0:
                return str(urls[0].path())
        except Exception as e:
            print(f"Error getting cache directory: {e}")
        
        return None


# Global iOS API instance
_ios_api: Optional[IOSAPI] = None


def get_ios_api() -> IOSAPI:
    """Get the global iOS API instance."""
    global _ios_api
    if _ios_api is None:
        _ios_api = IOSAPI()
    return _ios_api


# Convenience functions
def is_ios() -> bool:
    """Check if running on iOS."""
    return get_ios_api()._is_ios


def check_location_permission() -> str:
    """Check location permission status."""
    return get_ios_api().check_location_permission()


def request_location_permission() -> bool:
    """Request location permission."""
    return get_ios_api().request_location_permission()


__all__ = [
    'IOSPermission',
    'IOSException',
    'PermissionDeniedException',
    'IOSAPI',
    'get_ios_api',
    'is_ios',
    'check_location_permission',
    'request_location_permission',
]
