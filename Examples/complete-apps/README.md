# Complete Applications - Examples

This directory contains **production-ready complete applications** built with PohLang and PLHub, demonstrating full end-to-end development workflows.

## 📱 Available Applications

### 1. Advanced Calculator
**Location:** `calculator/`

A comprehensive console calculator with basic and advanced mathematical operations.

**Features:**
- ✅ Basic operations (add, subtract, multiply, divide)
- ✅ Advanced operations (power, square root, percentage, averages)
- ✅ Calculation history tracking
- ✅ Interactive menu system
- ✅ Comprehensive test suite (10 tests)

**Quick Start:**
```bash
cd calculator
python plhub.py run src/main.poh
```

**Build:**
```bash
python plhub.py build --target bytecode --release
```

[📖 Full Documentation →](calculator/README.md)

---

### 2. Todo List Manager
**Location:** `todo-manager/`

A complete task management application with priorities, filtering, and statistics.

**Features:**
- ✅ Task CRUD operations (Create, Read, Update, Delete)
- ✅ Three priority levels (High, Medium, Low)
- ✅ Filter by priority and status
- ✅ Search functionality
- ✅ Statistics and completion tracking
- ✅ Test suite (10 tests)

**Quick Start:**
```bash
cd todo-manager
python plhub.py run src/main.poh
```

[📖 Full Documentation →](todo-manager/README.md)

---

### 3. Number Guessing Game
**Location:** `number-game/`

An interactive number guessing game with difficulty levels, hints, and high scores.

**Features:**
- ✅ Three difficulty levels (Easy, Medium, Hard)
- ✅ Smart hint system (direction + proximity)
- ✅ Statistics tracking (win rate, best score)
- ✅ Session management
- ✅ Comprehensive test suite (15 tests)

**Quick Start:**
```bash
cd number-game
python plhub.py run src/main.poh
```

[📖 Full Documentation →](number-game/README.md)

---

## 🎯 What Makes These "Complete" Applications?

Each application demonstrates:

### ✅ Full Project Structure
```
app-name/
├── src/               # Source code
│   └── main.poh      # Main entry point
├── tests/            # Test suite
│   └── test_*.poh    # Unit tests
├── plhub.json        # Project configuration
└── README.md         # Complete documentation
```

### ✅ Production-Ready Features
- **Error handling**: Validates inputs, handles edge cases
- **User experience**: Clear menus, formatted output, helpful messages
- **Testing**: Comprehensive test coverage with automated test suites
- **Documentation**: README with usage examples and architecture notes
- **Build configuration**: Ready for deployment

### ✅ Best Practices
- Clean code structure
- Clear variable names
- Comments explaining complex logic
- Modular organization
- Consistent formatting

### ✅ Complete Workflows
Each app demonstrates the full cycle:
1. **Create** - Project initialization with proper structure
2. **Develop** - Feature implementation with PohLang
3. **Test** - Automated testing with test suites
4. **Build** - Compilation to bytecode/native
5. **Deploy** - Ready for distribution

---

## 📊 Feature Comparison

| Feature | Calculator | Todo Manager | Number Game |
|---------|-----------|--------------|-------------|
| Menu System | ✅ | ✅ | ✅ |
| Data Persistence | ❌ | ❌ | ✅ (stats) |
| User Input | ✅ | ✅ | ✅ |
| Complex Logic | ✅ | ✅ | ✅ |
| List Operations | ✅ | ✅ | ❌ |
| Math Operations | ✅ | ✅ | ✅ |
| Conditional Flow | ✅ | ✅ | ✅ |
| Loops | ✅ | ✅ | ✅ |
| Statistics | ✅ (history) | ✅ | ✅ |
| Test Coverage | 10 tests | 10 tests | 15 tests |

---

## 🚀 Quick Start Guide

### Run Any Application

```bash
# Navigate to application directory
cd <app-name>

# Run the application
python plhub.py run src/main.poh

# Run tests
python plhub.py run tests/test_*.poh

# Build for production
python plhub.py build --target bytecode --release
```

