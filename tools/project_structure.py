"""
Project Structure Automation

Automates the creation of well-structured PohLang projects with sensible defaults,
best practices, and optional components.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field


@dataclass
class ProjectStructure:
    """Defines a complete project structure"""
    name: str
    description: str
    directories: List[str] = field(default_factory=list)
    files: Dict[str, str] = field(default_factory=dict)  # path -> content
    config: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def create_basic(cls, name: str) -> 'ProjectStructure':
        """Create a basic project structure"""
        return cls(
            name=name,
            description=f"A basic PohLang project: {name}",
            directories=[
                'src',
                'tests',
                'docs',
                'examples',
            ],
            files={
                'src/main.poh': cls._basic_main(),
                'tests/test_main.poh': cls._basic_test(),
                'examples/example.poh': cls._basic_example(),
                'README.md': cls._basic_readme(name),
                '.gitignore': cls._gitignore(),
            },
            config={
                'version': '1.0.0',
                'main': 'src/main.poh',
                'dependencies': {},
                'dev_dependencies': {},
            }
        )
    
    @classmethod
    def create_console_app(cls, name: str) -> 'ProjectStructure':
        """Create a console application structure"""
        return cls(
            name=name,
            description=f"A console application: {name}",
            directories=[
                'src',
                'src/commands',
                'src/utils',
                'tests',
                'tests/unit',
                'tests/integration',
                'docs',
                'examples',
            ],
            files={
                'src/main.poh': cls._console_main(),
                'src/commands/menu.poh': cls._console_menu(),
                'src/utils/input.poh': cls._console_utils(),
                'tests/test_main.poh': cls._console_test(),
                'examples/usage.poh': cls._console_example(),
                'README.md': cls._console_readme(name),
                'USAGE.md': cls._usage_guide(),
                '.gitignore': cls._gitignore(),
            },
            config={
                'version': '1.0.0',
                'main': 'src/main.poh',
                'type': 'console',
                'dependencies': {},
                'dev_dependencies': {},
            }
        )
    
    @classmethod
    def create_web_app(cls, name: str) -> 'ProjectStructure':
        """Create a web application structure"""
        return cls(
            name=name,
            description=f"A web application: {name}",
            directories=[
                'src',
                'src/routes',
                'src/controllers',
                'src/models',
                'public',
                'public/css',
                'public/js',
                'views',
                'tests',
                'docs',
            ],
            files={
                'src/main.poh': cls._web_main(),
                'src/routes/index.poh': cls._web_routes(),
                'README.md': cls._web_readme(name),
                'public/index.html': cls._web_index_html(),
                '.gitignore': cls._gitignore(),
            },
            config={
                'version': '1.0.0',
                'main': 'src/main.poh',
                'type': 'web',
                'dependencies': {},
                'dev_dependencies': {},
            }
        )
    
    @classmethod
    def create_library(cls, name: str) -> 'ProjectStructure':
        """Create a library/package structure"""
        return cls(
            name=name,
            description=f"A reusable PohLang library: {name}",
            directories=[
                'src',
                'src/core',
                'src/utils',
                'tests',
                'tests/unit',
                'examples',
                'docs',
                'docs/api',
            ],
            files={
                'src/lib.poh': cls._library_main(name),
                'src/core/functions.poh': cls._library_functions(),
                'tests/test_lib.poh': cls._library_test(),
                'examples/basic_usage.poh': cls._library_example(name),
                'README.md': cls._library_readme(name),
                'LICENSE': cls._mit_license(),
                'CHANGELOG.md': cls._changelog(),
                '.gitignore': cls._gitignore(),
            },
            config={
                'version': '0.1.0',
                'main': 'src/lib.poh',
                'type': 'library',
                'exports': ['src/lib.poh', 'src/core/functions.poh'],
                'dependencies': {},
                'dev_dependencies': {},
            }
        )
    
    # Template content generators
    
    @staticmethod
    def _basic_main() -> str:
        return """Start Program

# Main Application Entry Point
# This is where your PohLang application starts

Write "Welcome to PohLang!"
Write ""

Set name to "World"
Write "Hello, " plus name plus "!"

Write ""
Write "Edit this file to build your application."

End Program
"""
    
    @staticmethod
    def _basic_test() -> str:
        return """Start Program

# Test: Main Application
# Verifies basic application functionality

Write "Running tests..."
Write ""

# Test 1: String concatenation
Set greeting to "Hello"
Set name to "PohLang"
Set result to greeting plus " " plus name

If result is equal to "Hello PohLang"
    Write "✅ Test 1 passed: String concatenation"
Otherwise
    Write "❌ Test 1 failed"
End If

# Test 2: Arithmetic
Set x to 10
Set y to 20
Set sum to x plus y

