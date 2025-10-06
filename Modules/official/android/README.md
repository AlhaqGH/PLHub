# Android System Deep Access Module

Comprehensive Android system API access for PohLang applications.

## Features

### 🔐 Permission Management
- Runtime permission requests
- Permission status checking
- Multi-permission handling
- Permission rationale support

### 📱 Intents and Activities
- Start activities
- Send broadcasts
- Handle intent filters
- Deep linking support

### 📡 Sensors and Hardware
- Accelerometer, Gyroscope, Magnetometer
- Proximity, Light, Temperature sensors
- Step counter and detector
- Heart rate monitor (if available)

### 📍 Location Services
- GPS location
- Network location
- Geofencing
- Location updates

### 🔔 Notifications
- Simple notifications
- Rich notifications
- Notification channels (Android 8+)
- Action buttons

### 📞 Telephony and SMS
- Make phone calls
- Send SMS messages
- Read SMS (with permission)
- Phone state monitoring

### 📷 Camera and Media
- Camera access
- Photo capture
- Video recording
- Media playback

### 💾 Storage and Files
- Internal storage
- External storage
- Scoped storage (Android 10+)
- Media store access

### 🔊 Audio
- Record audio
- Play audio
- Volume control
- Audio focus management

### 🌐 Connectivity
- Network status
- Wi-Fi management
- Bluetooth
- NFC

### 📇 Content Providers
- Contacts
- Calendar
- Call log
- Media store

## Installation

The Android module requires additional dependencies when running on Android:

```bash
# For Chaquopy (Android Python runtime)
pip install pyjnius

# Or add to requirements.txt
echo "pyjnius" >> requirements.txt
```

## Usage Examples

### Permission Management

```python
from Modules.official.android import (
    get_android_api,
    AndroidPermission,
    check_permission,
    request_permission
)

# Check permission
if check_permission(AndroidPermission.CAMERA):
    print("Camera permission granted")
else:
    # Request permission
    request_permission(AndroidPermission.CAMERA)

# Request multiple permissions
api = get_android_api()
permissions = [
    AndroidPermission.CAMERA,
    AndroidPermission.ACCESS_FINE_LOCATION,
    AndroidPermission.RECORD_AUDIO
]
results = api.request_permissions(permissions)
```

### Location Services

```python
from Modules.official.android import get_android_api, AndroidPermission

api = get_android_api()

# Request location permission first
if not check_permission(AndroidPermission.ACCESS_FINE_LOCATION):
    api.request_permission(AndroidPermission.ACCESS_FINE_LOCATION)

# Get current location
location = api.get_location()
if location:
    print(f"Latitude: {location['latitude']}")
    print(f"Longitude: {location['longitude']}")
    print(f"Accuracy: {location['accuracy']} meters")
```

### Sensors

```python
from Modules.official.android import get_android_api

api = get_android_api()

# List all available sensors
sensors = api.list_sensors()
for sensor in sensors:
    print(f"Sensor: {sensor}")

# Read accelerometer
accel_data = api.read_accelerometer()
if accel_data:
    print(f"X: {accel_data['x']}")
    print(f"Y: {accel_data['y']}")
    print(f"Z: {accel_data['z']}")
```

### Notifications

```python
from Modules.official.android import get_android_api, AndroidPermission

api = get_android_api()

# Request notification permission (Android 13+)
if not check_permission(AndroidPermission.POST_NOTIFICATIONS):
    api.request_permission(AndroidPermission.POST_NOTIFICATIONS)

# Show notification
api.show_notification(
    title="Hello from PohLang!",
    message="This is a system notification"
)
```

### Intents and Activities

```python
from Modules.official.android import get_android_api

api = get_android_api()

# Open URL in browser
api.open_url("https://github.com/AlhaqGH/PLHub")

# Share text
api.share_text("Check out PohLang!", title="Share PohLang")

# Make phone call (requires permission)
api.make_call("+1234567890")

# Send SMS
api.send_sms("+1234567890", "Hello from PohLang!")
```

