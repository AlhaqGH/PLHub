"""
PLHub User-Friendly UI Helpers
Provides beautiful, intuitive command-line interface utilities for all PLHub commands.
"""

import sys
import os
import time
import shutil
from typing import Optional, List, Callable, Any
from pathlib import Path
from enum import Enum


class Color:
    """ANSI color codes for terminal output"""
    # Basic colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Styles
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'
    
    @staticmethod
    def enabled() -> bool:
        """Check if colors are supported"""
        # Windows 10+ supports ANSI colors
        if sys.platform == 'win32':
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
                return True
            except:
                return False
        return True
    
    @staticmethod
    def disable():
        """Disable all colors (for CI/CD or when unsupported)"""
        for attr in dir(Color):
            if not attr.startswith('_') and attr.isupper():
                setattr(Color, attr, '')


# Disable colors if not supported
if not Color.enabled() and os.getenv('PLHUB_NO_COLOR') != '1':
    try:
        import colorama
        colorama.init()
    except:
        Color.disable()


class Icon:
    """Unicode icons for better visual feedback"""
    SUCCESS = "✅"
    ERROR = "❌"
    WARNING = "⚠️"
    INFO = "ℹ️"
    ARROW = "→"
    BULLET = "•"
    CHECK = "✓"
    CROSS = "✗"
    ROCKET = "🚀"
    PACKAGE = "📦"
    FOLDER = "📁"
    FILE = "📄"
    WRENCH = "🔧"
    SPARKLES = "✨"
    FIRE = "🔥"
    GEAR = "⚙️"
    CLOCK = "⏱️"
    DOWNLOAD = "⬇️"
    UPLOAD = "⬆️"
    BUILD = "🏗️"
    TEST = "🧪"
    DEBUG = "🐛"
    SEARCH = "🔍"
    BOOK = "📚"
    LIGHT = "💡"
    COMPUTER = "💻"
    PHONE = "📱"


class UI:
    """User-friendly UI helper methods"""
    
    @staticmethod
    def success(message: str, prefix: str = ""):
        """Print success message with green color"""
        prefix_str = f"{prefix} " if prefix else f"{Icon.SUCCESS} "
        print(f"{Color.GREEN}{prefix_str}{message}{Color.RESET}")
    
    @staticmethod
    def error(message: str, prefix: str = ""):
        """Print error message with red color"""
        prefix_str = f"{prefix} " if prefix else f"{Icon.ERROR} "
        print(f"{Color.RED}{prefix_str}{message}{Color.RESET}", file=sys.stderr)
    
    @staticmethod
    def warning(message: str, prefix: str = ""):
        """Print warning message with yellow color"""
        prefix_str = f"{prefix} " if prefix else f"{Icon.WARNING} "
        print(f"{Color.YELLOW}{prefix_str}{message}{Color.RESET}")
    
    @staticmethod
    def info(message: str, prefix: str = ""):
        """Print info message with blue color"""
        prefix_str = f"{prefix} " if prefix else f"{Icon.INFO} "
        print(f"{Color.CYAN}{prefix_str}{message}{Color.RESET}")
    
    @staticmethod
    def step(message: str, number: Optional[int] = None):
        """Print step message"""
        if number:
            print(f"{Color.BOLD}{Color.BLUE}[{number}]{Color.RESET} {message}")
        else:
            print(f"{Color.BOLD}{Color.BLUE}{Icon.ARROW}{Color.RESET} {message}")
    
    @staticmethod
    def header(message: str):
        """Print header message"""
        print(f"\n{Color.BOLD}{Color.CYAN}{message}{Color.RESET}")
        print(f"{Color.DIM}{'=' * min(len(message), 60)}{Color.RESET}")
    
    @staticmethod
    def section(message: str):
        """Print section message"""
        print(f"\n{Color.BOLD}{message}{Color.RESET}")
    
    @staticmethod
    def bullet(message: str, indent: int = 0):
        """Print bullet point"""
        print(f"{'  ' * indent}{Icon.BULLET} {message}")
    
    @staticmethod
    def detail(key: str, value: str, indent: int = 0):
        """Print key-value detail"""
        print(f"{'  ' * indent}{Color.DIM}{key}:{Color.RESET} {Color.BOLD}{value}{Color.RESET}")
    
    @staticmethod
    def command(cmd: str):
        """Print command to run"""
        print(f"{Color.DIM}$ {Color.RESET}{Color.BRIGHT_WHITE}{cmd}{Color.RESET}")
    
    @staticmethod
    def tip(message: str):
        """Print helpful tip"""
        print(f"{Color.YELLOW}{Icon.LIGHT} Tip:{Color.RESET} {message}")
    
    @staticmethod
    def divider(char: str = "-", width: Optional[int] = None):
        """Print divider line"""
        if width is None:
            width = shutil.get_terminal_size((80, 20)).columns
        print(f"{Color.DIM}{char * width}{Color.RESET}")


