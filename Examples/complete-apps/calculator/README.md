# Advanced Calculator

A complete, production-ready console calculator application built with PohLang.

## Features

✅ **Basic Operations**
- Addition
- Subtraction
- Multiplication
- Division (with zero-check)

✅ **Advanced Operations**
- Power (x^y)
- Square Root
- Percentage calculations
- Average of multiple numbers

✅ **User Experience**
- Interactive menu system
- Calculation history
- Error handling
- Clear formatting

✅ **Quality Assurance**
- Comprehensive test suite (10 tests)
- Edge case handling
- Input validation

## Installation

```bash
cd Examples/complete-apps/calculator
```

## Usage

### Run the Application

```bash
python plhub.py run src/main.poh
```

### Run Tests

```bash
python plhub.py run tests/test_basic.poh
```

### Build

```bash
# Build to bytecode
python plhub.py build --target bytecode --release

# Build native executable (when available)
python plhub.py build --target native --release
```

## Example Session

```
================================================
       ADVANCED CALCULATOR v1.0
================================================

Main Menu:
  1. Basic Operations
  2. Advanced Operations
  3. View History
  4. Clear History
  5. Exit

Enter your choice (1-5):
> 1

Basic Operations:
  a. Addition
  b. Subtraction
  c. Multiplication
  d. Division

Enter operation (a-d):
> a

Enter first number:
> 42

Enter second number:
> 8

─────────────────────────────────────
📊 Result:
   42 Addition 8 = 50
─────────────────────────────────────
```

## Project Structure

```
calculator/
├── src/
│   └── main.poh           # Main application
├── tests/
│   └── test_basic.poh     # Test suite
├── plhub.json             # Project configuration
└── README.md              # This file
```

## Testing

The test suite covers:

- Basic arithmetic operations (add, subtract, multiply, divide)
- Advanced operations (power, average, percentage)
- Edge cases (zero, negative numbers)
- List operations (history tracking)

Expected output:
```
════════════════════════════════════════
   CALCULATOR TEST SUITE
════════════════════════════════════════

Test 1: Addition (5 + 3 = 8)
  ✓ PASSED
Test 2: Subtraction (10 - 4 = 6)
  ✓ PASSED
...
════════════════════════════════════════
   TEST SUMMARY
════════════════════════════════════════
Total tests: 10
Passed: 10
Failed: 0

✓ ALL TESTS PASSED! 🎉
════════════════════════════════════════
```

## Architecture

### Menu System
The application uses a simple menu-driven architecture with a main loop that handles user input and dispatches to operation handlers.

### History Tracking
All calculations are stored in a list and can be viewed or cleared by the user.

### Error Handling
The application validates user input and handles edge cases like division by zero.

## Future Enhancements

- [ ] Save/load history to file
- [ ] Scientific functions (sin, cos, tan, log)
- [ ] Expression parser (evaluate "2 + 3 * 4")
- [ ] Unit conversion
- [ ] Graphing capabilities
- [ ] GUI version

## License

MIT License - see LICENSE file for details.

## Author

PohLang Team