If sum is equal to 30
    Write "✅ Test 2 passed: Arithmetic"
Otherwise
    Write "❌ Test 2 failed"
End If

Write ""
Write "Tests completed!"

End Program
"""
    
    @staticmethod
    def _basic_example() -> str:
        return """Start Program

# Example: PohLang v0.5.0 Features
# Demonstrates Phase 1 phrasal expressions

Write "==================================="
Write "  PohLang v0.5.0 Examples"
Write "==================================="
Write ""

# Variables
Write "1. Variables:"
Set message to "Hello from PohLang"
Write "   " plus message
Write ""

# Arithmetic with phrasal expressions
Write "2. Arithmetic & Phrasal Expressions:"
Set numbers to [10, 20, 5, 15]
Set sum to total of numbers
Set min to smallest in numbers
Set max to largest in numbers
Write "   Numbers: [10, 20, 5, 15]"
Write "   Total: " plus sum
Write "   Smallest: " plus min
Write "   Largest: " plus max
Write ""

# String operations
Write "3. String Operations:"
Set greeting to "hello world"
Set upper to make uppercase greeting
Set clean to trim spaces from "  spaced  "
Write "   Original: " plus greeting
Write "   Uppercase: " plus upper
Write "   Trimmed: [" plus clean plus "]"
Write ""

# Collection operations
Write "4. Collections:"
Set fruits to ["apple", "banana", "orange"]
Set count to count of fruits
Set first to first in fruits
Set last to last in fruits
Write "   Fruits: " plus join fruits with ", "
Write "   Count: " plus count
Write "   First: " plus first plus ", Last: " plus last
Write ""

# Conditionals
Write "5. Conditionals:"
Set temperature to 25
If temperature is greater than 20
    Write "   It's warm outside!"
Otherwise
    Write "   It's cool outside."
End If

End Program
"""
    
    @staticmethod
    def _basic_readme(name: str) -> str:
        return f"""# {name}

A PohLang project created with PL-Hub v0.5.0.

## Description

Add your project description here.

## Getting Started

### Prerequisites

- PL-Hub (PohLang Development Environment)
- PohLang Runtime

### Installation

```bash
git clone <your-repo>
cd {name}
```

### Running

```bash
python plhub.py run src/main.poh
```

### Development

```bash
# Watch mode with hot reload
python plhub.py dev

# Run tests
python plhub.py test

# Watch tests
python plhub.py test --watch
```

### Building

```bash
python plhub.py build
```

## Project Structure

```
{name}/
├── src/           # Source code
├── tests/         # Test files
├── examples/      # Example files
├── docs/          # Documentation
└── plhub.json     # Project configuration
```

## License

MIT License - See LICENSE file for details.

## Contributing

Contributions welcome! Please read CONTRIBUTING.md first.
"""
    
    @staticmethod
    def _console_main() -> str:
        return """Start Program

# Console Application
# Interactive command-line interface

Write "==================================="
Write "  Console Application"
Write "==================================="
Write ""

Set running to 1

While running is equal to 1
    Write ""
    Write "Main Menu:"
    Write "  1. Option One"
    Write "  2. Option Two"
    Write "  3. Help"
    Write "  4. Exit"
    Write ""
    
    Ask for "Enter your choice (1-4): " and store in choice
    
    If choice is equal to "1"
        Write "You selected Option One"
    Otherwise
        If choice is equal to "2"
            Write "You selected Option Two"
        Otherwise
            If choice is equal to "3"
                Write "Help: Choose an option from the menu"
            Otherwise
                If choice is equal to "4"
                    Write "Goodbye!"
                    Set running to 0
                Otherwise
                    Write "Invalid choice. Please try again."
                End
            End
        End
    End
End

End Program
"""
    
    @staticmethod
    def _console_menu() -> str:
        return """Start Program

# Menu System
# Reusable menu display and handling

# This file can be imported by other files
# Add menu functions here

Write "Menu module loaded"

End Program
"""
    
    @staticmethod
    def _console_utils() -> str:
        return """Start Program

# Input Utilities
# Helper functions for user input handling

# This file can be imported by other files
# Add utility functions here

Write "Input utilities module loaded"

End Program
"""
    
    @staticmethod
    def _console_test() -> str:
        return """Start Program

# Test: Console Application
# Tests for console app functionality

Write "Running console app tests..."
Write ""

# Test menu options
Set test_passed to 0
Set total_tests to 2

# Test 1: Menu choice validation
Set choice to "1"
If choice is equal to "1"
    Write "✅ Test 1 passed: Menu choice validation"
    Increase test_passed by 1
Otherwise
    Write "❌ Test 1 failed"
End

# Test 2: Exit condition
Set running to 0
If running is equal to 0
    Write "✅ Test 2 passed: Exit condition"
    Increase test_passed by 1
