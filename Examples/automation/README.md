# Automation Examples

This directory contains examples demonstrating PLHub's automation features.

## Examples

### 1. Hot Reload Demo (`hotreload_demo.poh`)

Demonstrates hot reload functionality:

```bash
# Start the dev server
python ../../plhub.py dev --file hotreload_demo.poh

# Now edit hotreload_demo.poh and save
# Watch the application automatically reload!
```

### 2. Test Example (`test_arithmetic.poh`)

Example test file showing test patterns:

```bash
# Run the test
cargo run --manifest-path ../../PohLang/runtime/Cargo.toml -- test_arithmetic.poh --run

# Or use automated test runner (when in a project with tests/ directory)
python ../../plhub.py test
```

## Creating Your Own Examples

### Hot Reload App

1. Create a `.poh` file with your application code
2. Run with: `python plhub.py dev --file yourfile.poh`
3. Edit and save - watch it reload instantly!

### Test Files

1. Create a `tests/` directory in your project
2. Add `.poh` files with "test" in the name
3. Run with: `python plhub.py test`
4. Or watch mode: `python plhub.py test --watch`

## Tips

- **Hot Reload**: Changes are debounced (500ms) to avoid rapid reloads
- **Watch Mode**: Only rebuilds changed files and their dependencies
- **Test Watch**: Watches both `src/` and `tests/` directories
- **VS Code**: Use tasks (`Ctrl+Shift+B`) for quick access to automation

## Requirements

Optional but recommended:
```bash
pip install watchdog
```

Provides more efficient file watching than polling.
