#!/usr/bin/env python3
"""
Release Automation for PLHub

Automates the entire release process:
1. Version bumping across all files
2. Changelog generation
3. SDK packaging
4. Git tagging and pushing
5. PyPI publishing
6. GitHub release creation

Usage:
    python tools/release_automation.py --version 0.5.2 --type minor
    python tools/release_automation.py --bump patch  # Auto-increment patch version
    python tools/release_automation.py --publish-only  # Just publish existing version
"""

import argparse
import subprocess
import sys
import re
import shutil
import zipfile
from pathlib import Path
from datetime import datetime
from typing import List, Tuple
import json
import hashlib


class ReleaseAutomation:
    def __init__(self, plhub_root: Path):
        self.root = plhub_root
        self.sdk_dir = self.root / "plhub-sdk"
        self.dist_dir = self.root / "dist"
        self.current_version = self._get_current_version()
        
    def _get_current_version(self) -> str:
        """Extract current version from setup.py"""
        setup_py = self.root / "setup.py"
        content = setup_py.read_text(encoding="utf-8")
        match = re.search(r'version="([^"]+)"', content)
        if match:
            return match.group(1)
        return "0.0.0"
    
    def _bump_version(self, bump_type: str) -> str:
        """Bump version based on type (major, minor, patch)"""
        major, minor, patch = map(int, self.current_version.split("."))
        
        if bump_type == "major":
            return f"{major + 1}.0.0"
        elif bump_type == "minor":
            return f"{major}.{minor + 1}.0"
        elif bump_type == "patch":
            return f"{major}.{minor}.{patch + 1}"
        else:
            raise ValueError(f"Invalid bump type: {bump_type}")
    
    def update_version_strings(self, new_version: str, feature_name: str = None):
        """Update version in all relevant files"""
        print(f"📝 Updating version from {self.current_version} to {new_version}...")
        
        files_to_update = {
            "setup.py": [
                (r'version="[^"]+"', f'version="{new_version}"'),
            ],
            "plhub.py": [
                (r"PL-Hub v[\d.]+", f"PL-Hub v{new_version}"),
            ],
            "plhub-sdk/setup.py": [
                (r'version="[^"]+"', f'version="{new_version}"'),
            ],
            "plhub-sdk/plhub.py": [
                (r"PL-Hub v[\d.]+", f"PL-Hub v{new_version}"),
            ],
            "plhub-sdk/RELEASE_PACKAGE.md": [
                (r"Version\*\*: [\d.]+", f"Version**: {new_version}"),
                (r"PL-Hub v[\d.]+", f"PL-Hub v{new_version}"),
            ],
        }
        
        for file_path, replacements in files_to_update.items():
            full_path = self.root / file_path
            if not full_path.exists():
                print(f"  ⚠️  Skipping {file_path} (not found)")
                continue
                
            content = full_path.read_text(encoding="utf-8")
            for pattern, replacement in replacements:
                content = re.sub(pattern, replacement, content)
            
            full_path.write_text(content, encoding="utf-8")
            print(f"  ✅ Updated {file_path}")
        
        # Update CHANGELOG files
        self._update_changelog(new_version, feature_name)
        self._update_release_notes(new_version, feature_name)
    
    def _update_changelog(self, version: str, feature_name: str = None):
        """Add new version entry to CHANGELOG.md"""
        today = datetime.now().strftime("%Y-%m-%d")
        feature_text = f" - {feature_name}" if feature_name else ""
        
        new_entry = f"""## [{version}] - {today}{feature_text}

### Added
- New features and improvements

### Changed
- Updates and modifications

### Fixed
- Bug fixes and corrections

"""
        
        for changelog_file in [self.root / "CHANGELOG.md", self.sdk_dir / "CHANGELOG.md"]:
            if not changelog_file.exists():
                continue
                
            content = changelog_file.read_text(encoding="utf-8")
            
            # Find insertion point (after header, before first version)
            lines = content.split("\n")
            insert_idx = 0
            for i, line in enumerate(lines):
                if line.startswith("## ["):
                    insert_idx = i
                    break
            
            # Insert new entry
            lines.insert(insert_idx, new_entry.rstrip())
            changelog_file.write_text("\n".join(lines), encoding="utf-8")
            print(f"  ✅ Updated {changelog_file.name}")
    
    def _update_release_notes(self, version: str, feature_name: str = None):
        """Create/update RELEASE_NOTES.md"""
        today = datetime.now().strftime("%B %d, %Y")
        feature_text = f" - {feature_name}" if feature_name else ""
        
        content = f"""# PL-Hub v{version} Release Notes{feature_text}

**Release Date**: {today}

## 🎉 What's New

### Major Features
- [Add major features here]

### Improvements
- [Add improvements here]

### Bug Fixes
- [Add bug fixes here]

## 📦 Installation

```bash
# Install from PyPI
pip install --upgrade plhub

# Or install from source
git clone https://github.com/AlhaqGH/PLHub.git
cd PLHub
pip install -e .
```

## 🚀 Quick Start

```bash
# Create a new project
plhub create my_app --template basic

# Run your program
plhub run src/main.poh

# Build for release
plhub build --release
```

## 🔗 Links

- **GitHub**: https://github.com/AlhaqGH/PLHub
- **Documentation**: https://github.com/AlhaqGH/PLHub/docs
- **PyPI**: https://pypi.org/project/plhub/

## 🙏 Thank You

Thank you to all contributors and users of PL-Hub and PohLang!

---

For detailed changes, see [CHANGELOG.md](CHANGELOG.md)
"""
        
        release_notes = self.root / "RELEASE_NOTES.md"
        release_notes.write_text(content, encoding="utf-8")
        print(f"  ✅ Created RELEASE_NOTES.md")
    
    def create_sdk_package(self, version: str) -> Path:
        """Create SDK zip package"""
        print(f"\n📦 Creating SDK package...")
        
        zip_name = f"plhub-sdk-{version}.zip"
        zip_path = self.root / zip_name
        
        # Remove old zip if exists
        if zip_path.exists():
            zip_path.unlink()
        
        # Create zip
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for item in self.sdk_dir.rglob("*"):
                if item.is_file():
                    # Skip pycache and other build artifacts
                    if "__pycache__" in str(item) or item.suffix in [".pyc", ".pyo"]:
                        continue
                    
                    arcname = item.relative_to(self.sdk_dir.parent)
                    zipf.write(item, arcname)
        
        # Calculate hash
        sha256_hash = hashlib.sha256()
        with open(zip_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        
        hash_file = zip_path.with_suffix(".zip.sha256")
        hash_file.write_text(f"{sha256_hash.hexdigest()}  {zip_name}\n")
        
        size_mb = zip_path.stat().st_size / (1024 * 1024)
        print(f"  ✅ Created {zip_name} ({size_mb:.2f} MB)")
        print(f"  ✅ Created {hash_file.name}")
        
        return zip_path
    
    def git_operations(self, version: str, dry_run: bool = False):
        """Perform git commit, tag, and push"""
        print(f"\n🔧 Git operations...")
        
        commands = [
            ["git", "add", "."],
            ["git", "commit", "-m", f"Release v{version}"],
            ["git", "tag", "-a", f"v{version}", "-m", f"Release v{version}"],
            ["git", "push", "origin", "main"],
            ["git", "push", "origin", f"v{version}"],
        ]
        
        for cmd in commands:
            cmd_str = " ".join(cmd)
            if dry_run:
                print(f"  🔍 Would run: {cmd_str}")
            else:
                print(f"  ⚙️  Running: {cmd_str}")
                try:
                    result = subprocess.run(
                        cmd,
                        cwd=self.root,
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    if result.stdout:
                        print(f"     {result.stdout.strip()}")
                except subprocess.CalledProcessError as e:
                    print(f"  ❌ Error: {e}")
                    print(f"     {e.stderr}")
                    if "nothing to commit" not in e.stdout and "nothing to commit" not in e.stderr:
                        return False
        
        print(f"  ✅ Git operations complete")
        return True
    
    def build_distributions(self):
        """Build wheel and source distributions"""
        print(f"\n🏗️  Building distributions...")
        
        # Clean old builds
        if self.dist_dir.exists():
            shutil.rmtree(self.dist_dir)
        
        build_dir = self.root / "build"
        if build_dir.exists():
            shutil.rmtree(build_dir)
        
        egg_info = self.root / "plhub.egg-info"
        if egg_info.exists():
            shutil.rmtree(egg_info)
        
        # Build distributions
        commands = [
            [sys.executable, "setup.py", "sdist", "bdist_wheel"],
        ]
        
        for cmd in commands:
            print(f"  ⚙️  Running: {' '.join(cmd)}")
            try:
                result = subprocess.run(
                    cmd,
                    cwd=self.root,
                    capture_output=True,
                    text=True,
                    check=True
                )
                if result.stdout:
                    print(f"     {result.stdout.strip()}")
            except subprocess.CalledProcessError as e:
                print(f"  ❌ Error building distributions: {e}")
                print(f"     {e.stderr}")
                return False
        
        # List created files
        if self.dist_dir.exists():
            print(f"\n  📦 Created distributions:")
            for item in self.dist_dir.iterdir():
                size_mb = item.stat().st_size / (1024 * 1024)
                print(f"     - {item.name} ({size_mb:.2f} MB)")
        
        print(f"  ✅ Distributions built successfully")
        return True
    
    def publish_to_pypi(self, test_pypi: bool = False, dry_run: bool = False):
        """Publish to PyPI using twine"""
        print(f"\n🚀 Publishing to {'Test ' if test_pypi else ''}PyPI...")
        
        # Check if twine is installed
        try:
            subprocess.run([sys.executable, "-m", "twine", "--version"],
                         capture_output=True, check=True)
        except subprocess.CalledProcessError:
            print("  ❌ twine not found. Install with: pip install twine")
            return False
        
        # Publish
        repo_arg = "--repository testpypi" if test_pypi else ""
        cmd = [sys.executable, "-m", "twine", "upload"]
        if repo_arg:
            cmd.append(repo_arg)
        cmd.append("dist/*")
        
        cmd_str = " ".join(cmd)
        if dry_run:
            print(f"  🔍 Would run: {cmd_str}")
            return True
        
        print(f"  ⚙️  Running: {cmd_str}")
        print(f"  ℹ️  You may be prompted for PyPI credentials...")
        
        try:
            result = subprocess.run(
                cmd,
                cwd=self.root,
                check=True
            )
            print(f"  ✅ Published to {'Test ' if test_pypi else ''}PyPI successfully")
            
            # Show package URL
            pypi_url = f"https://{'test.' if test_pypi else ''}pypi.org/project/plhub/"
            print(f"  🔗 Package URL: {pypi_url}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"  ❌ Error publishing: {e}")
            return False
    
    def create_github_release(self, version: str, dry_run: bool = False):
        """Open GitHub release page in browser"""
        print(f"\n🌐 Creating GitHub release...")
        
        url = f"https://github.com/AlhaqGH/PLHub/releases/new?tag=v{version}"
        
        if dry_run:
            print(f"  🔍 Would open: {url}")
        else:
            print(f"  🌐 Opening GitHub release page: {url}")
            import webbrowser
            webbrowser.open(url)
            print(f"  ℹ️  Please complete the release on GitHub:")
            print(f"     1. Review the pre-filled tag and title")
            print(f"     2. Copy release notes from RELEASE_NOTES.md")
            print(f"     3. Attach plhub-sdk-{version}.zip")
            print(f"     4. Click 'Publish release'")
        
        return True
    
    def full_release(self, version: str = None, bump_type: str = None, 
                    feature_name: str = None, test_pypi: bool = False,
                    skip_git: bool = False, skip_pypi: bool = False,
                    dry_run: bool = False):
        """Execute full release process"""
        
        # Determine version
        if version:
            new_version = version
        elif bump_type:
            new_version = self._bump_version(bump_type)
        else:
            print("❌ Must specify either --version or --bump")
            return False
        
        print(f"\n{'='*60}")
        print(f"🚀 PL-Hub Release Automation v{new_version}")
        print(f"{'='*60}\n")
        
        if dry_run:
            print("⚠️  DRY RUN MODE - No changes will be made\n")
        
        # Step 1: Update versions
        self.update_version_strings(new_version, feature_name)
        
        # Step 2: Create SDK package
        sdk_zip = self.create_sdk_package(new_version)
        
        # Step 3: Git operations
        if not skip_git:
            if not self.git_operations(new_version, dry_run):
                print("❌ Git operations failed")
                return False
        else:
            print("\n⏭️  Skipping Git operations (--skip-git)")
        
        # Step 4: Build distributions
        if not skip_pypi:
            if not self.build_distributions():
                print("❌ Build failed")
                return False
        
        # Step 5: Publish to PyPI
        if not skip_pypi:
            if not self.publish_to_pypi(test_pypi, dry_run):
                print("❌ PyPI publish failed")
                return False
        else:
            print("\n⏭️  Skipping PyPI publish (--skip-pypi)")
        
        # Step 6: GitHub release
        self.create_github_release(new_version, dry_run)
        
        # Summary
        print(f"\n{'='*60}")
        print(f"✅ Release v{new_version} completed successfully!")
        print(f"{'='*60}\n")
        
        print("📋 Next steps:")
        print("  1. Complete the GitHub release page")
        print(f"  2. Verify package on PyPI: https://pypi.org/project/plhub/")
        print(f"  3. Test installation: pip install --upgrade plhub=={new_version}")
        print("  4. Update documentation if needed")
        print("  5. Announce the release!")
        
        return True


def main():
    parser = argparse.ArgumentParser(
        description="Automate PLHub release process",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Bump patch version (0.5.1 -> 0.5.2)
  python tools/release_automation.py --bump patch
  
  # Bump minor version (0.5.1 -> 0.6.0)
  python tools/release_automation.py --bump minor --feature "New UI System"
  
  # Specific version
  python tools/release_automation.py --version 1.0.0 --feature "Stable Release"
  
  # Dry run (no changes)
  python tools/release_automation.py --bump patch --dry-run
  
  # Publish only (skip git)
  python tools/release_automation.py --version 0.5.1 --skip-git --publish-only
  
  # Test PyPI first
  python tools/release_automation.py --bump patch --test-pypi
        """
    )
    
    parser.add_argument("--version", help="Specific version number (e.g., 0.5.2)")
    parser.add_argument("--bump", choices=["major", "minor", "patch"],
                       help="Auto-bump version type")
    parser.add_argument("--feature", help="Feature name for release notes")
    parser.add_argument("--test-pypi", action="store_true",
                       help="Publish to Test PyPI first")
    parser.add_argument("--skip-git", action="store_true",
                       help="Skip git operations")
    parser.add_argument("--skip-pypi", action="store_true",
                       help="Skip PyPI publishing")
    parser.add_argument("--publish-only", action="store_true",
                       help="Only build and publish (skip version updates)")
    parser.add_argument("--dry-run", action="store_true",
                       help="Show what would be done without making changes")
    
    args = parser.parse_args()
    
    # Validation
    if not args.version and not args.bump and not args.publish_only:
        parser.error("Must specify --version, --bump, or --publish-only")
    
    # Get PLHub root
    plhub_root = Path(__file__).parent.parent
    
    # Create automation instance
    automation = ReleaseAutomation(plhub_root)
    
    # Run release
    if args.publish_only:
        # Just build and publish current version
        print(f"📦 Publishing current version: {automation.current_version}")
        
        if not args.skip_pypi:
            automation.build_distributions()
            automation.publish_to_pypi(args.test_pypi, args.dry_run)
        
        automation.create_github_release(automation.current_version, args.dry_run)
    else:
        # Full release process
        success = automation.full_release(
            version=args.version,
            bump_type=args.bump,
            feature_name=args.feature,
            test_pypi=args.test_pypi,
            skip_git=args.skip_git,
            skip_pypi=args.skip_pypi,
            dry_run=args.dry_run
        )
        
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