Otherwise
    Write "❌ Test 2 failed"
End

Write ""
Write "Tests completed: " plus test_passed plus "/" plus total_tests plus " passed"

End Program
"""
    
    @staticmethod
    def _console_example() -> str:
        return """Start Program

# Example: Console Application with Phrasal Expressions
# Demonstrates PohLang v0.5.0 features

Write "Console Application Example - PohLang v0.5.0"
Write ""

# Menu options with collections
Set menu_items to ["Start", "Settings", "Help", "Exit"]
Set menu_count to count of menu_items
Set first_option to first in menu_items
Set last_option to last in menu_items

Write "Menu has " plus menu_count plus " options"
Write "First: " plus first_option plus ", Last: " plus last_option
Write ""

# Process a sample list
Set tasks to ["Read", "Write", "Test"]
Set task_list to join tasks with " → "
Write "Task flow: " plus task_list
Write ""

# String operations
Set username to "  admin  "
Set clean_name to trim spaces from username
Set upper_name to make uppercase clean_name
Write "Cleaned username: [" plus clean_name plus "]"
Write "Display name: " plus upper_name
Write ""

# Number processing
Set scores to [85, 92, 78, 95]
Set total to total of scores
Set highest to largest in scores
Set lowest to smallest in scores
Write "Scores: " plus join scores with ", "
Write "Total: " plus total plus ", High: " plus highest plus ", Low: " plus lowest
Write ""

Write "Example completed!"

End Program
"""
    
    @staticmethod
    def _console_readme(name: str) -> str:
        return f"""# {name}

A console application built with PohLang.

## Features

- Interactive menu system
- User input handling
- Command processing
- Help system

## Usage

```bash
python plhub.py run src/main.poh
```

Follow the on-screen menu to interact with the application.

## Commands

The application provides the following menu options:

1. **Option One** - Description of option one
2. **Option Two** - Description of option two
3. **Help** - Display help information
4. **Exit** - Close the application

## Development

```bash
# Hot reload during development
python plhub.py dev

# Run tests
python plhub.py test
```

## Project Structure

```
{name}/
├── src/
│   ├── main.poh           # Main entry point
│   ├── commands/
│   │   └── menu.poh       # Menu system
│   └── utils/
│       └── input.poh      # Input utilities
├── tests/                 # Test files
└── examples/              # Usage examples
```
"""
    
    @staticmethod
    def _usage_guide() -> str:
        return """# Usage Guide

## Getting Started

This console application provides an interactive menu-driven interface.

### Running the Application

```bash
python plhub.py run src/main.poh
```

### Menu Navigation

1. Start the application
2. Read the menu options
3. Enter your choice (1-4)
4. Follow the prompts

### Commands

- **Option One**: [Describe what this does]
- **Option Two**: [Describe what this does]
- **Help**: Display help information
- **Exit**: Close the application

## Tips

- Enter the number corresponding to your choice
- Use the Help option if you need assistance
- Press Ctrl+C to force quit if needed

## Troubleshooting

**Problem**: Invalid choice message  
**Solution**: Make sure you enter a number between 1-4

**Problem**: Application won't start  
**Solution**: Check that PohLang runtime is installed

## Advanced Usage

### Customization

Edit `src/main.poh` to add new menu options or modify behavior.

### Testing

Run tests with:
```bash
python plhub.py test
```
"""
    
    @staticmethod
    def _web_main() -> str:
        return """Start Program

# Web Application (Placeholder)
# Full web support coming soon

Write "Web Application Server"
Write ""
Write "Note: Full web server functionality is planned for a future release."
Write "For now, this serves as a template for web application structure."

End Program
"""
    
    @staticmethod
    def _web_routes() -> str:
        return """Start Program

# Web Routes (Placeholder)
# Define application routes here

Write "Routes module loaded"

End Program
"""
    
    @staticmethod
    def _web_readme(name: str) -> str:
        return f"""# {name}

A web application built with PohLang.

**Note**: Full web server functionality is planned for a future PohLang release.
This template provides the structure for web application development.

## Structure

```
{name}/
├── src/
│   ├── main.poh           # Application entry
│   ├── routes/            # Route definitions
│   ├── controllers/       # Request handlers
│   └── models/            # Data models
├── public/                # Static assets
├── views/                 # Templates
└── tests/                 # Test files
```

## Future Features

