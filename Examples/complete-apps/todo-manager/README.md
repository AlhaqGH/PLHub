# Todo List Manager

A complete task management application with priorities, filtering, and statistics.

## Features

✅ **Task Management**
- Add new tasks with priorities
- Mark tasks as complete
- Delete tasks
- Update task status

✅ **Organization**
- Three priority levels (High, Medium, Low)
- Filter by priority
- Filter by status (pending/completed)
- Search functionality

✅ **Analytics**
- Task statistics
- Completion rate tracking
- Priority distribution
- Real-time counters

✅ **User Interface**
- Clean, formatted output
- Status icons (✅ ⬜)
- Priority indicators (🔴 🟡 🟢)
- Interactive menus

## Installation

```bash
cd Examples/complete-apps/todo-manager
```

## Usage

### Run the Application

```bash
python plhub.py run src/main.poh
```

### Run Tests

```bash
python plhub.py run tests/test_main.poh
```

### Build

```bash
# Build to bytecode
python plhub.py build --target bytecode --release
```

## Example Session

```
════════════════════════════════════════
      TODO LIST MANAGER v1.0
════════════════════════════════════════

────────────────────────────────────────
MAIN MENU
────────────────────────────────────────
  1. View All Tasks
  2. Add New Task
  3. Complete Task
  4. Delete Task
  5. View by Priority
  6. View by Status
  7. Search Tasks
  8. Statistics
  9. Exit
────────────────────────────────────────
Enter choice (1-9):
> 2

ADD NEW TASK
────────────────────────────────────────
Task title:
> Finish project documentation

Priority (1=Low, 2=Medium, 3=High):
> 3

✓ Task added successfully!

────────────────────────────────────────
Enter choice (1-9):
> 1

════════════════════════════════════════
        ALL TASKS
════════════════════════════════════════
[1] ⬜ Finish project documentation (HIGH)
════════════════════════════════════════

────────────────────────────────────────
Enter choice (1-9):
> 8

════════════════════════════════════════
        STATISTICS
════════════════════════════════════════
Total Tasks: 1
────────────────────────────────────────
Status:
  ✅ Completed: 0
  ⬜ Pending:   1

Priority:
  🔴 High:   1
  🟡 Medium: 0
  🟢 Low:    0

Completion Rate: 0%
════════════════════════════════════════
```

## Project Structure

```
todo-manager/
├── src/
│   └── main.poh           # Main application
├── tests/
│   └── test_main.poh      # Test suite
├── plhub.json             # Project configuration
└── README.md              # This file
```

## Data Model

Each task is represented as a list with 4 elements:

```
[id, title, priority, completed]
```

- **id**: Unique identifier (number)
- **title**: Task description (string)
- **priority**: 1 (Low), 2 (Medium), or 3 (High)
- **completed**: True or False

Example:
```
[1, "Buy groceries", 2, False]
```

## Testing

The test suite covers:

1. Adding tasks to empty list
2. Adding multiple tasks
3. Accessing task properties
4. Marking tasks as complete
5. Deleting tasks
6. Filtering by priority
7. Calculating completion rate
8. Counting pending tasks
9. Priority distribution
10. Finding tasks by ID

Expected output:
```
════════════════════════════════════════
   TODO MANAGER TEST SUITE
════════════════════════════════════════

Test 1: Add task to empty list
  ✓ PASSED
Test 2: Add multiple tasks
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

## Key Features Demonstrated

### List Operations
- Appending items
- Accessing by index
- Counting items
- Filtering
- Rebuilding lists (for updates/deletes)

### Data Structures
- Nested lists (list of lists)
- Multiple properties per item
- Boolean flags

### Control Flow
- While loops with counters
- Nested conditionals
- State machines

### User Interaction
- Menu systems
- Input validation
- Formatted output

## Future Enhancements

- [ ] Persistent storage (save to file)
- [ ] Due dates and reminders
- [ ] Categories/tags
- [ ] Subtasks
- [ ] Export to CSV/JSON
- [ ] Web interface
- [ ] Mobile apps

## License

MIT License - see LICENSE file for details.

## Author

PohLang Team
