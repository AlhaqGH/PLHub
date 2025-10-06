# Platform Module

Unified platform detection and capability management for PohLang applications across multiple platforms.

## Supported Platforms

- **Desktop**: Windows, macOS, Linux
- **Mobile**: Android, iOS
- **Web**: Browser-based (future)

## Features

### Platform Detection
- Automatic detection of current platform
- Platform type identification
- System information retrieval

### Capability Management
- Query available platform capabilities
- Check for specific features (camera, GPS, sensors, etc.)
- Platform-specific feature flags

### Cross-Platform Abstraction
- Unified API across platforms
- Platform-specific implementations
- Graceful degradation

## Usage

```python
from Modules.official.platform import (
    get_platform_info,
    is_android,
    is_ios,
    is_mobile,
    has_capability,
    PlatformCapability
)

# Get platform information
platform = get_platform_info()
print(f"Running on: {platform.type.value}")
print(f"System: {platform.system}")
print(f"Is mobile: {platform.is_mobile}")

# Check platform type
if is_android():
    print("Running on Android")
elif is_ios():
    print("Running on iOS")

# Check capabilities
if has_capability(PlatformCapability.CAMERA):
    print("Camera is available")

if has_capability(PlatformCapability.LOCATION):
    print("Location services available")
```

## Platform Capabilities

| Capability | Windows | macOS | Linux | Android | iOS |
|------------|---------|-------|-------|---------|-----|
| Filesystem | ✅ | ✅ | ✅ | ✅ | ✅ |
| Network | ✅ | ✅ | ✅ | ✅ | ✅ |
| Camera | ✅ | ✅ | ✅ | ✅ | ✅ |
| Microphone | ✅ | ✅ | ✅ | ✅ | ✅ |
| Location | ❌ | ❌ | ❌ | ✅ | ✅ |
| Notifications | ✅ | ✅ | ✅ | ✅ | ✅ |
| Sensors | ❌ | ❌ | ❌ | ✅ | ✅ |
| Bluetooth | ✅ | ✅ | ✅ | ✅ | ✅ |
| NFC | ❌ | ❌ | ❌ | ✅ | ✅ |
| Biometric | ❌ | ❌ | ❌ | ✅ | ✅ |
| Telephony | ❌ | ❌ | ❌ | ✅ | ❌ |
| SMS | ❌ | ❌ | ❌ | ✅ | ✅ |
| Contacts | ❌ | ❌ | ❌ | ✅ | ✅ |
| Calendar | ❌ | ❌ | ❌ | ✅ | ✅ |
| Photos | ✅ | ✅ | ✅ | ✅ | ✅ |

## Integration with PohLang

The platform module integrates seamlessly with PohLang applications through natural language commands:

```poh
Start Program

# Check platform
Use platform
Ask platform for type
Write "Running on: " plus type

# Check capabilities
Ask platform if has_camera
If has_camera equals "yes"
    Write "Camera is available"
End

End Program
```
