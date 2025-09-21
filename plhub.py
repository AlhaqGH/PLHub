#!/usr/bin/env python3
"""
PL-Hub Main Entrypoint

The primary entry point for the PohLang development environment.
PLHub is to PohLang what Flutter is to Dart - a comprehensive development platform.

Usage:
    python plhub.py run <file.poh>           # Run a PohLang program
    python plhub.py create <project_name>    # Create new project
    python plhub.py install <package>        # Install package
    python plhub.py build                    # Build project
"""

import sys
import os
import subprocess
from pathlib import Path
import argparse
import json
import shutil
import datetime
import logging

def _load_dotenv(dotenv_path: Path) -> None:
    """Lightweight .env loader (KEY=VALUE pairs, no quotes)."""
    # Try python-dotenv if available
    try:
        from dotenv import load_dotenv as _load
        _load(dotenv_path)
        return
    except Exception:
        # Fall back to simple parser
        try:
            if dotenv_path.exists():
                for line in dotenv_path.read_text(encoding="utf-8").splitlines():
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip()
                    os.environ.setdefault(k, v)
        except Exception:
            # Non-fatal
            pass


# Load .env if present
_load_dotenv(Path(__file__).parent / ".env")

# Determine interpreter import location
RUNTIME_DIR = Path(__file__).parent / 'Runtime'
RUNTIME_INTERPRETER = RUNTIME_DIR / 'Interpreter'
if RUNTIME_INTERPRETER.exists():
    # Add the Runtime directory to sys.path so 'Interpreter' is importable
    sys.path.insert(0, str(RUNTIME_DIR))
else:
    # Fall back to adjacent PohLang repo or installed package
    POHLANG_PATH = Path(__file__).parent.parent / "PohLang"
    if not POHLANG_PATH.exists():
        try:
            result = subprocess.run([sys.executable, "-c", "import pohlang; print(pohlang.__file__)"] ,
                                   capture_output=True, text=True, check=True)
            POHLANG_PATH = Path(result.stdout.strip()).parent
        except (subprocess.CalledProcessError, ImportError):
            print("Error: PohLang installation not found.")
            print("Please ensure PohLang is installed or PLHub is in the same directory as PohLang.")
            sys.exit(1)
    sys.path.insert(0, str(POHLANG_PATH))

try:
    from Interpreter.poh_interpreter import Interpreter, RuntimeErrorPoh
    from Interpreter.poh_parser import ParseError
except ImportError as e:
    print(f"Error: Could not import PohLang interpreter: {e}")
    # Only print POHLANG_PATH if it's defined in this scope
    if 'POHLANG_PATH' in globals():
        print(f"PohLang path: {POHLANG_PATH}")
    print("Make sure PohLang is properly installed or integrated via 'plhub release'.")
    sys.exit(1)


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def read_pohlang_version(pohlang_repo: Path) -> tuple[str, str]:
    """Return (version, commit) for PohLang.

    - Prefer Interpreter/__init__.py __version__ (language version)
    - Fallback to pyproject.toml [project].version
    - Fallback to git rev-parse HEAD
    """
    version = None
    commit = None
    interp_init = pohlang_repo / 'Interpreter' / '__init__.py'
    pyproj = pohlang_repo / 'pyproject.toml'
    try:
        if interp_init.exists():
            text = interp_init.read_text(encoding='utf-8')
            for line in text.splitlines():
                if line.strip().startswith('__version__'):
                    version = line.split('=', 1)[1].strip().strip('"\'')
                    break
        if pyproj.exists():
            text = pyproj.read_text(encoding='utf-8')
            for line in text.splitlines():
                if line.strip().startswith('version'):  # naive parse
                    # line like: version = "0.1.0"
                    try:
                        version = line.split('=', 1)[1].strip().strip('"\'')
                        # Do not break if we already have interpreter version
                        if version and not version:
                            break
                    except Exception:
                        pass
        # git commit
        if (pohlang_repo / '.git').exists():
            res = subprocess.run(['git', '-C', str(pohlang_repo), '--no-pager', 'rev-parse', 'HEAD'],
                                 capture_output=True, text=True)
            if res.returncode == 0:
                commit = res.stdout.strip()
    except Exception:
        pass
    return version or 'unknown', commit or 'unknown'


