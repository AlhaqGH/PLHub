# Math Utils Package

Mathematical utility functions for PohLang programs.

## Functions

### `square(number)`
Returns the square of a number.
```pohLang
Set result to square(5)  # Returns 25
```

### `power(base, exponent)`
Returns base raised to the power of exponent.
```pohLang
Set result to power(2, 3)  # Returns 8
```

### `abs(number)`
Returns the absolute value of a number.
```pohLang
Set result to abs(-5)  # Returns 5
```

### `max(a, b)`
Returns the larger of two numbers.
```pohLang
Set result to max(10, 7)  # Returns 10
```

### `min(a, b)`
Returns the smaller of two numbers.
```pohLang
Set result to min(10, 7)  # Returns 7
```

### `is_even(number)`
Returns true if number is even, false otherwise.
```pohLang
Set result to is_even(4)  # Returns true
```

### `is_odd(number)`
Returns true if number is odd, false otherwise.
```pohLang
Set result to is_odd(4)  # Returns false
```

## Usage

```pohLang
# Import the math_utils package
Import "math_utils"

# Use the functions
Set x to 5
Set squared to square(x)
Write "5 squared is " plus squared

Set is_x_even to is_even(x)
If is_x_even is true
    Write x plus " is even"
Otherwise
    Write x plus " is odd"
End
```

## Installation

```bash
plhub install math_utils
```