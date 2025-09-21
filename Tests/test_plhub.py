"""
PL-Hub Test Suite

Tests for the PohLang development environment functionality.
"""

import unittest
import sys
import os
import tempfile
import shutil
from pathlib import Path
import json

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import plhub
except ImportError:
    # If plhub module is not available, we'll test what we can
    plhub = None


class TestPLHubEnvironment(unittest.TestCase):
    """Test cases for the PLHub environment setup."""
    
    def setUp(self):
        """Set up test environment."""
        self.project_root = Path(__file__).parent.parent
        self.test_dir = Path(tempfile.mkdtemp())
        
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_plhub_structure(self):
        """Test that PLHub has proper structure as development environment."""
        required_dirs = [
            "CLI",
            "Editor", 
            "Examples",
            "Modules",
            "Tests",
            "docs",
            "templates",
            "tools",
            "packages",
            "plugins"
        ]
        
        for dir_name in required_dirs:
            dir_path = self.project_root / dir_name
            self.assertTrue(dir_path.exists(), f"{dir_name}/ directory should exist in PLHub")
    
    def test_required_files_exist(self):
        """Test that documented files exist."""
        required_files = [
            "README.md",
            "plhub.py", 
            "setup.py"
        ]
        
        for file_name in required_files:
            file_path = self.project_root / file_name
            self.assertTrue(file_path.exists(), f"{file_name} should exist")
    
    def test_no_duplicate_interpreter(self):
        """Test that PLHub doesn't contain duplicate interpreter (should be in PohLang)."""
        interpreter_dir = self.project_root / "Interpreter"
        self.assertFalse(interpreter_dir.exists(), "PLHub should not contain Interpreter/ (belongs in PohLang)")
    
    def test_no_duplicate_transpiler(self):
        """Test that PLHub doesn't contain duplicate transpiler (should be in PohLang).""" 
        transpiler_dir = self.project_root / "Transpiler"
        self.assertFalse(transpiler_dir.exists(), "PLHub should not contain Transpiler/ (belongs in PohLang)")


class TestTemplates(unittest.TestCase):
    """Test template functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.project_root = Path(__file__).parent.parent
        
    def test_templates_directory_exists(self):
        """Test that templates directory exists."""
        templates_dir = self.project_root / "templates"
        self.assertTrue(templates_dir.exists(), "templates/ directory should exist")
        
    def test_template_files_exist(self):
        """Test that template files exist."""
        templates_dir = self.project_root / "templates"
        expected_templates = ["basic.poh", "console.poh", "web.poh"]
        
        for template in expected_templates:
            template_path = templates_dir / template
            self.assertTrue(template_path.exists(), f"Template {template} should exist")


class TestExamples(unittest.TestCase):
    """Test that example programs are available."""
    
    def setUp(self):
        """Set up test environment."""
        self.examples_dir = Path(__file__).parent.parent / "Examples"
        
    def test_examples_directory_exists(self):
        """Test that Examples directory exists."""
        self.assertTrue(self.examples_dir.exists(), "Examples directory should exist")


class TestPLHubFunctionality(unittest.TestCase):
    """Test PLHub functionality if available."""
    
    @unittest.skipIf(plhub is None, "plhub module not available")
    def test_template_content_basic(self):
        """Test that basic template content is returned."""
        content = plhub.get_template_content("basic")
        self.assertIn("PohLang", content)
        self.assertIn("Write", content)
        
    @unittest.skipIf(plhub is None, "plhub module not available")  
    def test_template_content_fallback(self):
        """Test that unknown templates fall back to basic."""
        content = plhub.get_template_content("unknown_template")
        basic_content = plhub.get_template_content("basic")
        self.assertEqual(content, basic_content)


if __name__ == '__main__':
    unittest.main()