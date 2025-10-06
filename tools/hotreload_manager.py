"""
PLHub Hot Reload System
Provides real-time code reloading for all platforms during development.
Watches for file changes and automatically updates running applications.
"""

import os
import time
import json
import asyncio
import websockets
import threading
from pathlib import Path
from typing import Dict, List, Set, Optional, Callable
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent
from enum import Enum


class ReloadStrategy(Enum):
    """Hot reload strategies for different platforms"""
    FULL_RESTART = "full_restart"  # Restart entire app
    MODULE_REPLACE = "module_replace"  # Replace specific modules
    STATE_PRESERVE = "state_preserve"  # Reload while preserving state
    INCREMENTAL = "incremental"  # Incremental updates


class HotReloadServer:
    """WebSocket server for hot reload communication"""
    
    def __init__(self, port: int = 8765):
        self.port = port
        self.clients: Set[websockets.WebSocketServerProtocol] = set()
        self.server = None
        self.running = False
    
    async def register(self, websocket):
        """Register new client"""
        self.clients.add(websocket)
        print(f"Hot reload client connected. Total clients: {len(self.clients)}")
        try:
            await websocket.wait_closed()
        finally:
            self.clients.remove(websocket)
            print(f"Client disconnected. Total clients: {len(self.clients)}")
    
    async def broadcast(self, message: Dict):
        """Broadcast message to all connected clients"""
        if not self.clients:
            return
        
        message_json = json.dumps(message)
        disconnected = set()
        
        for client in self.clients:
            try:
                await client.send(message_json)
            except Exception as e:
                print(f"Error sending to client: {e}")
                disconnected.add(client)
        
        # Remove disconnected clients
        self.clients -= disconnected
    
    async def start(self):
        """Start WebSocket server"""
        self.running = True
        self.server = await websockets.serve(self.register, "localhost", self.port)
        print(f"✓ Hot reload server started on ws://localhost:{self.port}")
        await asyncio.Future()  # Run forever
    
    def stop(self):
        """Stop WebSocket server"""
        self.running = False
        if self.server:
            self.server.close()


class FileWatcher(FileSystemEventHandler):
    """Watches for file changes"""
    
    def __init__(self, watch_patterns: List[str], callback: Callable):
        super().__init__()
        self.watch_patterns = watch_patterns
        self.callback = callback
        self.debounce_timer = None
        self.debounce_delay = 0.5  # seconds
        self.pending_changes: Set[str] = set()
    
    def on_any_event(self, event: FileSystemEvent):
        """Handle file system events"""
        if event.is_directory:
            return
        
        # Check if file matches watch patterns
        file_path = Path(event.src_path)
        if not self._should_watch(file_path):
            return
        
        # Ignore certain files
        if self._should_ignore(file_path):
            return
        
        # Add to pending changes
        self.pending_changes.add(str(file_path))
        
        # Debounce: Only trigger after delay with no new changes
        if self.debounce_timer:
            self.debounce_timer.cancel()
        
        self.debounce_timer = threading.Timer(
            self.debounce_delay,
            self._trigger_reload
        )
        self.debounce_timer.start()
    
    def _should_watch(self, file_path: Path) -> bool:
        """Check if file should be watched"""
        suffix = file_path.suffix.lower()
        
        for pattern in self.watch_patterns:
            if pattern.startswith('*.'):
                if suffix == pattern[1:]:
                    return True
            elif pattern in str(file_path):
                return True
        
        return False
    
    def _should_ignore(self, file_path: Path) -> bool:
        """Check if file should be ignored"""
        ignore_patterns = [
            '__pycache__',
            '.git',
            'node_modules',
            'build',
            'dist',
            '.DS_Store',
            'Thumbs.db',
            '.pyc',
            '.pyo',
            '.class',
            '.o',
            '.so',
            '.dylib',
            '.dll',
            '.exe'
        ]
        
        path_str = str(file_path)
        for pattern in ignore_patterns:
            if pattern in path_str:
                return True
        
        return False
    
    def _trigger_reload(self):
        """Trigger reload callback"""
        if self.pending_changes:
            changes = list(self.pending_changes)
            self.pending_changes.clear()
            self.callback(changes)


