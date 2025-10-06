"""PohLang Python interpreter CLI for PLHub.

This is a compatibility wrapper that uses PohLang from its proper location.

Usage:
	# Preferred (matches README)
	python -m CLI.cli run Examples/hello_world.poh

	# Back-compat shorthand
	python -m CLI.cli Examples/hello_world.poh

This command executes a .poh script using the Python reference interpreter.
"""

from __future__ import annotations
import sys
import argparse
from pathlib import Path

# Determine PohLang installation path
POHLANG_PATH = Path(__file__).parent.parent.parent / "PohLang"
if not POHLANG_PATH.exists():
    print("Error: PohLang installation not found.")
    print("Please ensure PohLang is installed or PLHub is in the same directory as PohLang.")
    sys.exit(1)

# Add PohLang to Python path for imports
sys.path.insert(0, str(POHLANG_PATH))

try:
    from Interpreter.poh_interpreter import Interpreter, RuntimeErrorPoh
except ImportError as e:
    print(f"Error: Could not import PohLang interpreter: {e}")
    print(f"PohLang path: {POHLANG_PATH}")
    sys.exit(1)


def main():
	# Pre-scan argv to support shorthand: `python -m CLI.cli <script.poh> [--debug]`
	original_argv = sys.argv[1:]
	script_candidates = [a for a in original_argv if not a.startswith('-')]
	argv = original_argv
	if 'run' not in original_argv and len(script_candidates) == 1 and script_candidates[0].lower().endswith('.poh'):
		# Rewrite argv to use the 'run' subcommand
		script_arg = script_candidates[0]
		argv = ['run', script_arg] + [a for a in original_argv if a is not script_arg]

	parser = argparse.ArgumentParser(description="PohLang Python reference interpreter")
	# Global flags
	parser.add_argument('--debug', action='store_true', help='Enable debug tracing')
	# Subcommands
	subparsers = parser.add_subparsers(dest='command')
	run_parser = subparsers.add_parser('run', help='Run a .poh script')
	run_parser.add_argument('script', help='Path to .poh script')
	args = parser.parse_args(argv)

	# Determine target script
	path = None
	if args.command == 'run':
		path = args.script
	else:
		parser.print_help()
		return 2

	interp = Interpreter()
	interp.debug_enabled = args.debug
	try:
		interp.run_file(path)
	except (RuntimeErrorPoh, Exception) as e:  # noqa: BLE001
		print(f"Runtime error: {e}")
		if args.debug:
			import traceback
			traceback.print_exc()
		sys.exit(70)


if __name__ == '__main__':  # pragma: no cover
	main()