### Device Information

```python
from Modules.official.android import get_android_api

api = get_android_api()

# Get device info
device_info = api.get_device_info()
print(f"Manufacturer: {device_info['manufacturer']}")
print(f"Model: {device_info['model']}")
print(f"Android Version: {device_info['android_version']}")

# Get battery info
battery = api.get_battery_info()
print(f"Battery Level: {battery['level']}%")
print(f"Charging: {battery['is_charging']}")
```

### Storage

```python
from Modules.official.android import get_android_api

api = get_android_api()

# Get external storage path
storage_path = api.get_external_storage_path()
print(f"External Storage: {storage_path}")

# Get app-specific directory
app_dir = api.get_app_directory()
print(f"App Directory: {app_dir}")
```

## PohLang Integration

Use Android features in PohLang with natural language:

```poh
Start Program

# Import Android module
Use android

# Check and request camera permission
Ask android check_permission "CAMERA"
If permission equals "no"
    Ask android request_permission "CAMERA"
End

# Get device information
Ask android for device_info
Write "Device: " plus device_info.manufacturer plus " " plus device_info.model

# Get location
Ask android for location
If location exists
    Write "Latitude: " plus location.latitude
    Write "Longitude: " plus location.longitude
End

# Show notification
Ask android show_notification with title "Hello" and message "From PohLang"

# Open URL
Ask android open_url "https://github.com/AlhaqGH/PLHub"

End Program
```

## Android Manifest Configuration

Add required permissions to your `AndroidManifest.xml`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.pohlang.app">
    
    <!-- Permissions -->
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <uses-permission android:name="android.permission.CAMERA" />
    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
    <uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
    <uses-permission android:name="android.permission.RECORD_AUDIO" />
    <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />
    <uses-permission android:name="android.permission.CALL_PHONE" />
    <uses-permission android:name="android.permission.SEND_SMS" />
    <uses-permission android:name="android.permission.READ_CONTACTS" />
    
    <!-- Features -->
    <uses-feature android:name="android.hardware.camera" android:required="false" />
    <uses-feature android:name="android.hardware.location.gps" android:required="false" />
    
    <application>
        <!-- Your app configuration -->
    </application>
</manifest>
```

## Runtime Requirements

### On Android Device

1. **Chaquopy** - Python for Android
   ```gradle
   dependencies {
       implementation 'com.chaquo.python:gradle:14.0.2'
   }
   ```

2. **PyJNIus** - Python-Java bridge
   ```bash
   pip install pyjnius
   ```

### Development/Testing

The module provides mock implementations when not running on Android, allowing you to develop and test on your desktop.

## Permission Best Practices

1. **Request permissions when needed** - Don't request all permissions at app start
2. **Explain why** - Show rationale before requesting sensitive permissions
3. **Handle denial gracefully** - Provide alternative functionality
4. **Check before use** - Always check permissions before accessing restricted APIs

## Supported Android Versions

- **Minimum**: Android 6.0 (API 23) - Runtime permissions
- **Target**: Android 14 (API 34) - Latest features
- **Recommended**: Android 10+ (API 29) - Scoped storage

## Common Issues

### Permission Denied

```python
from Modules.official.android import PermissionDeniedException

try:
    api.make_call("+1234567890")
except PermissionDeniedException as e:
    print(f"Permission denied: {e}")
    # Request permission or show rationale
```

### Context Not Available

Ensure your app runs in an Android activity context. The module automatically detects and initializes the context.

## Additional Resources

- [Android Developer Guide](https://developer.android.com/)
- [Android Permissions](https://developer.android.com/guide/topics/permissions/overview)
- [Chaquopy Documentation](https://chaquo.com/chaquopy/doc/current/)
- [PyJNIus Documentation](https://pyjnius.readthedocs.io/)
