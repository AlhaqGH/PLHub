# UI Showcase Example

This example demonstrates the PLHub UI toolkit capabilities using **simple, natural PohLang statements**.

## Features Demonstrated

- **Card Display**: Simple framed content blocks with titles and body text
- **Button Widgets**: Interactive components with styled labels
- **Stack Layouts**: Vertical lists of items
- **Styling**: Uses the `default_light` theme (configured in `ui/styles/active_style.json`)

## Design Philosophy

All widgets are built using **only natural PohLang Phase 1 statements**:
- `Set` - Assign values to variables
- `Write` - Display text
- `If/Otherwise` - Conditional logic
- `Repeat times` - Simple loops
- Natural operators: `plus`, `minus`, `is greater than`, etc.

**No complex syntax** - no function parameters, no brackets, no symbols. Just natural language!

## Running

```bash
cd Examples/ui_showcase
cargo run --manifest-path ../../PohLang/runtime/Cargo.toml -- main.poh --run
```

Or using the PLHub CLI (if configured):
```bash
python ../../plhub.py run main.poh
```

## Exploring

- **Themes**: Check `ui/styles/active_style.json` and `ui/styles/themes/`
- **Widgets**: View `ui/widgets/welcome_card.poh` for a simple standalone widget example
- **Main Program**: See `main.poh` for inline widget demonstrations

## Customizing

### Try Different Themes

```bash
cd Examples/ui_showcase
python ../../plhub.py style list
python ../../plhub.py style apply midnight_dark
cargo run --manifest-path ../../PohLang/runtime/Cargo.toml -- main.poh --run
```

### Generate Additional Widgets

```bash
python ../../plhub.py widget generate button --name ActionButton
python ../../plhub.py widget generate card --name InfoCard
python ../../plhub.py widget generate stack --name MenuStack
```

Each generated widget is a **standalone PohLang program** using simple statements. Just open the file, modify the variable values, and run it!

### Widget Examples

**Button Widget** (`ui/widgets/action_button.poh`):
```poh
Start Program

Set button_text to "Click Me"
Write "[ " plus button_text plus " ]"

End Program
```

**Card Widget** (`ui/widgets/info_card.poh`):
```poh
Start Program

Set card_title to "My Title"
Set card_body to "My content here"

Write "========================"
Write card_title
Write "------------------------"
Write card_body
Write "========================"

End Program
```

**Stack Layout** (`ui/widgets/menu_stack.poh`):
```poh
Start Program

Set item_count to 3
Set counter to 1

Write "Stack Layout:"
Repeat item_count times
    Write "Item " plus counter
    Increase counter by 1
End

End Program
```

