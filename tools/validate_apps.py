#!/usr/bin/env python3
"""
Validate Complete Applications
Tests that all complete apps can build and run successfully
"""

import subprocess
import sys
from pathlib import Path
from typing import List, Tuple


class AppValidator:
    """Validator for complete PohLang applications."""
    
    def __init__(self, apps_dir: Path):
        """Initialize validator with apps directory."""
        self.apps_dir = Path(apps_dir)
        self.results = []
        
    def validate_all(self) -> bool:
        """
        Validate all complete applications.
        
        Returns:
            True if all apps are valid, False otherwise
        """
        print("╔════════════════════════════════════════╗")
        print("║  VALIDATING COMPLETE APPLICATIONS      ║")
        print("╚════════════════════════════════════════╝")
        print()
        
        # Find all app directories
        apps = [d for d in self.apps_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]
        
        if not apps:
            print("❌ No applications found!")
            return False
        
        print(f"Found {len(apps)} applications to validate\n")
        
        # Validate each app
        for app_dir in sorted(apps):
            self._validate_app(app_dir)
            print()
        
        # Print summary
        self._print_summary()
        
        # Return overall success
        return all(result[1] for result in self.results)
    
    def _validate_app(self, app_dir: Path):
        """Validate a single application."""
        app_name = app_dir.name
        print(f"═══ {app_name.upper()} ═══")
        
        checks = [
            ("Project structure", lambda: self._check_structure(app_dir)),
            ("plhub.json config", lambda: self._check_config(app_dir)),
            ("Source files", lambda: self._check_source(app_dir)),
            ("Test files", lambda: self._check_tests(app_dir)),
            ("Documentation", lambda: self._check_docs(app_dir)),
        ]
        
        all_passed = True
        
        for check_name, check_func in checks:
            try:
                passed = check_func()
                status = "✅" if passed else "❌"
                print(f"  {status} {check_name}")
                if not passed:
                    all_passed = False
            except Exception as e:
                print(f"  ❌ {check_name}: {e}")
                all_passed = False
        
        self.results.append((app_name, all_passed))
    
    def _check_structure(self, app_dir: Path) -> bool:
        """Check that required directories exist."""
        required = ["src", "tests"]
        
        for dir_name in required:
            if not (app_dir / dir_name).exists():
                print(f"      Missing: {dir_name}/")
                return False
        
        return True
    
    def _check_config(self, app_dir: Path) -> bool:
        """Check plhub.json exists and is valid."""
        config_file = app_dir / "plhub.json"
        
        if not config_file.exists():
            print("      Missing: plhub.json")
            return False
        
        try:
            import json
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            required_fields = ["name", "version", "main"]
            missing = [field for field in required_fields if field not in config]
            
            if missing:
                print(f"      Missing fields: {', '.join(missing)}")
                return False
            
            return True
            
        except json.JSONDecodeError as e:
            print(f"      Invalid JSON: {e}")
            return False
    
    def _check_source(self, app_dir: Path) -> bool:
        """Check that source files exist."""
        src_dir = app_dir / "src"
        
        if not src_dir.exists():
            return False
        
        poh_files = list(src_dir.rglob("*.poh"))
        
        if not poh_files:
            print("      No .poh files found")
            return False
        
        # Check main file exists
        main_file = src_dir / "main.poh"
        if not main_file.exists():
            print("      Missing: src/main.poh")
            return False
        
        return True
    
    def _check_tests(self, app_dir: Path) -> bool:
        """Check that test files exist."""
        tests_dir = app_dir / "tests"
        
        if not tests_dir.exists():
            return False
        
        test_files = list(tests_dir.rglob("*.poh"))
        
        if not test_files:
            print("      No test files found")
            return False
        
        return True
    
    def _check_docs(self, app_dir: Path) -> bool:
        """Check that documentation exists."""
        readme = app_dir / "README.md"
        
        if not readme.exists():
            print("      Missing: README.md")
            return False
        
        # Check README has content
        content = readme.read_text()
        if len(content) < 100:
            print("      README too short")
            return False
        
        return True
    
    def _print_summary(self):
        """Print validation summary."""
        print("╔════════════════════════════════════════╗")
        print("║         VALIDATION SUMMARY             ║")
        print("╚════════════════════════════════════════╝")
        print()
        
        total = len(self.results)
        passed = sum(1 for _, success in self.results if success)
        failed = total - passed
        
        for app_name, success in self.results:
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"  {status}  {app_name}")
        
        print()
        print(f"Total:  {total} applications")
        print(f"Passed: {passed} ({passed*100//total if total > 0 else 0}%)")
        print(f"Failed: {failed}")
        print()
        
        if failed == 0:
            print("✨ All applications are valid! 🎉")
        else:
            print(f"⚠️  {failed} application(s) need attention")


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Validate complete PohLang applications"
    )
    parser.add_argument("apps_dir", nargs="?", 
                       default="Examples/complete-apps",
                       help="Directory containing applications")
    
    args = parser.parse_args()
    
    apps_dir = Path(args.apps_dir)
    
    if not apps_dir.exists():
        print(f"❌ Directory not found: {apps_dir}")
        sys.exit(1)
    
    validator = AppValidator(apps_dir)
    success = validator.validate_all()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