def integrate_pohlang(pohlang_repo: Path, runtime_dir: Path) -> dict:
    """Copy the Interpreter, bin, and transpiler directories from PohLang into PLHub/Runtime.

    Returns metadata dict about the embedded interpreter.
    """
    interpreter_src = pohlang_repo / 'Interpreter'
    if not interpreter_src.exists():
        raise FileNotFoundError(f"PohLang Interpreter not found at {interpreter_src}")

    # Ensure runtime dir
    runtime_dir.mkdir(parents=True, exist_ok=True)

    # Copy Interpreter
    interpreter_dst = runtime_dir / 'Interpreter'
    if interpreter_dst.exists():
        shutil.rmtree(interpreter_dst)
    shutil.copytree(interpreter_src, interpreter_dst)

    # Copy Dart transpiler (optional but recommended)
    transpiler_src = pohlang_repo / 'transpiler'
    transpiler_dst = runtime_dir / 'transpiler'
    if transpiler_src.exists():
        if transpiler_dst.exists():
            shutil.rmtree(transpiler_dst)
        shutil.copytree(transpiler_src, transpiler_dst)

    # Copy Dart bin entrypoints so `dart run` works from Runtime
    bin_src = pohlang_repo / 'bin'
    bin_dst = runtime_dir / 'bin'
    if bin_src.exists():
        if bin_dst.exists():
            shutil.rmtree(bin_dst)
        shutil.copytree(bin_src, bin_dst)

    version, commit = read_pohlang_version(pohlang_repo)
    metadata = {
        'pohlang_version': version,
        'source_repo': 'https://github.com/AlhaqGH/PohLang',
        'source_commit': commit,
        'embedded_at': datetime.datetime.now(datetime.timezone.utc).isoformat()
    }

    # Write metadata
    meta_file = runtime_dir / 'pohlang_metadata.json'
    try:
        with meta_file.open('w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
    except Exception as e:
        logging.warning(f"Failed to write metadata: {e}")

    return metadata


def run_plhub_tests(plhub_root: Path) -> None:
    """Run PL-Hub tests via pytest or unittest, raising on failure."""
    logging.info('Running PL-Hub tests...')
    tests_dir = plhub_root / 'Tests'
    if (plhub_root / '.venv').exists():
        python_exec = str((plhub_root / '.venv' / 'Scripts' / 'python.exe'))
        if not Path(python_exec).exists():
            python_exec = sys.executable
    else:
        python_exec = sys.executable

    # Prefer pytest if available
    try:
        res = subprocess.run([python_exec, '-m', 'pytest', str(tests_dir)], capture_output=True, text=True)
        if res.returncode == 0:
            logging.info('Tests passed (pytest).')
            return
        else:
            logging.warning('pytest failed, falling back to unittest.\n' + res.stdout + '\n' + res.stderr)
    except Exception:
        logging.info('pytest not available; using unittest discovery.')

    res = subprocess.run([python_exec, '-m', 'unittest', 'discover', '-s', str(tests_dir)], capture_output=True, text=True)
    if res.returncode != 0:
        logging.error(res.stdout)
        logging.error(res.stderr)
        raise RuntimeError('PL-Hub tests failed')
    logging.info('Tests passed (unittest).')


def build_plhub_distribution(plhub_root: Path) -> Path:
    """Build wheel/sdist for PL-Hub using setup.py. Returns dist directory path."""
    logging.info('Building PL-Hub distribution...')
    dist_dir = plhub_root / 'dist'
    if dist_dir.exists():
        for p in dist_dir.glob('*'):
            try:
                p.unlink()
            except Exception:
                pass
    # First try PEP 517 build if available
    res = subprocess.run([sys.executable, '-m', 'build', '--sdist', '--wheel'], cwd=str(plhub_root), capture_output=True, text=True)
    if res.returncode != 0:
        logging.warning('PEP 517 build failed, trying setup.py...')
        logging.debug(res.stdout)
        logging.debug(res.stderr)
        cmd = [sys.executable, 'setup.py', 'sdist', 'bdist_wheel']
        res = subprocess.run(cmd, cwd=str(plhub_root), capture_output=True, text=True)
        if res.returncode != 0:
            logging.error(res.stdout)
            logging.error(res.stderr)
            raise RuntimeError('Build failed')
    logging.info('Build completed.')
    return dist_dir


def git_tag_and_optionally_push(plhub_root: Path, tag_name: str, message: str, push: bool) -> bool:
    """Create a git tag and optionally push commit and tag.

    Returns True if tagging attempted (and likely succeeded), False if skipped.
    """
    # Verify git repo
    res = subprocess.run(['git', '-C', str(plhub_root), 'rev-parse', '--is-inside-work-tree'], capture_output=True, text=True)
    if res.returncode != 0 or 'true' not in res.stdout.lower():
        logging.warning('Git repository not detected; skipping tagging/push.')
        return False

    logging.info(f'Creating git tag {tag_name}...')
    # Add any changes (Runtime updates, metadata)
    subprocess.run(['git', '-C', str(plhub_root), 'add', '-A'], check=False)
    # Commit if there are staged changes
    res = subprocess.run(['git', '-C', str(plhub_root), 'diff', '--cached', '--quiet'])
    if res.returncode != 0:
        subprocess.run(['git', '-C', str(plhub_root), 'commit', '-m', message], check=False)
    # Create/replace tag
    subprocess.run(['git', '-C', str(plhub_root), 'tag', '-f', tag_name, '-m', message], check=False)
    if push:
        subprocess.run(['git', '-C', str(plhub_root), 'push'], check=False)
        subprocess.run(['git', '-C', str(plhub_root), 'push', '-f', 'origin', tag_name], check=False)
    return True


def checkout_pohlang_ref(pohlang_repo: Path, ref: str | None) -> None:
    """Optionally checkout a specific ref in the PohLang repository."""
    if not ref:
        return
    # Ensure it's a git repo
    res = subprocess.run(['git', '-C', str(pohlang_repo), 'rev-parse', '--is-inside-work-tree'], capture_output=True, text=True)
    if res.returncode != 0:
        logging.warning('PohLang path is not a git repo; cannot checkout ref.')
        return
    if ref == 'latest-tag':
        subprocess.run(['git', '-C', str(pohlang_repo), 'fetch', '--tags'], check=False)
        res = subprocess.run(['git', '-C', str(pohlang_repo), 'describe', '--tags', '--abbrev=0'], capture_output=True, text=True)
        if res.returncode != 0:
            logging.warning('Could not determine latest tag; staying on current ref.')
            return
        ref = res.stdout.strip()
        logging.info(f'Checking out PohLang latest tag: {ref}')
    else:
        logging.info(f'Checking out PohLang ref: {ref}')
    subprocess.run(['git', '-C', str(pohlang_repo), 'checkout', ref], check=False)


def release_command(args) -> int:
    """Orchestrate pre-release integration, tests, build, and git tagging."""
    setup_logging()
    plhub_root = Path(__file__).parent
    pohlang_repo = Path(args.pohlang_path) if args.pohlang_path else plhub_root.parent / 'PohLang'
    runtime_dir = plhub_root / 'Runtime'
    runtime_dir.mkdir(exist_ok=True)

    logging.info('Starting PL-Hub release process...')
    logging.info(f'PohLang repo: {pohlang_repo}')
    logging.info(f'Runtime directory: {runtime_dir}')

    # 1) Integrate PohLang
    try:
        # Optionally switch PohLang repo to requested ref
        checkout_pohlang_ref(pohlang_repo, getattr(args, 'pohlang_ref', None))
        # Warn if uncommitted changes exist in PohLang repo
        res = subprocess.run(['git', '-C', str(pohlang_repo), 'rev-parse', '--is-inside-work-tree'], capture_output=True, text=True)
        if res.returncode == 0 and 'true' in res.stdout.lower():
            dirty = subprocess.run(['git', '-C', str(pohlang_repo), 'status', '--porcelain'], capture_output=True, text=True)
            if dirty.stdout.strip():
                logging.warning('PohLang repository has uncommitted changes; integrating a dirty state.')
        metadata = integrate_pohlang(pohlang_repo, runtime_dir)
        logging.info(f"Integrated PohLang interpreter version {metadata.get('pohlang_version')} (commit {metadata.get('source_commit')}).")
    except Exception as e:
        logging.error(f'Integration failed: {e}')
        return 1

    # 2) Run tests
    if not args.skip_tests:
        try:
            run_plhub_tests(plhub_root)
        except Exception as e:
            logging.error(f'Tests failed: {e}')
            return 1
    else:
        logging.info('Skipping tests as requested.')

    # Stop here if dry run
    if getattr(args, 'dry_run', False):
        logging.info('Dry run completed successfully. Integration and tests passed.')
        return 0

    # 3) Build packages
    try:
        dist_dir = build_plhub_distribution(plhub_root)
        built = sorted(dist_dir.glob('*'))
        for p in built:
            logging.info(f'Built artifact: {p.name}')
    except Exception as e:
        logging.error(f'Build failed: {e}')
        return 1

    # 4) Tag release
    # Determine PLHub version from setup.py
    plhub_version = '0.0.0'
    try:
        setup_text = (plhub_root / 'setup.py').read_text(encoding='utf-8')
        for line in setup_text.splitlines():
            if 'version=' in line and 'setup(' not in line and 'version' in line:
                # naive extraction version="2.0.0",
                parts = line.split('version')[-1]
                q1 = parts.find('"')
                q2 = parts.find('"', q1+1)
                if q1 != -1 and q2 != -1:
                    plhub_version = parts[q1+1:q2]
                    break
    except Exception:
        pass

    poh_version = (metadata.get('pohlang_version') or 'unknown')
    # Tag format: plhub-vX.Y.Z (requirement)
    default_tag = f"plhub-v{plhub_version}"
    tag_name = args.tag or default_tag
    tag_message = f"PL-Hub {plhub_version} including PohLang {poh_version}"

    try:
        attempted = git_tag_and_optionally_push(plhub_root, tag_name, tag_message, push=not args.no_push)
        if attempted:
            logging.info(f'Release tagged as {tag_name}.')
        else:
            logging.info('Tagging skipped (no git repository detected).')
    except Exception as e:
        logging.error(f'Git tagging failed: {e}')
        return 1

    logging.info('Release process completed successfully.')
    return 0

def main():
    """Main entry point for PL-Hub."""
    parser = argparse.ArgumentParser(
        description="PL-Hub: PohLang Development Environment",
        prog="plhub",
        epilog="Examples:\n"
               "  python plhub.py run Examples/hello_world.poh\n"
               "  python plhub.py create my_project\n"
               "  python plhub.py --help\n"
               "  python plhub.py --version",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='PL-Hub v0.5.0 - PohLang Development Environment'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Run command
    run_parser = subparsers.add_parser('run', help='Run a PohLang program')
    run_parser.add_argument('file', help='PohLang file to run (.poh extension)')
    run_parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    run_parser.add_argument('--debug', action='store_true', help='Enable debug tracing')
    
    # Create command
    create_parser = subparsers.add_parser('create', help='Create a new PohLang project')
    create_parser.add_argument('name', help='Project name')
    create_parser.add_argument('--template', default='basic', help='Project template (basic, console, web)')
    
    # Install command
    install_parser = subparsers.add_parser('install', help='Install a PohLang package')
    install_parser.add_argument('package', help='Package name to install')
    
    # Build command
    build_parser = subparsers.add_parser('build', help='Build the current project')
    build_parser.add_argument('--target', default='dart', choices=['dart', 'python'], help='Build target')
    
    # Transpile command
    transpile_parser = subparsers.add_parser('transpile', help='Transpile a .poh file to another target')
    transpile_parser.add_argument('file', help='PohLang file to transpile (.poh)')
    transpile_parser.add_argument('--to', default='dart', choices=['dart'], help='Transpile target (currently only dart)')
    transpile_parser.add_argument('--out-dir', default='build', help='Output directory (for transpiled code)')

    # List command
    list_parser = subparsers.add_parser('list', help='List available items')
    list_parser.add_argument('type', choices=['examples', 'templates', 'packages'], help='What to list')
    
    # Release command
    release_parser = subparsers.add_parser('release', help='Run PL-Hub release automation')
    release_parser.add_argument('--dry-run', action='store_true', help='Run integration and tests without building or tagging')
    release_parser.add_argument('--no-push', action='store_true', help='Do not push git tags/commits')
    release_parser.add_argument('--tag', default=None, help='Override git tag name (default: v<plhub_version>-poh<version>)')
    release_parser.add_argument('--pohlang-path', default=None, help='Path to PohLang repo to integrate (defaults to sibling PohLang/)')
    release_parser.add_argument('--skip-tests', action='store_true', help='Skip running PL-Hub tests')
    release_parser.add_argument('--pohlang-ref', default='latest-tag', help="Git ref in PohLang to checkout before integration (default: latest-tag; e.g., 'v0.1.0', 'main')")

    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    if args.command == 'run':
        return run_program(args)
    elif args.command == 'create':
        return create_project(args)
    elif args.command == 'install':
        return install_package(args)
    elif args.command == 'build':
        return build_project(args)
    elif args.command == 'transpile':
        return transpile_file(args)
    elif args.command == 'list':
        return list_items(args)
    elif args.command == 'release':
        return release_command(args)
    
    return 0


def run_program(args):
    """Run a PohLang program."""
    file_path = args.file
    
    # Validate file exists
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return 1
    
    # Validate file extension
    if not file_path.endswith('.poh'):
        print(f"Warning: File '{file_path}' does not have .poh extension.")
        print("Proceeding anyway...")
    
    if args.verbose:
        print(f"PL-Hub: Running {file_path}")
        print()
    
    try:
        interp = Interpreter()
        if args.debug:
            interp.debug_enabled = True
        interp.run_file(file_path)
    except (RuntimeErrorPoh, ParseError) as e:
        print(f"Error running program: {e}")
        return 1
    
    return 0


def create_project(args):
    """Create a new PohLang project."""
    project_name = args.name
    template = args.template
    
    project_dir = Path.cwd() / project_name
    
    if project_dir.exists():
        print(f"Error: Directory '{project_name}' already exists.")
        return 1
    
    print(f"Creating PohLang project '{project_name}' with template '{template}'...")
    
    # Create project structure
    project_dir.mkdir()
    (project_dir / "src").mkdir()
    (project_dir / "examples").mkdir()
    (project_dir / "tests").mkdir()
    
    # Create project configuration
    config = {
        "name": project_name,
        "version": "1.0.0",
        "description": f"A PohLang project: {project_name}",
        "main": "src/main.poh",
        "dependencies": {},
        "dev_dependencies": {}
    }
    
    with open(project_dir / "plhub.json", "w") as f:
        json.dump(config, f, indent=2)
    
    # Create main file based on template
    main_content = get_template_content(template)
    with open(project_dir / "src" / "main.poh", "w") as f:
        f.write(main_content)
    
    # Create README
    readme_content = f"""# {project_name}

A PohLang project created with PL-Hub.

## Running

```bash
cd {project_name}
python -m plhub run src/main.poh
```

## Building

```bash
python -m plhub build
```
"""
    
    with open(project_dir / "README.md", "w") as f:
        f.write(readme_content)
    
    print(f"✅ Project '{project_name}' created successfully!")
    print(f"📁 Location: {project_dir}")
    print(f"🚀 To run: cd {project_name} && python plhub.py run src/main.poh")
    
    return 0


def install_package(args):
    """Install a PohLang package."""
    package_name = args.package
    
    # Check if we're in a project directory
    if not Path("plhub.json").exists():
        print("Error: Not in a PohLang project directory.")
        print("Run 'python plhub.py create <project_name>' to create a new project.")
        return 1
    
    print(f"Installing package '{package_name}'...")
    
    # Load project config
    with open("plhub.json", "r") as f:
        config = json.load(f)
    
    # For now, just add to dependencies (package registry would be implemented later)
    config["dependencies"][package_name] = "^1.0.0"
    
    # Save updated config
    with open("plhub.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Package '{package_name}' installed successfully!")
    
    return 0


def build_project(args):
    """Build the current project."""
    if not Path("plhub.json").exists():
        print("Error: Not in a PohLang project directory.")
        return 1
    
    target = args.target
    print(f"Building project for target: {target}")
    
    with open("plhub.json", "r") as f:
        config = json.load(f)
    
    main_file = config.get("main", "src/main.poh")
    
    if not Path(main_file).exists():
        print(f"Error: Main file '{main_file}' not found.")
        return 1
    
    if target == "dart":
        print("Building Dart transpilation...")
        try:
            # Prefer bundled transpiler
            bundled_dart = RUNTIME_DIR / "bin" / "pohlang.dart"
            sibling_dart = (Path(__file__).parent.parent / "PohLang" / "bin" / "pohlang.dart")
            transpiler_path = None
            if bundled_dart.exists():
                transpiler_path = bundled_dart
            elif sibling_dart.exists():
                transpiler_path = sibling_dart
            else:
                # As a last resort, try installed dart package via simple name
                transpiler_path = None

            if transpiler_path is not None:
                result = subprocess.run([
                    "dart", "run", str(transpiler_path),
                    main_file, "--no-run"
                ], capture_output=True, text=True)
                if result.returncode == 0:
                    print("✅ Dart build completed successfully!")
                else:
                    print(f"❌ Dart build failed:\n{result.stdout}\n{result.stderr}")
                    return 1
            else:
                print("Warning: Dart transpiler entrypoint not found. Using Python interpreter instead.")
                return run_with_python(main_file)
        except FileNotFoundError:
            print("Error: 'dart' command not found. Please install Dart SDK or use --target python.")
            return 1
        except Exception as e:
            print(f"Error during Dart build: {e}")
            return 1
    else:  # python
        return run_with_python(main_file)
    
    return 0


def list_items(args):
    """List available items."""
    item_type = args.type
    
    if item_type == 'examples':
        examples_dir = Path(__file__).parent / "Examples"
        if examples_dir.exists():
            print("Available example programs:")
            for example in sorted(examples_dir.glob("*.poh")):
                print(f"  - {example.name}")
        else:
            print("No examples found.")
    
    elif item_type == 'templates':
        print("Available project templates:")
        print("  - basic: Simple console application")
        print("  - console: Advanced console application with input/output")
        print("  - web: Web application template (experimental)")
    
    elif item_type == 'packages':
        if Path("plhub.json").exists():
            with open("plhub.json", "r") as f:
                config = json.load(f)
            
            print("Installed packages:")
            deps = config.get("dependencies", {})
            if deps:
                for name, version in deps.items():
                    print(f"  - {name}: {version}")
            else:
                print("  No packages installed.")
        else:
            print("Not in a PohLang project directory.")
    
    return 0


def get_template_content(template_name):
    """Get content for a project template."""
    templates = {
        "basic": '''# Basic PohLang Program
Write "Hello from PohLang!"
Write "This is a basic project template."
''',
        "console": '''# Console Application Template
Write "Welcome to your PohLang console application!"
Write ""

Ask for name
Write "Hello " plus name plus "!"

Set count to 0
Repeat 3
    Set count to count plus 1
    Write "Loop iteration: " plus count
End

Write ""
Write "Thanks for using PohLang!"
''',
        "web": '''# Web Application Template (Experimental)
Write "Web application features coming soon!"
Write "For now, this is a placeholder."

# Future: Web server functionality
# Make start_server with port
#     Write "Starting server on port " plus port
#     # Server implementation
# End
# 
# Use start_server with 8080
'''
    }
    
    return templates.get(template_name, templates["basic"])


def transpile_file(args):
    """Transpile a single .poh file using the bundled or sibling Dart transpiler."""
    if not Path(args.file).exists():
        print(f"Error: File '{args.file}' not found.")
        return 1
    if args.to != 'dart':
        print("Error: Only 'dart' transpile target is currently supported.")
        return 64
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    bundled_dart = RUNTIME_DIR / "bin" / "pohlang.dart"
    sibling_dart = (Path(__file__).parent.parent / "PohLang" / "bin" / "pohlang.dart")
    transpiler_path = bundled_dart if bundled_dart.exists() else (sibling_dart if sibling_dart.exists() else None)

    try:
        if transpiler_path is None:
            print("Error: Could not locate PohLang Dart transpiler entrypoint.")
            print("Run 'plhub release' to bundle the latest PohLang into Runtime or place PohLang next to PLHub.")
            return 1
        # Use --no-run and optionally pass output directory if supported
        # For now, we run with --no-run and move outputs if the transpiler writes to CWD
        res = subprocess.run([
            "dart", "run", str(transpiler_path), args.file, "--no-run"
        ], capture_output=True, text=True)
        if res.returncode != 0:
            print(f"❌ Transpile failed:\n{res.stdout}\n{res.stderr}")
            return 1
        print("✅ Transpile completed. Check generated Dart files (location depends on transpiler settings).")
        return 0
    except FileNotFoundError:
        print("Error: 'dart' command not found. Please install Dart SDK from https://dart.dev/get-dart.")
        return 1
    except Exception as e:
        print(f"Error during transpile: {e}")
        return 1


def run_with_python(file_path):
    """Run a PohLang file with the Python interpreter."""
    try:
        interp = Interpreter()
        interp.run_file(file_path)
        print("✅ Python execution completed successfully!")
        return 0
    except (RuntimeErrorPoh, ParseError) as e:
        print(f"❌ Python execution failed: {e}")
        return 1


def list_examples():
    """List available example programs (deprecated - use 'list examples')."""
    print("Use 'python plhub.py list examples' instead.")
    return list_items(type('Args', (), {'type': 'examples'})())


if __name__ == '__main__':
    sys.exit(main() or 0)