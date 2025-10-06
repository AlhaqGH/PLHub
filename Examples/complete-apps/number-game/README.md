# Number Guessing Game

An interactive number guessing game with difficulty levels, hints, and statistics tracking.

## Features

✅ **Game Modes**
- Easy: 1-50 range, unlimited guesses
- Medium: 1-100 range, 10 guesses
- Hard: 1-500 range, 7 guesses

✅ **Gameplay**
- Smart hint system (too high/low)
- Proximity hints (very close/getting warmer)
- Limited guesses in harder modes
- Win/lose conditions

✅ **Statistics**
- Games played counter
- Games won counter
- Win rate calculation
- Average attempts tracking
- Best score (fewest attempts)

✅ **User Experience**
- Clear instructions
- Animated feedback
- Emoji indicators
- Difficulty selection
- Session summary

## Installation

```bash
cd Examples/complete-apps/number-game
```

## Usage

### Run the Game

```bash
python plhub.py run src/main.poh
```

### Run Tests

```bash
python plhub.py run tests/test_game.poh
```

### Build

```bash
# Build to bytecode
python plhub.py build --target bytecode --release
```

## Example Game Session

```
════════════════════════════════════════
    NUMBER GUESSING GAME v1.0
════════════════════════════════════════

────────────────────────────────────────
MAIN MENU
────────────────────────────────────────
  1. Play Game
  2. Instructions
  3. Statistics
  4. Exit
────────────────────────────────────────
Enter choice:
> 1

SELECT DIFFICULTY
────────────────────────────────────────
  1. Easy   (1-50,  unlimited guesses)
  2. Medium (1-100, 10 guesses)
  3. Hard   (1-500, 7 guesses)
────────────────────────────────────────
Enter difficulty:
> 2

════════════════════════════════════════
      GAME STARTED - MEDIUM
════════════════════════════════════════
I'm thinking of a number between 1 and 100
You have 10 guesses
════════════════════════════════════════

Guess #1 (Remaining: 9)
Enter your guess:
> 50

❌ Too low! Try higher

Guess #2 (Remaining: 8)
Enter your guess:
> 75

❌ Too high! Try lower

Guess #3 (Remaining: 7)
Enter your guess:
> 60

❌ Too low! Try higher
💡 Hint: Getting warmer!

Guess #4 (Remaining: 6)
Enter your guess:
> 65

❌ Too low! Try higher
💡 Hint: You're very close!

Guess #5 (Remaining: 5)
Enter your guess:
> 67

🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉
     CONGRATULATIONS! YOU WON!
🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉

You found the number 67
Attempts: 5

Score: 45 points

```

## Project Structure

```
number-game/
├── src/
│   └── main.poh           # Main game
├── tests/
│   └── test_game.poh      # Test suite
├── plhub.json             # Project configuration
└── README.md              # This file
```

## Game Mechanics

### Number Generation
In a full implementation, the secret number would be randomly generated based on the difficulty range. For this demo, it uses a fixed number for testing purposes.

### Hint System

The game provides two types of hints:

1. **Direction Hints**
   - "Too high" when guess > secret
   - "Too low" when guess < secret

2. **Proximity Hints**
   - "Very close" when distance < 5
   - "Getting warmer" when distance < 10

### Scoring

Score = attempts × 10 - difficulty_bonus

- Easy: No bonus
- Medium: -5 bonus
- Hard: -10 bonus

Lower score is better!

### Win/Lose Conditions

**Win:** Guess == secret number

**Lose:** attempts >= max_guesses (Medium/Hard only)

## Testing

The test suite covers 15 test cases:

1. Less than comparison
2. Greater than comparison
3. Equality comparison
4. Distance calculation (positive)
5. Distance calculation (negative)
6. Attempts counter
7. Remaining guesses
8. Win condition
9. Game over condition
10. Score calculation
11. Win rate calculation
12. Average attempts
13. Best score update
14. Proximity hint
15. Difficulty range

Expected output:
```
════════════════════════════════════════
   NUMBER GAME TEST SUITE
════════════════════════════════════════

Test 1: Check if 25 < 50
  ✓ PASSED
Test 2: Check if 75 > 50
  ✓ PASSED
...
════════════════════════════════════════
   TEST SUMMARY
════════════════════════════════════════
Total tests: 15
Passed: 15
Failed: 0

✓ ALL TESTS PASSED! 🎉
════════════════════════════════════════
```

## Strategy Tips

### Binary Search Approach

For optimal gameplay, use binary search:

1. Start with middle number of range
2. If too high, guess middle of lower half
3. If too low, guess middle of upper half
4. Repeat until found

Example for 1-100 range:
```
Guess 1: 50
  Too low → Range is now 51-100
Guess 2: 75
  Too high → Range is now 51-74
Guess 3: 62
  Too low → Range is now 63-74
Guess 4: 68
  And so on...
```

This guarantees finding any number in 1-100 within 7 guesses!

## Future Enhancements

- [ ] True random number generation
- [ ] Difficulty presets (speed mode, zen mode)
- [ ] Multiplayer mode
- [ ] Leaderboards
- [ ] Custom range selection
- [ ] Hint penalties (harder mode)
- [ ] Time-based scoring
- [ ] Sound effects

## License

MIT License - see LICENSE file for details.

## Author

PohLang Team
