import os
import sys
import shutil
import tempfile
from pathlib import Path
import unittest


class TestRuntimeInterpreterPreference(unittest.TestCase):
    def setUp(self):
        self.repo_root = Path(__file__).parent.parent
        self.runtime_dir = self.repo_root / 'Runtime'
        self.interpreter_dir = self.runtime_dir / 'Interpreter'
        self.tmpdir = Path(tempfile.mkdtemp())
        # Ensure a clean runtime interpreter stub
        if self.interpreter_dir.exists():
            shutil.rmtree(self.interpreter_dir)
        self.interpreter_dir.mkdir(parents=True)

        # Write a minimal stub Interpreter with a marker side-effect
        (self.interpreter_dir / '__init__.py').write_text('', encoding='utf-8')
        marker = self.runtime_dir / 'USED_RUNTIME_INTERPRETER'
        code = f"""
class RuntimeErrorPoh(Exception):
    pass

class ParseError(Exception):
    pass

class Interpreter:
    def __init__(self):
        pass
    def run_file(self, file_path):
        # Touch the marker file so the test can verify this interpreter ran
        open(r"{marker}", 'w').write('used')
        return 0
"""
        (self.interpreter_dir / 'poh_interpreter.py').write_text(code, encoding='utf-8')
        (self.interpreter_dir / 'poh_parser.py').write_text('class ParseError(Exception):\n    pass\n', encoding='utf-8')

        # Create a simple .poh file to run
        self.sample = self.tmpdir / 'test.poh'
        self.sample.write_text('Write "Hello"\n', encoding='utf-8')

        # Add PLHub root to sys.path so `import plhub` resolves local file
        sys.path.insert(0, str(self.repo_root))

    def tearDown(self):
        # Cleanup files we created
        try:
            if self.interpreter_dir.exists():
                shutil.rmtree(self.interpreter_dir)
        except Exception:
            pass
        try:
            shutil.rmtree(self.tmpdir)
        except Exception:
            pass
        marker = self.runtime_dir / 'USED_RUNTIME_INTERPRETER'
        try:
            if marker.exists():
                marker.unlink()
        except Exception:
            pass
        # Remove path injection
        try:
            sys.path.remove(str(self.repo_root))
        except ValueError:
            pass

    def test_runtime_interpreter_is_preferred(self):
        # Import plhub fresh
        if 'plhub' in sys.modules:
            del sys.modules['plhub']
        import importlib
        plhub = importlib.import_module('plhub')

        # Call run_with_python through CLI-style function
        class Args:
            file = str(self.sample)
            verbose = False
            debug = False

        exit_code = plhub.run_program(Args)
        self.assertEqual(exit_code, 0)
        marker = self.runtime_dir / 'USED_RUNTIME_INTERPRETER'
        self.assertTrue(marker.exists(), 'Runtime Interpreter should have been used (marker created).')


if __name__ == '__main__':
    unittest.main()
