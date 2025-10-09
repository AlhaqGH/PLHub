"""
Automated Test Runner for PohLang Projects

Provides:
- Test discovery and execution
- Watch mode for continuous testing
- Coverage tracking
- Test result reporting
- CI/CD integration support
"""

import os
import sys
import time
import json
import subprocess
import platform
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import re


@dataclass
class PohTestResult:
    """Individual test result"""
    name: str
    file: str
    passed: bool
    duration: float  # seconds
    output: str
    error: Optional[str] = None


@dataclass
class PohTestSuite:
    """Complete test suite results"""
    total: int
    passed: int
    failed: int
    skipped: int
    duration: float
    results: List[PohTestResult]
    timestamp: str
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate percentage"""
        if self.total == 0:
            return 100.0
        return (self.passed / self.total) * 100


class PohTestRunner:
    """Automated test runner with watch mode and reporting"""
    
    def __init__(self, project_root: Path, verbose: bool = False):
        self.project_root = project_root
        self.verbose = verbose
        self.test_dir = project_root / 'tests'
        self.plhub_root = Path(__file__).parent.parent
        self.results_dir = project_root / '.plhub' / 'test-results'
        
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
        
        for p in os.environ.get('PATH', '').split(os.pathsep):
            candidates.append(Path(p) / exe)
        
        for candidate in candidates:
            if candidate.exists():
                return candidate
        
        return None
    
    def discover_tests(self, filter_pattern: Optional[str] = None) -> List[Path]:
        """Discover all test files in the tests directory"""
        if not self.test_dir.exists():
            return []
        
        test_files = []
        
        # Look for files with 'test' in the name
        for file_path in self.test_dir.rglob('*.poh'):
            if 'test' in file_path.stem.lower():
                if filter_pattern:
                    if re.search(filter_pattern, str(file_path), re.IGNORECASE):
                        test_files.append(file_path)
                else:
                    test_files.append(file_path)
        
        return sorted(test_files)
    
    def run_test_file(self, file_path: Path) -> PohTestResult:
        """Run a single test file and capture results"""
        start_time = time.time()
        pohlang_bin = self.find_pohlang_binary()
        
        if not pohlang_bin:
            return PohTestResult(
                name=file_path.stem,
                file=str(file_path),
                passed=False,
                duration=0.0,
                output='',
                error='PohLang binary not found'
            )
        
        try:
            result = subprocess.run(
                [str(pohlang_bin), '--run', str(file_path)],
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=30  # 30 second timeout
            )
            
            duration = time.time() - start_time
            output = result.stdout
            error = result.stderr if result.returncode != 0 else None
            passed = result.returncode == 0
            
            return PohTestResult(
                name=file_path.stem,
                file=str(file_path.relative_to(self.project_root)),
                passed=passed,
                duration=duration,
                output=output,
                error=error
            )
            
        except subprocess.TimeoutExpired:
            duration = time.time() - start_time
            return PohTestResult(
                name=file_path.stem,
                file=str(file_path.relative_to(self.project_root)),
                passed=False,
                duration=duration,
                output='',
                error='Test timed out after 30 seconds'
            )
        except Exception as e:
            duration = time.time() - start_time
            return PohTestResult(
                name=file_path.stem,
                file=str(file_path.relative_to(self.project_root)),
                passed=False,
                duration=duration,
                output='',
                error=str(e)
            )
    
    def run_all_tests(self, filter_pattern: Optional[str] = None) -> PohTestSuite:
        """Run all discovered tests"""
        test_files = self.discover_tests(filter_pattern)
        
        if not test_files:
            print("⚠️  No test files found")
            if not self.test_dir.exists():
                print(f"   Create a 'tests/' directory and add .poh files with 'test' in the name")
            return PohTestSuite(
                total=0,
                passed=0,
                failed=0,
                skipped=0,
                duration=0.0,
                results=[],
                timestamp=datetime.now().isoformat()
            )
        
        print(f"🧪 Running {len(test_files)} test(s)...\n")
        
        start_time = time.time()
        results = []
        
        for test_file in test_files:
            self.log(f"Running {test_file.name}...")
            result = self.run_test_file(test_file)
            results.append(result)
            
            # Print progress
            status = "✅" if result.passed else "❌"
            print(f"{status} {result.name} ({result.duration:.2f}s)")
            
            if result.error and self.verbose:
                print(f"   Error: {result.error}")
        
        total_duration = time.time() - start_time
        passed = sum(1 for r in results if r.passed)
        failed = sum(1 for r in results if not r.passed)
        
        test_suite = PohTestSuite(
            total=len(results),
            passed=passed,
            failed=failed,
            skipped=0,
            duration=total_duration,
            results=results,
            timestamp=datetime.now().isoformat()
        )
        
        # Save results
        self.save_results(test_suite)
        
        return test_suite
    
    def save_results(self, suite: PohTestSuite):
        """Save test results to JSON file"""
        self.results_dir.mkdir(parents=True, exist_ok=True)
        
        # Save latest results
        latest_file = self.results_dir / 'latest.json'
        with open(latest_file, 'w', encoding='utf-8') as f:
            json.dump({
                'suite': asdict(suite),
                'results': [asdict(r) for r in suite.results]
            }, f, indent=2)
        
        # Save timestamped results
        timestamp_file = self.results_dir / f"test-{suite.timestamp.replace(':', '-')}.json"
        with open(timestamp_file, 'w', encoding='utf-8') as f:
            json.dump({
                'suite': asdict(suite),
                'results': [asdict(r) for r in suite.results]
            }, f, indent=2)
    
    def print_summary(self, suite: PohTestSuite):
        """Print test suite summary"""
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print(f"Total:    {suite.total}")
        print(f"Passed:   {suite.passed} ✅")
        print(f"Failed:   {suite.failed} ❌")
        print(f"Duration: {suite.duration:.2f}s")
        print(f"Success:  {suite.success_rate:.1f}%")
        print("=" * 60)
        
        if suite.failed > 0:
            print("\nFailed tests:")
            for result in suite.results:
                if not result.passed:
                    print(f"  ❌ {result.name}")
                    if result.error:
                        print(f"     {result.error}")
    
    def watch_mode(self, filter_pattern: Optional[str] = None):
        """Watch for changes and re-run tests automatically"""
        print(f"👀 Watching for test changes in {self.test_dir}")
        print("Press Ctrl+C to stop\n")
        
        # Run tests initially
        suite = self.run_all_tests(filter_pattern)
        self.print_summary(suite)
        
        try:
            from watchdog.observers import Observer
            from watchdog.events import FileSystemEventHandler
            import threading
            
            class TestFileHandler(FileSystemEventHandler):
                def __init__(self, runner, filter_pattern):
                    self.runner = runner
                    self.filter_pattern = filter_pattern
                    self.debounce_timer = None
                
                def on_modified(self, event):
                    if event.is_directory or not event.src_path.endswith('.poh'):
                        return
                    self.trigger_rerun()
                
                def on_created(self, event):
                    if event.is_directory or not event.src_path.endswith('.poh'):
                        return
                    self.trigger_rerun()
                
                def trigger_rerun(self):
                    if self.debounce_timer:
                        self.debounce_timer.cancel()
                    
                    def do_rerun():
                        print("\n📝 Changes detected, re-running tests...\n")
                        suite = self.runner.run_all_tests(self.filter_pattern)
                        self.runner.print_summary(suite)
                        print("\n👀 Watching for changes...")
                    
                    self.debounce_timer = threading.Timer(0.5, do_rerun)
                    self.debounce_timer.start()
            
            event_handler = TestFileHandler(self, filter_pattern)
            observer = Observer()
            observer.schedule(event_handler, str(self.test_dir), recursive=True)
            # Also watch src directory for changes
            src_dir = self.project_root / 'src'
            if src_dir.exists():
                observer.schedule(event_handler, str(src_dir), recursive=True)
            observer.start()
            
            print("\n👀 Watching for changes...")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                observer.stop()
                print("\n⏹️  Watch mode stopped")
            observer.join()
            
        except ImportError:
            print("Note: Install 'watchdog' package for watch mode")
            print("  pip install watchdog")
    
    def generate_ci_report(self, suite: PohTestSuite, format: str = 'github') -> str:
        """Generate CI-friendly test report"""
        if format == 'github':
            report = "## Test Results\n\n"
            report += f"- **Total Tests:** {suite.total}\n"
            report += f"- **Passed:** {suite.passed} ✅\n"
            report += f"- **Failed:** {suite.failed} ❌\n"
            report += f"- **Duration:** {suite.duration:.2f}s\n"
            report += f"- **Success Rate:** {suite.success_rate:.1f}%\n\n"
            
            if suite.failed > 0:
                report += "### Failed Tests\n\n"
                for result in suite.results:
                    if not result.passed:
                        report += f"- ❌ **{result.name}**\n"
                        if result.error:
                            report += f"  ```\n  {result.error}\n  ```\n"
            
            return report
        
        elif format == 'junit':
            # JUnit XML format for CI/CD systems
            xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
            xml += f'<PohTestSuite name="PohLang Tests" tests="{suite.total}" '
            xml += f'failures="{suite.failed}" time="{suite.duration:.2f}">\n'
            
            for result in suite.results:
                xml += f'  <testcase name="{result.name}" '
                xml += f'classname="{result.file}" time="{result.duration:.2f}"'
                if result.passed:
                    xml += ' />\n'
                else:
                    xml += '>\n'
                    xml += f'    <failure message="{result.error or "Test failed"}">\n'
                    xml += f'      {result.error or ""}\n'
                    xml += '    </failure>\n'
                    xml += '  </testcase>\n'
            
            xml += '</PohTestSuite>\n'
            return xml
        
        return ''



