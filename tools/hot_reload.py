"""
Hot Reload System for PohLang Applications

Provides:
- File watching and change detection
- Automatic program restart on changes
- State preservation between reloads
- Error recovery
- Development mode server
"""

import os
import sys
import time
import json
import subprocess
import platform
import signal
from pathlib import Path
from typing import Optional, Dict, Any, Callable
from datetime import datetime
import threading


class HotReloadServer:
    """Hot reload development server for PohLang applications"""
    
    def __init__(self, project_root: Path, entry_file: Path, verbose: bool = False):
        self.project_root = project_root
        self.entry_file = entry_file
        self.verbose = verbose
        self.plhub_root = Path(__file__).parent.parent
        self.process: Optional[subprocess.Popen] = None
        self.running = False
        self.reload_count = 0
        self.state_file = project_root / '.plhub' / 'hotreload_state.json'
        
    def log(self, message: str):
        """Print message if verbose mode enabled"""
        if self.verbose:
            timestamp = datetime.now().strftime('%H:%M:%S')
            print(f"[{timestamp}] {message}")
        else:
            print(message)
    
    def find_pohlang_binary(self) -> Optional[Path]:
        """Locate the PohLang runtime binary"""
        exe = 'pohlang.exe' if platform.system().lower().startswith('win') else 'pohlang'
        candidates = [
            self.plhub_root / 'Runtime' / 'bin' / exe,
            self.plhub_root / 'bin' / exe,
        ]
        
        for p in os.environ.get('PATH', '').split(os.pathsep):
            candidates.append(Path(p) / exe)
        
        for candidate in candidates:
            if candidate.exists():
                return candidate
        
        return None
    
    def save_state(self, state: Dict[str, Any]):
        """Save application state before reload"""
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2)
    
    def load_state(self) -> Dict[str, Any]:
        """Load application state after reload"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return {}
    
    def start_process(self):
        """Start the PohLang application process"""
        pohlang_bin = self.find_pohlang_binary()
        if not pohlang_bin:
            print("❌ PohLang binary not found")
            return False
        
        try:
            self.log(f"🚀 Starting {self.entry_file.name}...")
            
            # Start the process
            self.process = subprocess.Popen(
                [str(pohlang_bin), '--run', str(self.entry_file)],
                cwd=self.project_root,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1  # Line buffered
            )
            
            # Monitor output in separate threads
            def monitor_stdout():
                if self.process and self.process.stdout:
                    for line in self.process.stdout:
                        print(line, end='')
            
            def monitor_stderr():
                if self.process and self.process.stderr:
                    for line in self.process.stderr:
                        print(line, end='', file=sys.stderr)
            
            stdout_thread = threading.Thread(target=monitor_stdout, daemon=True)
            stderr_thread = threading.Thread(target=monitor_stderr, daemon=True)
            stdout_thread.start()
            stderr_thread.start()
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to start process: {e}")
            return False
    
    def stop_process(self):
        """Stop the running PohLang application process"""
        if self.process:
            self.log("⏹️  Stopping process...")
            try:
                # Try graceful shutdown first
                self.process.terminate()
                try:
                    self.process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    # Force kill if not responding
                    self.process.kill()
                    self.process.wait()
            except Exception as e:
                self.log(f"Warning: Error stopping process: {e}")
            finally:
                self.process = None
    
    def reload(self):
        """Reload the application"""
        self.reload_count += 1
        self.log(f"🔄 Reloading... (#{self.reload_count})")
        
        # Stop current process
        self.stop_process()
        
        # Brief pause to ensure cleanup
        time.sleep(0.3)
        
        # Restart process
        if self.start_process():
            self.log(f"✅ Reload complete")
        else:
            self.log(f"❌ Reload failed")
    
    def watch_and_reload(self):
        """Watch for file changes and reload automatically"""
        print("=" * 60)
        print("🔥 PohLang Hot Reload Server")
        print("=" * 60)
        print(f"Project: {self.project_root.name}")
        print(f"Entry:   {self.entry_file.name}")
        print(f"Reloads: {self.reload_count}")
        print("=" * 60)
        print("\nPress Ctrl+C to stop\n")
        
        # Start initial process
        if not self.start_process():
            return
        
        self.running = True
        
        try:
            from watchdog.observers import Observer
            from watchdog.events import FileSystemEventHandler
            
            class PohFileHandler(FileSystemEventHandler):
                def __init__(self, server):
                    self.server = server
                    self.debounce_timer = None
                
                def on_modified(self, event):
                    if event.is_directory or not event.src_path.endswith('.poh'):
                        return
                    self.trigger_reload(event.src_path)
                
                def on_created(self, event):
                    if event.is_directory or not event.src_path.endswith('.poh'):
                        return
                    self.trigger_reload(event.src_path)
                
                def trigger_reload(self, file_path):
                    # Debounce: wait 0.5s before reloading
                    if self.debounce_timer:
                        self.debounce_timer.cancel()
                    
                    def do_reload():
                        rel_path = Path(file_path).relative_to(self.server.project_root)
                        print(f"\n📝 {rel_path} changed")
                        self.server.reload()
                    
                    self.debounce_timer = threading.Timer(0.5, do_reload)
                    self.debounce_timer.start()
            
            event_handler = PohFileHandler(self)
            observer = Observer()
            
            # Watch src directory
            src_dir = self.project_root / 'src'
            if src_dir.exists():
                observer.schedule(event_handler, str(src_dir), recursive=True)
            
            # Watch ui directory
            ui_dir = self.project_root / 'ui'
            if ui_dir.exists():
                observer.schedule(event_handler, str(ui_dir), recursive=True)
            
            # Watch entry file directory
            observer.schedule(event_handler, str(self.entry_file.parent), recursive=False)
            
            observer.start()
            
            try:
                while self.running:
                    time.sleep(1)
            except KeyboardInterrupt:
                pass
            finally:
                observer.stop()
                observer.join()
                self.stop_process()
                print("\n⏹️  Hot reload server stopped")
        
        except ImportError:
            print("❌ Hot reload requires 'watchdog' package")
            print("   Install with: pip install watchdog")
            self.stop_process()
    
    def run_once(self):
        """Run the application once (no watching)"""
        pohlang_bin = self.find_pohlang_binary()
        if not pohlang_bin:
            print("❌ PohLang binary not found")
            return 1
        
        try:
            result = subprocess.run(
                [str(pohlang_bin), '--run', str(self.entry_file)],
                cwd=self.project_root
            )
            return result.returncode
        except Exception as e:
            print(f"❌ Error: {e}")
            return 1


class DebugServer(HotReloadServer):
    """Extended hot reload server with debugging capabilities"""
    
    def __init__(self, project_root: Path, entry_file: Path, verbose: bool = False, debug_port: int = 5858):
        super().__init__(project_root, entry_file, verbose)
        self.debug_port = debug_port
        self.breakpoints: Dict[str, List[int]] = {}  # file -> line numbers
    
    def set_breakpoint(self, file_path: str, line: int):
        """Set a breakpoint at the specified file and line"""
        if file_path not in self.breakpoints:
            self.breakpoints[file_path] = []
        if line not in self.breakpoints[file_path]:
            self.breakpoints[file_path].append(line)
            self.log(f"🔴 Breakpoint set: {file_path}:{line}")
    
    def clear_breakpoint(self, file_path: str, line: int):
        """Clear a breakpoint"""
        if file_path in self.breakpoints and line in self.breakpoints[file_path]:
            self.breakpoints[file_path].remove(line)
            self.log(f"⚪ Breakpoint cleared: {file_path}:{line}")
    
    def list_breakpoints(self):
        """List all active breakpoints"""
        if not self.breakpoints:
            print("No breakpoints set")
            return
        
        print("\nActive breakpoints:")
        for file_path, lines in self.breakpoints.items():
            for line in sorted(lines):
                print(f"  🔴 {file_path}:{line}")
    
    def start_debug_session(self):
        """Start a debug session with breakpoint support"""
        print("=" * 60)
        print("🐛 PohLang Debug Server")
        print("=" * 60)
        print(f"Project: {self.project_root.name}")
        print(f"Entry:   {self.entry_file.name}")
        print(f"Port:    {self.debug_port}")
        print("=" * 60)
        print("\nDebug commands:")
        print("  break <file>:<line>  - Set breakpoint")
        print("  clear <file>:<line>  - Clear breakpoint")
        print("  list                 - List breakpoints")
        print("  run                  - Run/continue")
        print("  stop                 - Stop execution")
        print("  quit                 - Exit debugger")
        print("\nNote: Full debugger implementation requires PohLang runtime support")
        print("=" * 60)