class ProgressBar:
    """Progress bar for long-running operations"""
    
    def __init__(self, total: int, description: str = "", width: int = 40):
        self.total = total
        self.current = 0
        self.description = description
        self.width = width
        self.start_time = time.time()
        self._last_update = 0
    
    def update(self, amount: int = 1, description: Optional[str] = None):
        """Update progress bar"""
        self.current = min(self.current + amount, self.total)
        if description:
            self.description = description
        
        # Throttle updates to avoid flickering
        now = time.time()
        if now - self._last_update < 0.1 and self.current < self.total:
            return
        self._last_update = now
        
        self._render()
    
    def _render(self):
        """Render progress bar"""
        percent = (self.current / self.total) * 100 if self.total > 0 else 0
        filled = int(self.width * self.current / self.total) if self.total > 0 else 0
        bar = "█" * filled + "░" * (self.width - filled)
        
        elapsed = time.time() - self.start_time
        rate = self.current / elapsed if elapsed > 0 else 0
        eta = (self.total - self.current) / rate if rate > 0 else 0
        
        eta_str = self._format_time(eta)
        
        # Build status line
        status = f"{self.description} {Color.BRIGHT_CYAN}{bar}{Color.RESET} "
        status += f"{Color.BOLD}{percent:.1f}%{Color.RESET} "
        status += f"({self.current}/{self.total}) "
        if eta > 0 and self.current < self.total:
            status += f"{Color.DIM}ETA: {eta_str}{Color.RESET}"
        
        # Clear line and print
        print(f"\r{status}", end="", flush=True)
        
        if self.current >= self.total:
            print()  # New line when complete
    
    def _format_time(self, seconds: float) -> str:
        """Format seconds to human-readable time"""
        if seconds < 60:
            return f"{int(seconds)}s"
        elif seconds < 3600:
            return f"{int(seconds / 60)}m {int(seconds % 60)}s"
        else:
            h = int(seconds / 3600)
            m = int((seconds % 3600) / 60)
            return f"{h}h {m}m"
    
    def finish(self, message: Optional[str] = None):
        """Complete the progress bar"""
        self.current = self.total
        self._render()
        if message:
            UI.success(message)