class HotReloadManager:
    """Manages hot reload for all platforms"""
    
    def __init__(self, project_dir: Path, platform: str):
        self.project_dir = project_dir
        self.platform = platform
        self.server = HotReloadServer()
        self.observer = Observer()
        self.file_watcher = None
        self.running = False
        self.strategy = self._get_reload_strategy(platform)
        self.watch_patterns = self._get_watch_patterns(platform)
    
    def _get_reload_strategy(self, platform: str) -> ReloadStrategy:
        """Get reload strategy for platform"""
        strategies = {
            'web': ReloadStrategy.MODULE_REPLACE,
            'android': ReloadStrategy.INCREMENTAL,
            'ios': ReloadStrategy.STATE_PRESERVE,
            'macos': ReloadStrategy.STATE_PRESERVE,
            'windows': ReloadStrategy.MODULE_REPLACE
        }
        return strategies.get(platform, ReloadStrategy.FULL_RESTART)
    
    def _get_watch_patterns(self, platform: str) -> List[str]:
        """Get file patterns to watch for platform"""
        patterns = {
            'web': ['*.poh', '*.js', '*.ts', '*.html', '*.css', '*.json'],
            'android': ['*.poh', '*.java', '*.kt', '*.xml', '*.gradle'],
            'ios': ['*.poh', '*.swift', '*.m', '*.h', '*.storyboard', '*.xib'],
            'macos': ['*.poh', '*.swift', '*.m', '*.h', '*.storyboard', '*.xib'],
            'windows': ['*.poh', '*.cs', '*.xaml', '*.csproj']
        }
        return patterns.get(platform, ['*.poh'])
    
    def start(self):
        """Start hot reload system"""
        print(f"Starting hot reload for {self.platform}...")
        print(f"Strategy: {self.strategy.value}")
        print(f"Watching: {', '.join(self.watch_patterns)}")
        
        # Start file watcher
        self.file_watcher = FileWatcher(
            self.watch_patterns,
            self._on_files_changed
        )
        
        self.observer.schedule(
            self.file_watcher,
            str(self.project_dir),
            recursive=True
        )
        self.observer.start()
        
        # Start WebSocket server in background
        server_thread = threading.Thread(
            target=self._run_server,
            daemon=True
        )
        server_thread.start()
        
        self.running = True
        print("✓ Hot reload active. Watching for changes...")
    
    def _run_server(self):
        """Run WebSocket server in background"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.server.start())
    
    def _on_files_changed(self, changed_files: List[str]):
        """Handle file changes"""
        print(f"\n🔄 Files changed: {len(changed_files)}")
        for file in changed_files:
            print(f"   - {Path(file).relative_to(self.project_dir)}")
        
        # Prepare reload message
        message = {
            'type': 'reload',
            'strategy': self.strategy.value,
            'files': [str(Path(f).relative_to(self.project_dir)) for f in changed_files],
            'timestamp': time.time()
        }
        
        # Platform-specific handling
        if self.platform == 'web':
            self._reload_web(message)
        elif self.platform == 'android':
            self._reload_android(message)
        elif self.platform in ['ios', 'macos']:
            self._reload_apple(message)
        elif self.platform == 'windows':
            self._reload_windows(message)
        
        print("✓ Hot reload complete")
    
    def _reload_web(self, message: Dict):
        """Hot reload for web platform"""
        # Send to browser via WebSocket
        asyncio.run(self.server.broadcast(message))
        print("→ Sent reload signal to browser")
    
    def _reload_android(self, message: Dict):
        """Hot reload for Android platform"""
        # Use ADB to trigger reload
        try:
            import subprocess
            # Send broadcast to app
            result = subprocess.run(
                ['adb', 'shell', 'am', 'broadcast',
                 '-a', 'com.pohlang.HOTRELOAD',
                 '--es', 'files', ','.join(message['files'])],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print("→ Sent reload signal to Android device")
            else:
                print("⚠️  Could not send reload signal to Android")
        except Exception as e:
            print(f"⚠️  Android reload error: {e}")
    
    def _reload_apple(self, message: Dict):
        """Hot reload for iOS/macOS platform"""
        # Use Network.framework connection
        asyncio.run(self.server.broadcast(message))
        print(f"→ Sent reload signal to {self.platform}")
    
    def _reload_windows(self, message: Dict):
        """Hot reload for Windows platform"""
        # Use named pipes or WebSocket
        asyncio.run(self.server.broadcast(message))
        print("→ Sent reload signal to Windows app")
    
    def stop(self):
        """Stop hot reload system"""
        print("\nStopping hot reload...")
        self.running = False
        self.observer.stop()
        self.observer.join()
        self.server.stop()
        print("✓ Hot reload stopped")
    
    def wait(self):
        """Wait for hot reload to finish"""
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()


class HotReloadClient:
    """Client-side hot reload handler (embedded in apps)"""
    
    def __init__(self, server_url: str = "ws://localhost:8765"):
        self.server_url = server_url
        self.websocket = None
        self.connected = False
        self.on_reload_callback = None
    
    async def connect(self):
        """Connect to hot reload server"""
        try:
            self.websocket = await websockets.connect(self.server_url)
            self.connected = True
            print(f"Connected to hot reload server: {self.server_url}")
            
            # Listen for messages
            async for message in self.websocket:
                await self._handle_message(message)
                
        except Exception as e:
            print(f"Hot reload connection failed: {e}")
            self.connected = False
    
    async def _handle_message(self, message: str):
        """Handle reload message from server"""
        try:
            data = json.loads(message)
            
            if data['type'] == 'reload':
                print(f"Hot reload triggered: {data['strategy']}")
                
                if self.on_reload_callback:
                    await self.on_reload_callback(data)
                else:
                    # Default: full page reload
                    self._default_reload(data)
                    
        except Exception as e:
            print(f"Error handling reload message: {e}")
    
    def _default_reload(self, data: Dict):
        """Default reload behavior"""
        strategy = data['strategy']
        
        if strategy == ReloadStrategy.MODULE_REPLACE.value:
            print("Replacing modules...")
            # Module replacement logic
        elif strategy == ReloadStrategy.STATE_PRESERVE.value:
            print("Reloading while preserving state...")
            # State-preserving reload logic
        elif strategy == ReloadStrategy.INCREMENTAL.value:
            print("Applying incremental updates...")
            # Incremental update logic
        else:
            print("Performing full restart...")
            # Full restart logic
    
    def set_reload_callback(self, callback: Callable):
        """Set custom reload callback"""
        self.on_reload_callback = callback
    
    def disconnect(self):
        """Disconnect from hot reload server"""
        if self.websocket:
            asyncio.run(self.websocket.close())
            self.connected = False


# Example usage for different platforms

def create_web_hot_reload(project_dir: Path) -> HotReloadManager:
    """Create hot reload manager for web project"""
    return HotReloadManager(project_dir, 'web')


def create_android_hot_reload(project_dir: Path) -> HotReloadManager:
    """Create hot reload manager for Android project"""
    return HotReloadManager(project_dir, 'android')


def create_ios_hot_reload(project_dir: Path) -> HotReloadManager:
    """Create hot reload manager for iOS project"""
    return HotReloadManager(project_dir, 'ios')


def create_macos_hot_reload(project_dir: Path) -> HotReloadManager:
    """Create hot reload manager for macOS project"""
    return HotReloadManager(project_dir, 'macos')


def create_windows_hot_reload(project_dir: Path) -> HotReloadManager:
    """Create hot reload manager for Windows project"""
    return HotReloadManager(project_dir, 'windows')
