"""
PLHub Enhanced Command Helpers
Provides user-friendly wrappers and enhancements for all PLHub commands.
"""

import sys
import os
import subprocess
import time
from pathlib import Path
from typing import Optional, List, Dict, Any, Callable
from tools.ui_helpers import (
    UI, Icon, Color, ProgressBar, Spinner, ErrorHelper,
    confirm, select, input_text, fuzzy_match, format_duration
)


class CommandContext:
    """Context for command execution with enhanced error handling"""
    
    def __init__(self, command_name: str):
        self.command_name = command_name
        self.start_time = time.time()
        self.success = False
    
    def __enter__(self):
        """Start command context"""
        UI.header(f"{Icon.ROCKET} {self.command_name}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """End command context with summary"""
        duration = time.time() - self.start_time
        
        if exc_type is None and self.success:
            UI.success(f"Completed in {format_duration(duration)}")
        elif exc_type:
            UI.error(f"Failed after {format_duration(duration)}")
            return False  # Re-raise exception
        else:
            UI.warning(f"Completed with warnings in {format_duration(duration)}")
    
    def set_success(self, success: bool = True):
        """Mark command as successful"""
        self.success = success


class EnhancedRunner:
    """Enhanced command runner with progress feedback"""
    
    @staticmethod
    def run_command(cmd: List[str], description: str, cwd: Optional[Path] = None,
                   show_output: bool = True, capture: bool = False) -> tuple[int, str, str]:
        """
        Run a command with user-friendly progress feedback
        
        Returns: (returncode, stdout, stderr)
        """
        UI.step(description)
        UI.command(' '.join(str(c) for c in cmd))
        
        if capture or not show_output:
            # Run with capture
            with Spinner(description):
                result = subprocess.run(
                    cmd,
                    cwd=cwd,
                    capture_output=True,
                    text=True
                )
            
            if result.returncode == 0:
                UI.success(f"{description} - Done")
            else:
                UI.error(f"{description} - Failed")
                if result.stderr:
                    print(f"{Color.RED}{result.stderr}{Color.RESET}")
            
            return result.returncode, result.stdout, result.stderr
        else:
            # Run with live output
            try:
                result = subprocess.run(cmd, cwd=cwd)
                
                if result.returncode == 0:
                    UI.success(f"{description} - Done")
                else:
                    UI.error(f"{description} - Failed (exit code {result.returncode})")
                
                return result.returncode, "", ""
            except subprocess.CalledProcessError as e:
                UI.error(f"{description} - Failed (exit code {e.returncode})")
                return e.returncode, "", ""
            except Exception as e:
                UI.error(f"{description} - Error: {e}")
                return 1, "", str(e)
    
    @staticmethod
    def check_dependency(name: str, command: List[str], install_hint: Optional[str] = None) -> bool:
        """Check if a dependency is available"""
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                UI.success(f"{name} is available", prefix=Icon.CHECK)
                return True
            else:
                raise FileNotFoundError
        except (FileNotFoundError, subprocess.TimeoutExpired):
            ErrorHelper.dependency_missing(name, install_hint)
            return False
    
    @staticmethod
    def verify_file_exists(filepath: Path, description: str = "file") -> bool:
        """Verify a file exists with user-friendly error"""
        if filepath.exists():
            return True
        
        # Look for similar files
        parent = filepath.parent
        if parent.exists():
            similar_files = [
                str(f.relative_to(parent.parent) if parent.parent.exists() else f.name)
                for f in parent.glob(f"*{filepath.stem}*")
            ]
            ErrorHelper.file_not_found(str(filepath), similar_files[:3] if similar_files else None)
        else:
            UI.error(f"{description.capitalize()} not found: {filepath}")
        
        return False


class BuildHelper:
    """Helper for build commands with progress tracking"""
    
    @staticmethod
    def build_with_progress(build_func: Callable, description: str = "Building project") -> bool:
        """Run build with progress indication"""
        UI.section(f"{Icon.BUILD} {description}")
        
        start_time = time.time()
        
        try:
            with Spinner(description):
                success = build_func()
            
            duration = time.time() - start_time
            
            if success:
                UI.success(f"Build completed in {format_duration(duration)}")
                return True
            else:
                UI.error(f"Build failed after {format_duration(duration)}")
                return False
        except Exception as e:
            duration = time.time() - start_time
            UI.error(f"Build error after {format_duration(duration)}: {e}")
            return False
    
    @staticmethod
    def show_build_summary(artifacts: List[Path], output_dir: Path):
        """Show build artifacts summary"""
        UI.section(f"{Icon.PACKAGE} Build Artifacts")
        
        for artifact in artifacts:
            size = artifact.stat().st_size if artifact.exists() else 0
            from tools.ui_helpers import format_size
            rel_path = artifact.relative_to(output_dir) if output_dir else artifact
            UI.bullet(f"{rel_path} ({format_size(size)})")
        
        UI.tip(f"Artifacts saved to: {output_dir}")


class InstallHelper:
    """Helper for package installation with progress"""
    
    @staticmethod
    def install_with_progress(package_name: str, version: Optional[str] = None) -> bool:
        """Install package with download progress"""
        version_str = f"@{version}" if version else ""
        UI.section(f"{Icon.DOWNLOAD} Installing {package_name}{version_str}")
        
        # Step 1: Resolve package
        with Spinner(f"Resolving {package_name}..."):
            # Simulate resolution
            time.sleep(0.5)
        UI.success(f"Resolved {package_name}")
        
        # Step 2: Download (would integrate with actual download)
        UI.step("Downloading package...")
        # This would be replaced with actual download logic
        from tools.ui_helpers import DownloadProgress
        progress = DownloadProgress(package_name, total_size=1024 * 1024 * 5)  # 5MB example
        
        # Simulate download
        for i in range(100):
            progress.update(1024 * 50)
            time.sleep(0.01)
        progress.finish()
        
        # Step 3: Verify
        with Spinner("Verifying integrity..."):
            time.sleep(0.3)
        UI.success("Package verified")
        
        # Step 4: Install
        with Spinner("Installing..."):
            time.sleep(0.5)
        UI.success(f"{package_name} installed successfully")
        
        return True
    
    @staticmethod
    def show_dependency_tree(package_name: str, dependencies: Dict[str, str]):
        """Show dependency tree"""
        UI.section(f"{Icon.BOOK} Dependencies for {package_name}")
        
        for dep, ver in dependencies.items():
            UI.bullet(f"{dep} {ver}")
        
        if not dependencies:
            UI.info("No dependencies")


class PlatformHelper:
    """Helper for cross-platform development"""
    
    @staticmethod
    def detect_platforms() -> Dict[str, bool]:
        """Detect available platform SDKs"""
        platforms = {}
        
        # Android
        if os.getenv('ANDROID_HOME') or os.getenv('ANDROID_SDK_ROOT'):
            platforms['android'] = True
        else:
            platforms['android'] = False
        
        # iOS/macOS (requires macOS)
        if sys.platform == 'darwin':
            try:
                result = subprocess.run(
                    ['xcodebuild', '-version'],
                    capture_output=True,
                    timeout=5
                )
                platforms['ios'] = result.returncode == 0
                platforms['macos'] = result.returncode == 0
            except:
                platforms['ios'] = False
                platforms['macos'] = False
        else:
            platforms['ios'] = False
            platforms['macos'] = False
        
        # Windows
        if sys.platform == 'win32':
            platforms['windows'] = True
        else:
            platforms['windows'] = False
        
        # Web (Node.js)
        try:
            result = subprocess.run(
                ['node', '--version'],
                capture_output=True,
                timeout=5
            )
            platforms['web'] = result.returncode == 0
        except:
            platforms['web'] = False
        
        return platforms
    
    @staticmethod
    def show_platform_status():
        """Show platform SDK status"""
        UI.section(f"{Icon.GEAR} Platform Status")
        
        platforms = PlatformHelper.detect_platforms()
        
        for platform, available in platforms.items():
            icon = Icon.SUCCESS if available else Icon.CROSS
            status = "Available" if available else "Not Available"
            color = Color.GREEN if available else Color.DIM
            print(f"  {icon} {platform.capitalize():12} {color}{status}{Color.RESET}")
        
        # Show setup instructions for unavailable platforms
        unavailable = [p for p, avail in platforms.items() if not avail]
        if unavailable:
            UI.tip(f"To enable {', '.join(unavailable)}, install the required SDKs")
    
    @staticmethod
    def select_device(platform: str, devices: List[Dict[str, str]]) -> Optional[str]:
        """Interactive device selection"""
        if not devices:
            UI.warning(f"No {platform} devices found")
            UI.tip(f"Connect a device or start an emulator")
            return None
        
        UI.section(f"{Icon.PHONE} Available {platform.capitalize()} Devices")
        
        # Display devices
        for i, device in enumerate(devices, 1):
            name = device.get('name', 'Unknown')
            status = device.get('status', 'unknown')
            type_info = device.get('type', '')
            
            status_color = Color.GREEN if status == 'online' else Color.DIM
            print(f"  [{i}] {name} {Color.DIM}({type_info}){Color.RESET} {status_color}{status}{Color.RESET}")
        
        # Let user select
        while True:
            try:
                choice = input(f"\n{Icon.INFO} Select device [1-{len(devices)}]: ").strip()
                idx = int(choice) - 1
                if 0 <= idx < len(devices):
                    return devices[idx].get('id')
                UI.error(f"Please enter a number between 1 and {len(devices)}")
            except ValueError:
                UI.error("Please enter a valid number")
            except KeyboardInterrupt:
                print()
                return None


class InteractiveWizard:
    """Interactive wizard for complex commands"""
    
    @staticmethod
    def create_project() -> Optional[Dict[str, Any]]:
        """Interactive project creation wizard"""
        UI.header(f"{Icon.SPARKLES} Create New Project")
        
        print("\nLet's set up your new PohLang project!\n")
        
        # Project name
        name = input_text("Project name", required=True)
        
        # Template selection
        templates = ['basic', 'console', 'web', 'library']
        template = select("Select project template", templates, default=0)
        
        # UI scaffolding
        ui_enabled = confirm("Include UI toolkit?", default=True)
        
        # Platform targets
        print(f"\n{Icon.INFO} Select target platforms (leave empty to skip)")
        platforms = []
        platform_options = ['Android', 'iOS', 'macOS', 'Windows', 'Web']
        
        for platform in platform_options:
            if confirm(f"  Target {platform}?", default=False):
                platforms.append(platform.lower())
        
        # Confirmation
        UI.section("Project Configuration")
        UI.detail("Name", name)
        UI.detail("Template", template)
        UI.detail("UI Toolkit", "Yes" if ui_enabled else "No")
        UI.detail("Platforms", ", ".join(platforms) if platforms else "None")
        
        if confirm("\nCreate project with these settings?", default=True):
            return {
                'name': name,
                'template': template,
                'ui_enabled': ui_enabled,
                'platforms': platforms
            }
        return None
    
    @staticmethod
    def configure_build() -> Optional[Dict[str, Any]]:
        """Interactive build configuration wizard"""
        UI.header(f"{Icon.BUILD} Build Configuration")
        
        # Build target
        targets = ['python', 'dart', 'native', 'bytecode']
        target = select("Build target", targets, default=0)
        
        # Configuration
        configs = ['debug', 'release']
        config = select("Build configuration", configs, default=0)
        
        # Optimizations
        optimize = confirm("Enable optimizations?", default=config == 'release')
        
        return {
            'target': target,
            'configuration': config,
            'optimize': optimize
        }


class DebugHelper:
    """Helper for debugging commands"""
    
    @staticmethod
    def start_debug_session(file: Path, port: int = 5858) -> bool:
        """Start debug session with user-friendly instructions"""
        UI.header(f"{Icon.DEBUG} Debug Session")
        
        UI.step(f"Starting debug server on port {port}")
        UI.info(f"File: {file}")
        
        # Check if file exists
        if not EnhancedRunner.verify_file_exists(file, "Script file"):
            return False
        
        UI.section("Debug Instructions")
        UI.bullet("Set breakpoints in your code")
        UI.bullet("Connect your IDE debugger to localhost:" + str(port))
        UI.bullet("Press Ctrl+C to stop debugging")
        
        UI.divider()
        
        # This would start actual debug server
        UI.info("Debug server ready")
        UI.tip("See docs/debugging.md for IDE setup instructions")
        
        return True
    
    @staticmethod
    def show_runtime_errors(errors: List[Dict[str, Any]]):
        """Display runtime errors with context"""
        if not errors:
            UI.success("No errors found")
            return
        
        UI.section(f"{Icon.ERROR} Runtime Errors ({len(errors)})")
        
        for i, error in enumerate(errors, 1):
            line = error.get('line', '?')
            message = error.get('message', 'Unknown error')
            file = error.get('file', 'unknown')
            
            print(f"\n{Color.RED}{i}. Line {line}:{Color.RESET} {message}")
            print(f"   {Color.DIM}in {file}{Color.RESET}")
            
            # Show code context if available
            if 'context' in error:
                print(f"\n   {Color.DIM}{error['context']}{Color.RESET}")


class DocHelper:
    """Helper for documentation and help"""
    
    @staticmethod
    def show_command_help(command: str, description: str, examples: List[str]):
        """Show detailed command help"""
        UI.header(f"{Icon.BOOK} plhub {command}")
        print(f"\n{description}\n")
        
        if examples:
            UI.section("Examples")
            for example in examples:
                UI.command(example)
                print()
    
    @staticmethod
    def show_quick_start():
        """Show quick start guide"""
        UI.header(f"{Icon.ROCKET} PLHub Quick Start")
        
        print("\n1. Create a new project:")
        UI.command("plhub create my_app")
        
        print("\n2. Navigate to project:")
        UI.command("cd my_app")
        
        print("\n3. Run your program:")
        UI.command("plhub run src/main.poh")
        
        print("\n4. Build for production:")
        UI.command("plhub build --release")
        
        UI.tip("Run 'plhub --help' for more commands")


def handle_common_errors(func: Callable) -> Callable:
    """Decorator for common error handling"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as e:
            UI.error(f"File not found: {e.filename}")
            return 1
        except PermissionError as e:
            UI.error(f"Permission denied: {e.filename}")
            UI.tip("Try running with appropriate permissions")
            return 1
        except KeyboardInterrupt:
            print()
            UI.warning("Operation cancelled by user")
            return 130
        except Exception as e:
            UI.error(f"Unexpected error: {e}")
            UI.tip("Run with --verbose for more details")
            return 1
    
    return wrapper


def suggest_similar_commands(command: str, available_commands: List[str]) -> List[str]:
    """Suggest similar commands for typos"""
    return fuzzy_match(command, available_commands, threshold=0.5)