class Spinner:
    """Animated spinner for indeterminate operations"""
    
    FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    
    def __init__(self, description: str = "Working..."):
        self.description = description
        self.frame = 0
        self.running = False
        self._thread = None
    
    def __enter__(self):
        """Start spinner"""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop spinner"""
        self.stop()
    
    def start(self):
        """Start spinner animation"""
        import threading
        self.running = True
        self._thread = threading.Thread(target=self._spin)
        self._thread.daemon = True
        self._thread.start()
    
    def stop(self, final_message: Optional[str] = None):
        """Stop spinner animation"""
        self.running = False
        if self._thread:
            self._thread.join()
        print(f"\r{' ' * (len(self.description) + 10)}\r", end="", flush=True)
        if final_message:
            print(final_message)
    
    def _spin(self):
        """Spinner animation loop"""
        while self.running:
            frame = self.FRAMES[self.frame % len(self.FRAMES)]
            print(f"\r{Color.CYAN}{frame}{Color.RESET} {self.description}", end="", flush=True)
            self.frame += 1
            time.sleep(0.1)


class Table:
    """Pretty table formatter"""
    
    def __init__(self, headers: List[str]):
        self.headers = headers
        self.rows: List[List[str]] = []
    
    def add_row(self, row: List[str]):
        """Add a row to the table"""
        self.rows.append(row)
    
    def render(self):
        """Render the table"""
        if not self.rows:
            return
        
        # Calculate column widths
        widths = [len(h) for h in self.headers]
        for row in self.rows:
            for i, cell in enumerate(row):
                widths[i] = max(widths[i], len(str(cell)))
        
        # Render header
        header_line = " │ ".join(
            f"{Color.BOLD}{h:<{widths[i]}}{Color.RESET}"
            for i, h in enumerate(self.headers)
        )
        print(f"│ {header_line} │")
        
        # Render separator
        sep = "─┼─".join("─" * w for w in widths)
        print(f"├─{sep}─┤")
        
        # Render rows
        for row in self.rows:
            row_line = " │ ".join(
                f"{str(cell):<{widths[i]}}"
                for i, cell in enumerate(row)
            )
            print(f"│ {row_line} │")


def confirm(message: str, default: bool = False) -> bool:
    """Ask for user confirmation"""
    suffix = " [Y/n]" if default else " [y/N]"
    response = input(f"{Icon.INFO} {message}{suffix}: ").strip().lower()
    
    if not response:
        return default
    return response in ('y', 'yes')


def select(prompt: str, options: List[str], default: Optional[int] = None) -> str:
    """Let user select from options"""
    print(f"\n{Icon.INFO} {prompt}")
    for i, option in enumerate(options, 1):
        default_marker = " (default)" if default == i - 1 else ""
        print(f"  {Color.CYAN}[{i}]{Color.RESET} {option}{Color.DIM}{default_marker}{Color.RESET}")
    
    while True:
        try:
            response = input(f"\nSelect [1-{len(options)}]: ").strip()
            if not response and default is not None:
                return options[default]
            
            choice = int(response)
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                UI.error(f"Please enter a number between 1 and {len(options)}")
        except ValueError:
            UI.error("Please enter a valid number")
        except KeyboardInterrupt:
            print()
            sys.exit(130)


def input_text(prompt: str, default: Optional[str] = None, required: bool = True) -> str:
    """Get text input from user"""
    default_text = f" [{default}]" if default else ""
    required_text = " (required)" if required and not default else ""
    
    while True:
        try:
            response = input(f"{Icon.INFO} {prompt}{default_text}{required_text}: ").strip()
            
            if not response and default:
                return default
            elif not response and required:
                UI.error("This field is required")
                continue
            else:
                return response
        except KeyboardInterrupt:
            print()
            sys.exit(130)


class ErrorHelper:
    """Helper for displaying errors with recovery suggestions"""
    
    @staticmethod
    def command_not_found(command: str, similar: Optional[List[str]] = None):
        """Display command not found error with suggestions"""
        UI.error(f"Command '{command}' not found")
        
        if similar:
            print(f"\n{Icon.LIGHT} Did you mean:")
            for cmd in similar[:3]:
                print(f"  {Color.CYAN}plhub {cmd}{Color.RESET}")
        
        print(f"\n{Icon.INFO} Run {Color.CYAN}plhub --help{Color.RESET} to see all commands")
    
    @staticmethod
    def file_not_found(filepath: str, suggestions: Optional[List[str]] = None):
        """Display file not found error with suggestions"""
        UI.error(f"File not found: {filepath}")
        
        if suggestions:
            print(f"\n{Icon.LIGHT} Did you mean:")
            for path in suggestions[:3]:
                print(f"  {Color.CYAN}{path}{Color.RESET}")
    
    @staticmethod
    def dependency_missing(dependency: str, install_cmd: Optional[str] = None):
        """Display missing dependency error with installation help"""
        UI.error(f"Missing dependency: {dependency}")
        
        if install_cmd:
            print(f"\n{Icon.LIGHT} Install it with:")
            UI.command(install_cmd)
    
    @staticmethod
    def build_failed(error: str, suggestions: Optional[List[str]] = None):
        """Display build failure with recovery suggestions"""
        UI.error(f"Build failed: {error}")
        
        if suggestions:
            print(f"\n{Icon.LIGHT} Try these solutions:")
            for i, suggestion in enumerate(suggestions, 1):
                print(f"  {i}. {suggestion}")
    
    @staticmethod
    def network_error(operation: str, url: Optional[str] = None):
        """Display network error with troubleshooting tips"""
        UI.error(f"Network error during {operation}")
        
        if url:
            print(f"  URL: {Color.DIM}{url}{Color.RESET}")
        
        print(f"\n{Icon.LIGHT} Troubleshooting:")
        UI.bullet("Check your internet connection")
        UI.bullet("Verify firewall/proxy settings")
        UI.bullet("Try again in a few moments")


class DownloadProgress:
    """Progress tracker for downloads"""
    
    def __init__(self, description: str, total_size: Optional[int] = None):
        self.description = description
        self.total_size = total_size
        self.downloaded = 0
        self.start_time = time.time()
        self._last_update = 0
    
    def update(self, chunk_size: int):
        """Update download progress"""
        self.downloaded += chunk_size
        
        # Throttle updates
        now = time.time()
        if now - self._last_update < 0.1 and self.total_size and self.downloaded < self.total_size:
            return
        self._last_update = now
        
        self._render()
    
    def _render(self):
        """Render download progress"""
        downloaded_mb = self.downloaded / 1024 / 1024
        elapsed = time.time() - self.start_time
        speed = self.downloaded / elapsed if elapsed > 0 else 0
        speed_mb = speed / 1024 / 1024
        
        if self.total_size:
            total_mb = self.total_size / 1024 / 1024
            percent = (self.downloaded / self.total_size) * 100
            eta = (self.total_size - self.downloaded) / speed if speed > 0 else 0
            eta_str = self._format_time(eta)
            
            status = f"\r{Icon.DOWNLOAD} {self.description}: "
            status += f"{Color.BOLD}{percent:.1f}%{Color.RESET} "
            status += f"({downloaded_mb:.1f}/{total_mb:.1f} MB) "
            status += f"at {speed_mb:.1f} MB/s "
            if eta > 0:
                status += f"{Color.DIM}ETA: {eta_str}{Color.RESET}"
        else:
            status = f"\r{Icon.DOWNLOAD} {self.description}: "
            status += f"{downloaded_mb:.1f} MB at {speed_mb:.1f} MB/s"
        
        print(status, end="", flush=True)
    
    def _format_time(self, seconds: float) -> str:
        """Format seconds to human-readable time"""
        if seconds < 60:
            return f"{int(seconds)}s"
        elif seconds < 3600:
            return f"{int(seconds / 60)}m"
        else:
            return f"{int(seconds / 3600)}h"
    
    def finish(self):
        """Complete the download"""
        self._render()
        print()  # New line


def fuzzy_match(needle: str, haystack: List[str], threshold: float = 0.6) -> List[str]:
    """Find similar strings using fuzzy matching"""
    import difflib
    matches = []
    
    for item in haystack:
        ratio = difflib.SequenceMatcher(None, needle.lower(), item.lower()).ratio()
        if ratio >= threshold:
            matches.append((ratio, item))
    
    matches.sort(reverse=True, key=lambda x: x[0])
    return [item for _, item in matches]


def format_size(bytes: int) -> str:
    """Format bytes to human-readable size"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024.0:
            return f"{bytes:.1f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.1f} PB"


def format_duration(seconds: float) -> str:
    """Format seconds to human-readable duration"""
    if seconds < 1:
        return f"{int(seconds * 1000)}ms"
    elif seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        secs = int(seconds % 60)
        return f"{minutes}m {secs}s"
    else:
        hours = int(seconds / 3600)
        minutes = int((seconds % 3600) / 60)
        return f"{hours}h {minutes}m"
