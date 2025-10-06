"""
Build Automation System for PohLang Projects

Provides:
- Watch mode with file monitoring
- Incremental builds with caching
- Dependency detection
- Build artifacts management
- Performance tracking
"""

import os
import sys
import time
import json
import hashlib
import subprocess
import platform
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import threading


@dataclass
class BuildCache:
    """Track file hashes and build timestamps"""
    file_hashes: Dict[str, str]  # file_path -> hash
    last_build: str  # ISO timestamp
    dependencies: Dict[str, List[str]]  # file -> [imported files]
    build_count: int
    
    @classmethod
    def load(cls, cache_file: Path) -> 'BuildCache':
        """Load cache from JSON file"""
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return cls(**data)
            except Exception:
                pass
        return cls(file_hashes={}, last_build='', dependencies={}, build_count=0)
    
    def save(self, cache_file: Path):
        """Save cache to JSON file"""
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(self), f, indent=2)


class BuildAutomation:
    """Automated build system with caching and incremental builds"""
    
    def __init__(self, project_root: Path, verbose: bool = False):
        self.project_root = project_root
        self.verbose = verbose
        self.cache_dir = project_root / '.plhub' / 'cache'
        self.cache_file = self.cache_dir / 'build_cache.json'
        self.cache = BuildCache.load(self.cache_file)
        self.plhub_root = Path(__file__).parent.parent
        
    def log(self, message: str):
        """Print message if verbose mode enabled"""
        if self.verbose:
            timestamp = datetime.now().strftime('%H:%M:%S')
            print(f"[{timestamp}] {message}")
    
    def find_pohlang_binary(self) -> Optional[Path]:
        """Locate the PohLang runtime binary"""
        exe = 'pohlang.exe' if platform.system().lower().startswith('win') else 'pohlang'
        candidates = [
            self.plhub_root / 'Runtime' / 'bin' / exe,
            self.plhub_root / 'bin' / exe,
        ]
        
        # Check PATH
        for p in os.environ.get('PATH', '').split(os.pathsep):
            candidates.append(Path(p) / exe)
        
        for candidate in candidates:
            if candidate.exists():
                return candidate
        
        return None
    
    def compute_file_hash(self, file_path: Path) -> str:
        """Compute SHA256 hash of file contents"""
        if not file_path.exists():
            return ''
        with open(file_path, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
    
    def find_source_files(self, directory: Path = None) -> List[Path]:
        """Find all .poh source files in project"""
        if directory is None:
            directory = self.project_root
        return list(directory.rglob('*.poh'))
    
    def extract_imports(self, file_path: Path) -> List[str]:
        """Extract Import statements from a .poh file"""
        imports = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    # Simple import detection: Import "path/to/file.poh"
                    if line.startswith('Import') or line.startswith('import'):
                        # Extract the quoted path
                        parts = line.split('"')
                        if len(parts) >= 2:
                            imports.append(parts[1])
        except Exception as e:
            self.log(f"Warning: Failed to parse imports from {file_path}: {e}")
        return imports
    
    def resolve_import_path(self, import_path: str, source_file: Path) -> Optional[Path]:
        """Resolve an import path to an absolute file path"""
        # Try relative to source file
        relative = source_file.parent / import_path
        if relative.exists():
            return relative.resolve()
        
        # Try relative to project root
        from_root = self.project_root / import_path
        if from_root.exists():
            return from_root.resolve()
        
        return None
    
    def build_dependency_graph(self) -> Dict[str, List[str]]:
        """Build a dependency graph of all source files"""
        dependencies = {}
        source_files = self.find_source_files()
        
        for file_path in source_files:
            imports = self.extract_imports(file_path)
            deps = []
            for imp in imports:
                resolved = self.resolve_import_path(imp, file_path)
                if resolved:
                    deps.append(str(resolved))
            dependencies[str(file_path)] = deps
        
        return dependencies
    
    def has_file_changed(self, file_path: Path) -> bool:
        """Check if file has changed since last build"""
        file_str = str(file_path)
        current_hash = self.compute_file_hash(file_path)
        old_hash = self.cache.file_hashes.get(file_str, '')
        return current_hash != old_hash
    
    def get_files_to_rebuild(self, changed_files: Set[Path]) -> Set[Path]:
        """Determine which files need rebuilding based on changes"""
        # Update dependency graph
        dependencies = self.build_dependency_graph()
        self.cache.dependencies = dependencies
        
        to_rebuild = set(changed_files)
        
        # Add dependent files
        for changed in changed_files:
            changed_str = str(changed)
            for file_path, deps in dependencies.items():
                if changed_str in deps:
                    to_rebuild.add(Path(file_path))
        
        return to_rebuild
    
    def compile_file(self, file_path: Path) -> Tuple[bool, str]:
        """Compile a single .poh file to bytecode"""
        pohlang_bin = self.find_pohlang_binary()
        if not pohlang_bin:
            return False, "PohLang binary not found"
        
        output_file = file_path.with_suffix('.pbc')
        
        try:
            cmd = [str(pohlang_bin), '--compile', str(file_path), '-o', str(output_file)]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                return True, f"Compiled {file_path.name} -> {output_file.name}"
            else:
                error_msg = result.stderr or result.stdout or "Unknown error"
                return False, f"Compilation failed: {error_msg}"
        except Exception as e:
            return False, f"Exception during compilation: {e}"
    
    def build_all(self, force: bool = False) -> Tuple[int, int, List[str]]:
        """Build all source files, returns (success_count, failure_count, messages)"""
        source_files = self.find_source_files()
        
        if force:
            files_to_build = set(source_files)
            self.log("Force build: compiling all files")
        else:
            # Incremental build
            changed = {f for f in source_files if self.has_file_changed(f)}
            files_to_build = self.get_files_to_rebuild(changed)
            self.log(f"Incremental build: {len(changed)} changed, {len(files_to_build)} to rebuild")
        
        if not files_to_build:
            return 0, 0, ["No files to build"]
        
        success_count = 0
        failure_count = 0
        messages = []
        
        for file_path in sorted(files_to_build):
            self.log(f"Building {file_path.relative_to(self.project_root)}...")
            success, msg = self.compile_file(file_path)
            
            if success:
                success_count += 1
                # Update cache
                self.cache.file_hashes[str(file_path)] = self.compute_file_hash(file_path)
            else:
                failure_count += 1
            
            messages.append(msg)
        
        # Update cache metadata
        self.cache.last_build = datetime.now().isoformat()
        self.cache.build_count += 1
        self.cache.save(self.cache_file)
        
        return success_count, failure_count, messages
    
    def watch_mode(self, callback=None):
        """Watch for file changes and rebuild automatically"""
        print(f"👀 Watching for changes in {self.project_root}")
        print("Press Ctrl+C to stop\n")
        
        # Try to use watchdog if available
        try:
            from watchdog.observers import Observer
            from watchdog.events import FileSystemEventHandler
            
            class PohFileHandler(FileSystemEventHandler):
                def __init__(self, builder, callback):
                    self.builder = builder
                    self.callback = callback
                    self.pending_changes = set()
                    self.debounce_timer = None
                
                def on_modified(self, event):
                    if event.is_directory or not event.src_path.endswith('.poh'):
                        return
                    self.trigger_rebuild(event.src_path)
                
                def on_created(self, event):
                    if event.is_directory or not event.src_path.endswith('.poh'):
                        return
                    self.trigger_rebuild(event.src_path)
                
                def trigger_rebuild(self, file_path):
                    self.pending_changes.add(Path(file_path))
                    
                    # Debounce: wait 0.5s before building
                    if self.debounce_timer:
                        self.debounce_timer.cancel()
                    
                    def do_rebuild():
                        if self.pending_changes:
                            print(f"\n📝 Changes detected: {len(self.pending_changes)} file(s)")
                            success, failure, messages = self.builder.build_all(force=False)
                            
                            if failure == 0:
                                print(f"✅ Build successful: {success} file(s) compiled")
                            else:
                                print(f"❌ Build completed with errors: {success} ok, {failure} failed")
                            
                            for msg in messages:
                                print(f"   {msg}")
                            
                            if self.callback:
                                self.callback(success, failure)
                            
                            self.pending_changes.clear()
                            print("\n👀 Watching for changes...")
                    
                    self.debounce_timer = threading.Timer(0.5, do_rebuild)
                    self.debounce_timer.start()
            
            event_handler = PohFileHandler(self, callback)
            observer = Observer()
            observer.schedule(event_handler, str(self.project_root), recursive=True)
            observer.start()
            
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                observer.stop()
                print("\n⏹️  Watch mode stopped")
            observer.join()
            
        except ImportError:
            # Fallback to polling
            print("Note: Install 'watchdog' package for better file watching")
            print("Falling back to polling mode\n")
            self._watch_mode_polling(callback)
    
    def _watch_mode_polling(self, callback=None, interval: float = 2.0):
        """Polling-based watch mode (fallback)"""
        file_mtimes = {}
        
        try:
            while True:
                changed = set()
                source_files = self.find_source_files()
                
                for file_path in source_files:
                    try:
                        mtime = file_path.stat().st_mtime
                        if str(file_path) not in file_mtimes:
                            file_mtimes[str(file_path)] = mtime
                        elif file_mtimes[str(file_path)] != mtime:
                            changed.add(file_path)
                            file_mtimes[str(file_path)] = mtime
                    except Exception:
                        pass
                
                if changed:
                    print(f"\n📝 Changes detected: {len(changed)} file(s)")
                    success, failure, messages = self.build_all(force=False)
                    
                    if failure == 0:
                        print(f"✅ Build successful: {success} file(s) compiled")
                    else:
                        print(f"❌ Build completed with errors: {success} ok, {failure} failed")
                    
                    for msg in messages:
                        print(f"   {msg}")
                    
                    if callback:
                        callback(success, failure)
                    
                    print("\n👀 Watching for changes...")
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n⏹️  Watch mode stopped")