- HTTP server
- Routing system
- Template engine
- Session management
- Database integration
"""
    
    @staticmethod
    def _web_index_html() -> str:
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PohLang Web App</title>
</head>
<body>
    <h1>PohLang Web Application</h1>
    <p>Welcome to your PohLang web application!</p>
</body>
</html>
"""
    
    @staticmethod
    def _library_main(name: str) -> str:
        return f"""Start Program

# {name} Library
# Main library entry point

Write "{name} library loaded"
Write "Version: 0.1.0"

# Export library functions here
# Other files can import this library

End Program
"""
    
    @staticmethod
    def _library_functions() -> str:
        return """Start Program

# Core Functions
# Reusable functions for the library

# Example function (natural language style)
# Add your functions here

Write "Core functions module loaded"

End Program
"""
    
    @staticmethod
    def _library_test() -> str:
        return """Start Program

# Test: Library Functions
# Unit tests for library functionality

Write "Running library tests..."
Write ""

Set tests_passed to 0
Set total_tests to 1

# Test 1: Library loads
Write "✅ Test 1 passed: Library loads successfully"
Increase tests_passed by 1

Write ""
Write "Tests completed: " plus tests_passed plus "/" plus total_tests plus " passed"

End Program
"""
    
    @staticmethod
    def _library_example(name: str) -> str:
        return f"""Start Program

# Example: Using {name} Library with PohLang v0.5.0
# Demonstrates library usage with phrasal expressions

Write "Example: {name} Library Usage"
Write ""

# Show phrasal expression patterns for library functions
Write "Recommended patterns for library functions:"
Write ""

Write "1. Collection Processing:"
Set data to [1, 2, 3, 4, 5]
Set sum to total of data
Set size to count of data
Write "   Process collections: total of <list>, count of <list>"
Write "   Example: " plus sum plus " (total), " plus size plus " (count)"
Write ""

Write "2. String Manipulation:"
Set text to "  sample text  "
Set clean to trim spaces from text
Set upper to make uppercase clean
Write "   Clean strings: trim spaces from <text>"
Write "   Transform: make uppercase/lowercase <text>"
Write "   Example: [" plus clean plus "] → " plus upper
Write ""

Write "3. Collection Operations:"
Set items to ["first", "second", "third"]
Set first_item to first in items
Set last_item to last in items
Set reversed to reverse of items
Write "   Access: first in <list>, last in <list>"
Write "   Transform: reverse of <list>"
Write "   Example: " plus first_item plus " ... " plus last_item
Write ""

Write "4. List Building:"
Set numbers to [10, 20, 30]
Set joined to join numbers with " + "
Write "   Join items: join <list> with <separator>"
Write "   Example: " plus joined
Write ""

Write "Import this library in your project:"
Write "  Import \\"src/lib.poh\\""

End Program
"""
    
    @staticmethod
    def _library_readme(name: str) -> str:
        return f"""# {name}

A reusable PohLang library.

## Installation

Add to your project:
```bash
# Copy to your project's dependencies
cp -r {name} your_project/lib/
```

## Usage

Import the library in your PohLang code:

```poh
Import "lib/{name}/src/lib.poh"
```

## API Documentation

### Functions

[Document your library functions here]

## Examples

See `examples/` directory for usage examples.

## Development

```bash
# Run tests
python plhub.py test

# Watch tests during development
python plhub.py test --watch
```

## Version

Current version: 0.1.0

See CHANGELOG.md for version history.

## License

MIT License - see LICENSE file
"""
    
    @staticmethod
    def _mit_license() -> str:
        return """MIT License

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
    
    @staticmethod
    def _changelog() -> str:
        return """# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-10-05

### Added
- Initial release
- Core library functionality
- Basic API
- Documentation
- Examples

### Changed
- N/A

### Deprecated
- N/A

### Removed
- N/A

### Fixed
- N/A

### Security
- N/A
"""
    
    @staticmethod
    def _gitignore() -> str:
        return """# PohLang / PLHub
*.pbc
*.pyc
__pycache__/
.plhub/
build/
dist/

# IDE
.vscode/settings.json
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Dependencies
plhub_modules/
node_modules/

# Logs
*.log
logs/

# Environment
.env
.env.local

# Testing
test-results/
coverage/
.pytest_cache/
"""


class ProjectStructureGenerator:
    """Generates complete project structures"""
    
    @staticmethod
    def generate(project_dir: Path, structure: ProjectStructure, plhub_root: Path):
        """Generate the complete project structure"""
        # Create project directory
        project_dir.mkdir(exist_ok=True)
        
        # Create all directories
        for directory in structure.directories:
            (project_dir / directory).mkdir(parents=True, exist_ok=True)
        
        # Create all files
        for file_path, content in structure.files.items():
            full_path = project_dir / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content, encoding='utf-8')
        
        # Create plhub.json
        config = {
            'name': structure.name,
            'description': structure.description,
            **structure.config
        }
        
        config_file = project_dir / 'plhub.json'
        config_file.write_text(json.dumps(config, indent=2), encoding='utf-8')
        
        return config
