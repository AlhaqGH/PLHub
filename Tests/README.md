# PL-Hub Tests

This directory contains automated tests for the PL-Hub development environment.

## Test Files

- `test_plhub.py` - Main test suite for PL-Hub functionality
- `test_cli.py` - CLI-specific tests (future)
- `test_examples.py` - Tests that verify examples work (future)
- `test_integration.py` - Integration tests (future)

## Running Tests

Run all tests:
```bash
python -m unittest Tests.test_plhub
```

Run specific test:
```bash
python -m unittest Tests.test_plhub.TestCLI.test_version_command
```

Run tests with verbose output:
```bash
python -m unittest -v Tests.test_plhub
```

## Test Coverage

Tests should cover:
- CLI functionality
- Example program execution
- Project structure validation
- Integration between components
- Error handling

## Contributing Tests

When adding new features:
1. Add corresponding test cases
2. Ensure tests pass before committing
3. Include both positive and negative test cases
4. Test edge cases and error conditions