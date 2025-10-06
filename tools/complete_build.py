#!/usr/bin/env python3
"""
Enhanced Build System for Complete PohLang Applications
Handles dependencies, assets, optimization, and packaging
"""

import json
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
import sys
import os


class CompleteBuildManager:
    """Build manager for complete PohLang applications."""
    
    def __init__(self, project_root: Path):
        """
        Initialize build manager.
        
        Args:
            project_root: Path to project root directory
        """
        self.project_root = Path(project_root)
        self.build_dir = self.project_root / "build"
        self.config = self._load_config()
        
    def _load_config(self) -> Dict:
        """Load plhub.json configuration."""
        config_path = self.project_root / "plhub.json"
        if not config_path.exists():
            raise FileNotFoundError(f"Project configuration not found: {config_path}")
        
        with open(config_path, 'r') as f:
            return json.load(f)
    
    def build_complete_app(
        self,
        target: str = "bytecode",
        release: bool = False,
        optimize: bool = True,
        include_tests: bool = False,
        bundle_assets: bool = True,
        output_dir: Optional[Path] = None
    ) -> bool:
        """
        Build a complete application with all features.
        
        Args:
            target: Build target (bytecode, native, dart)
            release: Build in release mode
            optimize: Enable optimizations
            include_tests: Include test files
            bundle_assets: Include assets directory
            output_dir: Custom output directory
            
        Returns:
            True if build succeeded, False otherwise
        """
        print("╔════════════════════════════════════════╗")
        print("║    BUILDING COMPLETE APPLICATION       ║")
        print("╚════════════════════════════════════════╝")
        print()
        
        # Validate project structure
        if not self._validate_project():
            return False
        
        # Setup build directory
        output = output_dir or self.build_dir
        output.mkdir(parents=True, exist_ok=True)
        
        # Build steps
        steps = [
            ("Checking dependencies", self._check_dependencies),
            ("Compiling source code", lambda: self._compile_source(target, release, optimize)),
            ("Processing assets", lambda: self._process_assets(output, bundle_assets)),
            ("Generating documentation", lambda: self._generate_docs(output)),
            ("Creating package manifest", lambda: self._create_manifest(output)),
        ]
        
        if include_tests:
            steps.append(("Including tests", lambda: self._include_tests(output)))
        
        # Execute build steps
        for step_name, step_func in steps:
            print(f"⏳ {step_name}...")
            try:
                if not step_func():
                    print(f"❌ Failed: {step_name}")
                    return False
                print(f"✅ {step_name} completed")
            except Exception as e:
                print(f"❌ Error in {step_name}: {e}")
                return False
            print()
        
        # Build summary
        self._print_build_summary(output, target, release)
        
        return True
    
    def _validate_project(self) -> bool:
        """Validate project structure and required files."""
        print("⏳ Validating project structure...")
        
        required = {
            "plhub.json": self.project_root / "plhub.json",
            "main file": self.project_root / self.config.get("main", "src/main.poh"),
            "src directory": self.project_root / "src",
        }
        
        for name, path in required.items():
            if not path.exists():
                print(f"❌ Missing required {name}: {path}")
                return False
        
        print("✅ Project structure valid")
        return True
    
    def _check_dependencies(self) -> bool:
        """Check and resolve dependencies."""
        deps = self.config.get("dependencies", {})
        
        if not deps:
            print("   No dependencies declared")
            return True
        
        print(f"   Found {len(deps)} dependencies:")
        for name, version in deps.items():
            print(f"     • {name}@{version}")
        
        # TODO: Actual dependency resolution
        print("   ⚠️  Dependency resolution not yet implemented")
        
        return True
    
    def _compile_source(self, target: str, release: bool, optimize: bool) -> bool:
        """Compile source code to target format."""
        main_file = self.project_root / self.config.get("main", "src/main.poh")
        
        if target == "bytecode":
            return self._compile_bytecode(main_file, release, optimize)
        elif target == "dart":
            return self._transpile_dart(main_file)
        elif target == "native":
            return self._compile_native(main_file, release, optimize)
        else:
            print(f"   Unknown target: {target}")
            return False
    
    def _compile_bytecode(self, main_file: Path, release: bool, optimize: bool) -> bool:
        """Compile to bytecode (.pbc)."""
        # Find pohlang compiler
        pohlang_bin = self._find_pohlang_binary()
        if not pohlang_bin:
            print("   ❌ PohLang compiler not found")
            return False
        
        output_file = self.build_dir / (self.config.get("name", "app") + ".pbc")
        
        cmd = [pohlang_bin, '--compile', str(main_file), '-o', str(output_file)]
        
        print(f"   Compiling: {main_file.name} → {output_file.name}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"   ❌ Compilation failed:")
            print(f"   {result.stderr}")
            return False
        
        print(f"   ✅ Bytecode: {output_file}")
        return True
    
    def _transpile_dart(self, main_file: Path) -> bool:
        """Transpile to Dart."""
        # TODO: Implement Dart transpilation
        print("   ⚠️  Dart transpilation not yet fully implemented")
        return True
    
    def _compile_native(self, main_file: Path, release: bool, optimize: bool) -> bool:
        """Compile to native executable."""
        # TODO: Implement native compilation
        print("   ⚠️  Native compilation not yet implemented")
        print("   Using bytecode instead")
        return self._compile_bytecode(main_file, release, optimize)
    
    def _process_assets(self, output_dir: Path, bundle: bool) -> bool:
        """Process and bundle assets."""
        assets_dir = self.project_root / "assets"
        
        if not assets_dir.exists():
            print("   No assets directory found")
            return True
        
        if not bundle:
            print("   Skipping asset bundling")
            return True
        
        output_assets = output_dir / "assets"
        
        if output_assets.exists():
            shutil.rmtree(output_assets)
        
        shutil.copytree(assets_dir, output_assets)
        
        # Count files
        asset_files = list(output_assets.rglob("*"))
        asset_count = len([f for f in asset_files if f.is_file()])
        
        print(f"   Bundled {asset_count} asset files")
        return True
    
    def _generate_docs(self, output_dir: Path) -> bool:
        """Generate documentation for the build."""
        docs_dir = output_dir / "docs"
        docs_dir.mkdir(exist_ok=True)
        
        # Copy README if exists
        readme = self.project_root / "README.md"
        if readme.exists():
            shutil.copy(readme, docs_dir / "README.md")
            print("   Included README.md")
        
        # Generate build info
        build_info = {
            "project": self.config.get("name", "unknown"),
            "version": self.config.get("version", "0.0.0"),
            "description": self.config.get("description", ""),
            "author": self.config.get("author", ""),
            "license": self.config.get("license", ""),
        }
        
        with open(docs_dir / "BUILD_INFO.json", 'w') as f:
            json.dump(build_info, f, indent=2)
        
        print("   Generated BUILD_INFO.json")
        return True
    
    def _create_manifest(self, output_dir: Path) -> bool:
        """Create package manifest."""
        manifest = {
            "name": self.config.get("name", "app"),
            "version": self.config.get("version", "0.0.0"),
            "description": self.config.get("description", ""),
            "main": self.config.get("main", "src/main.poh"),
            "dependencies": self.config.get("dependencies", {}),
            "build": {
                "timestamp": subprocess.check_output(
                    ["powershell", "-Command", "Get-Date -Format 'yyyy-MM-dd HH:mm:ss'"]
                    if sys.platform == "win32" else ["date", "+%Y-%m-%d %H:%M:%S"]
                ).decode().strip(),
                "platform": sys.platform,
            }
        }
        
        with open(output_dir / "manifest.json", 'w') as f:
            json.dump(manifest, f, indent=2)
        
        print("   Created manifest.json")
        return True
    
    def _include_tests(self, output_dir: Path) -> bool:
        """Include test files in build."""
        tests_dir = self.project_root / "tests"
        
        if not tests_dir.exists():
            print("   No tests directory found")
            return True
        
        output_tests = output_dir / "tests"
        
        if output_tests.exists():
            shutil.rmtree(output_tests)
        
        shutil.copytree(tests_dir, output_tests)
        
        test_files = list(output_tests.rglob("*.poh"))
        print(f"   Included {len(test_files)} test files")
        
        return True
    
    def _find_pohlang_binary(self) -> Optional[Path]:
        """Find pohlang/pohlangc binary."""
        # Check Runtime/bin
        runtime_bin = Path(__file__).parent.parent / "Runtime" / "bin"
        
        for name in ["pohlang.exe", "pohlang", "pohlangc.exe", "pohlangc"]:
            binary = runtime_bin / name
            if binary.exists():
                return binary
        
        # Check PATH
        try:
            result = subprocess.run(
                ["where" if sys.platform == "win32" else "which", "pohlang"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return Path(result.stdout.strip().split('\n')[0])
        except:
            pass
        
        return None
    
    def _print_build_summary(self, output_dir: Path, target: str, release: bool):
        """Print build summary."""
        mode = "RELEASE" if release else "DEBUG"
        
        print()
        print("╔════════════════════════════════════════╗")
        print("║         BUILD SUCCESSFUL! ✓            ║")
        print("╚════════════════════════════════════════╝")
        print()
        print(f"📦 Package: {self.config.get('name', 'app')}")
        print(f"🏷️  Version: {self.config.get('version', '0.0.0')}")
        print(f"🎯 Target:  {target}")
        print(f"🔧 Mode:    {mode}")
        print(f"📁 Output:  {output_dir}")
        print()
        
        # List output files
        print("📄 Build artifacts:")
        for item in sorted(output_dir.rglob("*")):
            if item.is_file():
                rel_path = item.relative_to(output_dir)
                size = item.stat().st_size
                size_str = self._format_size(size)
                print(f"   • {rel_path} ({size_str})")
        
        print()
        print("✨ Build complete! Ready to deploy.")
        print()
    
    def _format_size(self, bytes_size: int) -> str:
        """Format file size for display."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.1f} {unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.1f} TB"


def main():
    """CLI entry point for build tool."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Enhanced build system for complete PohLang applications"
    )
    parser.add_argument("project", nargs="?", default=".",
                       help="Project directory (default: current directory)")
    parser.add_argument("--target", default="bytecode",
                       choices=["bytecode", "native", "dart"],
                       help="Build target")
    parser.add_argument("--release", action="store_true",
                       help="Build in release mode")
    parser.add_argument("--debug", action="store_true",
                       help="Build in debug mode")
    parser.add_argument("--no-optimize", action="store_true",
                       help="Disable optimizations")
    parser.add_argument("--include-tests", action="store_true",
                       help="Include test files")
    parser.add_argument("--no-assets", action="store_true",
                       help="Don't bundle assets")
    parser.add_argument("-o", "--out", type=Path,
                       help="Output directory")
    
    args = parser.parse_args()
    
    try:
        builder = CompleteBuildManager(Path(args.project))
        
        success = builder.build_complete_app(
            target=args.target,
            release=args.release,
            optimize=not args.no_optimize,
            include_tests=args.include_tests,
            bundle_assets=not args.no_assets,
            output_dir=args.out
        )
        
        sys.exit(0 if success else 1)
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