### Test All Applications

```bash
# Test calculator
cd calculator && python plhub.py run tests/test_basic.poh

# Test todo manager
cd ../todo-manager && python plhub.py run tests/test_main.poh

# Test number game
cd ../number-game && python plhub.py run tests/test_game.poh
```

### Build All Applications

```bash
# Build all apps
for app in calculator todo-manager number-game; do
    cd $app
    python plhub.py build --target bytecode --release
    cd ..
done
```

---

## 📚 Learning Path

### Beginner Level
Start with **Calculator** to learn:
- Basic arithmetic operations
- User input and output
- Menu systems
- Simple conditionals

### Intermediate Level
Move to **Number Game** to understand:
- Game loops and state management
- Complex conditional logic
- Statistical calculations
- User feedback systems

### Advanced Level
Master **Todo Manager** to explore:
- Data structures (nested lists)
- CRUD operations
- Filtering and searching
- Complex state management

---

## 🎓 Educational Value

Each application teaches specific PohLang concepts:

### Calculator
- **Arithmetic**: All basic math operations
- **Advanced Math**: Power, square root, percentages
- **History**: List append and iteration
- **Formatting**: Clear output presentation

### Todo Manager
- **Data Structures**: List of lists (nested data)
- **State Management**: Complex object manipulation
- **Filtering**: Conditional data display
- **CRUD**: Full lifecycle operations

### Number Game
- **Game Logic**: Win/lose conditions
- **Hints**: Distance calculations
- **Statistics**: Averages, percentages, comparisons
- **User Flow**: Multi-level menus

---

## 🛠️ Development Workflow

For each application, follow this workflow:

### 1. Understand the Code
```bash
# Read the main.poh file
# Understand the logic flow
# Review test cases
```

### 2. Experiment
```bash
# Modify features
# Add new capabilities
# Try different approaches
```

### 3. Test Changes
```bash
# Run the test suite
# Verify functionality
# Fix any issues
```

### 4. Build & Deploy
```bash
# Build production version
# Create distributable
# Share with others
```

---

## 🎯 Extension Ideas

### Calculator Enhancements
- [ ] Scientific functions (sin, cos, tan)
- [ ] Expression parser ("2 + 3 * 4")
- [ ] Save/load history to file
- [ ] Unit conversions
- [ ] Currency calculations

### Todo Manager Enhancements
- [ ] File persistence (save/load)
- [ ] Due dates and reminders
- [ ] Categories and tags
- [ ] Subtasks
- [ ] Export to CSV/JSON

### Number Game Enhancements
- [ ] True random numbers
- [ ] Multiplayer mode
- [ ] Custom ranges
- [ ] Time-based scoring
- [ ] Difficulty progression

---

## 📖 Additional Resources

- **Complete App Building Guide**: [../../docs/COMPLETE_APP_GUIDE.md](../../docs/COMPLETE_APP_GUIDE.md)
- **PohLang Documentation**: [../../../../PohLang/README.md](../../../../PohLang/README.md)
- **PLHub CLI Reference**: [../../docs/cli_reference.md](../../docs/cli_reference.md)
- **Development Workflow**: [../../docs/development_workflow.md](../../docs/development_workflow.md)

---

## 🤝 Contributing

Want to add your own complete application?

1. Create a new directory: `your-app-name/`
2. Follow the standard structure (src/, tests/, plhub.json, README.md)
3. Ensure comprehensive testing
4. Write clear documentation
5. Submit a pull request

---

## 📝 License

All example applications are provided under MIT License. Feel free to use, modify, and distribute as needed.

---

## 🎉 Summary

These complete applications prove that **PohLang + PLHub** can be used to build:

✅ **Real applications** - Not just demos or snippets  
✅ **Full workflows** - From creation to deployment  
✅ **Production quality** - With testing and documentation  
✅ **Best practices** - Clean, maintainable code  

**Start building your own complete applications today!** 🚀
