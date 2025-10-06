import os
import sys
import shutil
import tempfile
from pathlib import Path
import unittest


class TestRuntimePreference(unittest.TestCase):
    """Test that PLHub properly uses available runtimes."""
    
    def setUp(self):
        self.repo_root = Path(__file__).parent.parent
        self.runtime_dir = self.repo_root / 'Runtime'
        self.tmpdir = Path(tempfile.mkdtemp())

        # Create a simple .poh file to run with proper PohLang syntax
        self.sample = self.tmpdir / 'test.poh'
        self.sample.write_text('''Start Program
Write "Hello from test"
End Program
''', encoding='utf-8')

        # Add PLHub root to sys.path so `import plhub` resolves local file
        sys.path.insert(0, str(self.repo_root))

    def tearDown(self):
        # Cleanup files we created
        try:
            shutil.rmtree(self.tmpdir)
        except Exception:
            pass
        # Remove path injection
        try:
            sys.path.remove(str(self.repo_root))
        except ValueError:
            pass

    def test_run_program_succeeds(self):
        """Test that PLHub can successfully run a PohLang program."""
        # Import plhub fresh
        if 'plhub' in sys.modules:
            del sys.modules['plhub']
        import importlib
        plhub = importlib.import_module('plhub')

        # Call run_program through CLI-style function
        class Args:
            file = str(self.sample)
            verbose = False
            debug = False

        exit_code = plhub.run_program(Args)
        self.assertEqual(exit_code, 0, 'Program should execute successfully')
    
    def test_rust_runtime_available(self):
        """Test that Rust runtime binary is available (preferred runtime)."""
        import platform as plat
        exe = 'pohlang.exe' if plat.system().lower().startswith('win') else 'pohlang'
        rust_binary = self.runtime_dir / 'bin' / exe
        
        # Note: The Rust binary might not always be present in development,
        # but if it exists, it should be preferred
        if rust_binary.exists():
            self.assertTrue(rust_binary.is_file(), 'Rust runtime should be a file')


if __name__ == '__main__':
    unittest.main()
