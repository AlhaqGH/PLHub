#!/usr/bin/env python3
"""
SDK Update Automation

Automatically sync changes from main PLHub to SDK when features are updated.

Usage:
    python tools/update_sdk.py                    # Sync all files
    python tools/update_sdk.py --files plhub.py   # Sync specific files
    python tools/update_sdk.py --verify           # Verify SDK is in sync
"""

import argparse
import shutil
import hashlib
from pathlib import Path
from typing import List, Set


class SDKUpdater:
    def __init__(self, plhub_root: Path):
        self.root = plhub_root
        self.sdk_dir = self.root / "plhub-sdk"
        
        # Files to sync from main to SDK
        self.sync_files = [
            "plhub.py",
            "setup.py",
            "README.md",
            "CHANGELOG.md",
            "LICENSE",
            "requirements.txt",
        ]
        
        # Directories to sync
        self.sync_dirs = [
            "CLI",
            "tools",
            "templates",
            "docs",
            "Examples",
        ]
    
    def _get_file_hash(self, file_path: Path) -> str:
        """Calculate SHA256 hash of a file"""
        if not file_path.exists():
            return ""
        
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def verify_sync(self) -> List[str]:
        """Check which files are out of sync"""
        out_of_sync = []
        
        print("🔍 Verifying SDK sync status...\n")
        
        # Check files
        for file_name in self.sync_files:
            main_file = self.root / file_name
            sdk_file = self.sdk_dir / file_name
            
            if not main_file.exists():
                continue
            
            main_hash = self._get_file_hash(main_file)
            sdk_hash = self._get_file_hash(sdk_file)
            
            if main_hash != sdk_hash:
                out_of_sync.append(file_name)
                status = "❌ OUT OF SYNC"
            else:
                status = "✅ IN SYNC"
            
            print(f"  {status}: {file_name}")
        
        # Check directories (just verify existence for now)
        for dir_name in self.sync_dirs:
            main_dir = self.root / dir_name
            sdk_dir = self.sdk_dir / dir_name
            
            if not main_dir.exists():
                continue
            
            if not sdk_dir.exists():
                out_of_sync.append(dir_name)
                print(f"  ❌ MISSING: {dir_name}/")
            else:
                print(f"  ✅ EXISTS: {dir_name}/")
        
        return out_of_sync
    
    def sync_file(self, file_name: str, force: bool = False):
        """Sync a single file from main to SDK"""
        main_file = self.root / file_name
        sdk_file = self.sdk_dir / file_name
        
        if not main_file.exists():
            print(f"  ⚠️  Skipping {file_name} (not found in main)")
            return False
        
        # Check if different
        if not force:
            main_hash = self._get_file_hash(main_file)
            sdk_hash = self._get_file_hash(sdk_file)
            
            if main_hash == sdk_hash:
                print(f"  ⏭️  Skipping {file_name} (already in sync)")
                return True
        
        # Copy file
        sdk_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(main_file, sdk_file)
        print(f"  ✅ Synced {file_name}")
        return True
    
    def sync_directory(self, dir_name: str, force: bool = False):
        """Sync a directory from main to SDK"""
        main_dir = self.root / dir_name
        sdk_dir = self.sdk_dir / dir_name
        
        if not main_dir.exists():
            print(f"  ⚠️  Skipping {dir_name}/ (not found in main)")
            return False
        
        # Remove SDK directory if forcing full sync
        if force and sdk_dir.exists():
            shutil.rmtree(sdk_dir)
        
        # Copy directory
        if not sdk_dir.exists() or force:
            shutil.copytree(main_dir, sdk_dir, dirs_exist_ok=True)
            file_count = sum(1 for _ in sdk_dir.rglob("*") if _.is_file())
            print(f"  ✅ Synced {dir_name}/ ({file_count} files)")
        else:
            print(f"  ⏭️  Skipping {dir_name}/ (use --force to overwrite)")
        
        return True
    
    def sync_all(self, force: bool = False, specific_files: List[str] = None):
        """Sync all files and directories"""
        print("🔄 Syncing PLHub → SDK...\n")
        
        if specific_files:
            # Sync only specific files
            for file_name in specific_files:
                if file_name in self.sync_files:
                    self.sync_file(file_name, force)
                elif file_name.rstrip("/") in self.sync_dirs:
                    self.sync_directory(file_name.rstrip("/"), force)
                else:
                    print(f"  ⚠️  Unknown file/directory: {file_name}")
        else:
            # Sync all files
            print("📄 Files:")
            for file_name in self.sync_files:
                self.sync_file(file_name, force)
            
            print("\n📁 Directories:")
            for dir_name in self.sync_dirs:
                self.sync_directory(dir_name, force)
        
        print("\n✅ SDK sync completed!")
    
    def create_sync_report(self) -> str:
        """Create a detailed sync report"""
        out_of_sync = self.verify_sync()
        
        if not out_of_sync:
            return "\n✅ SDK is fully in sync with main PLHub"
        
        report = "\n❌ SDK is out of sync:\n"
        for item in out_of_sync:
            report += f"  - {item}\n"
        report += "\nRun: python tools/update_sdk.py --sync"
        
        return report


def main():
    parser = argparse.ArgumentParser(
        description="Sync PLHub changes to SDK",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Verify sync status
  python tools/update_sdk.py --verify
  
  # Sync all files
  python tools/update_sdk.py --sync
  
  # Force sync (overwrite all)
  python tools/update_sdk.py --sync --force
  
  # Sync specific files
  python tools/update_sdk.py --sync --files plhub.py setup.py
  
  # Create sync report
  python tools/update_sdk.py --report
        """
    )
    
    parser.add_argument("--verify", action="store_true",
                       help="Verify SDK sync status")
    parser.add_argument("--sync", action="store_true",
                       help="Sync files to SDK")
    parser.add_argument("--force", action="store_true",
                       help="Force overwrite all files")
    parser.add_argument("--files", nargs="+",
                       help="Specific files to sync")
    parser.add_argument("--report", action="store_true",
                       help="Generate sync report")
    
    args = parser.parse_args()
    
    # Default to verify if no action specified
    if not any([args.verify, args.sync, args.report]):
        args.verify = True
    
    # Get PLHub root
    plhub_root = Path(__file__).parent.parent
    
    # Create updater
    updater = SDKUpdater(plhub_root)
    
    # Execute actions
    if args.verify:
        out_of_sync = updater.verify_sync()
        if out_of_sync:
            print(f"\n⚠️  {len(out_of_sync)} items out of sync")
            print("   Run: python tools/update_sdk.py --sync")
    
    if args.sync:
        updater.sync_all(args.force, args.files)
    
    if args.report:
        print(updater.create_sync_report())


if __name__ == "__main__":
    main()
