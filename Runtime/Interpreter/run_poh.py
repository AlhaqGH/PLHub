from __future__ import annotations
import sys
from .poh_interpreter import Interpreter, RuntimeErrorPoh
from .poh_parser import ParseError


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m Interpreter.run_poh <file.poh>")
        sys.exit(64)
    path = sys.argv[1]
    interp = Interpreter()
    try:
        interp.run_file(path)
    except (RuntimeErrorPoh, ParseError) as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
