# PLHub UI Toolkit Guide

PLHub includes a comprehensive UI toolkit for managing styles and reusable widgets in PohLang projects.

## Overview

The UI toolkit provides:

- **Styling System** – Theme definitions with tokens, typography, elevation, and component defaults
- **Widget Library** – Reusable PohLang component templates for common UI patterns
- **CLI Integration** – Commands to list, apply, create, and preview themes and widgets
- **Project Scaffolding** – Automatic UI structure generation during project creation

---

## Styling System

### Concepts

- **Theme**: A JSON manifest defining color tokens, typography, elevations, and component styles
- **Active Theme**: The theme currently applied to a project (tracked in `ui/styles/active_style.json`)
- **Built-in Themes**: Shipped with PLHub under `PLHub/styles/`
- **Project Themes**: Editable copies or custom themes stored in `<project>/ui/styles/themes/`

### CLI Commands

#### List Available Themes

```bash
python plhub.py style list
```

Output:
```
Built-in themes:
  - default_light: Default Light - Baseline light theme...
  - midnight_dark: Midnight Dark - High-contrast dark theme...

Project themes:
  - custom_sunset: Custom Sunset (ui/styles/themes/custom_sunset.json) - ...

Active theme: Default Light (default_light)
```

Use `--json` for machine-readable output.

#### Show Theme Details

```bash
python plhub.py style show midnight_dark
```

Output:
```
Name: Midnight Dark
Key: midnight_dark
Source: builtin
Location: C:\...\PLHub\styles\midnight_dark.json
Description: High-contrast dark theme inspired by modern developer tooling.
Token groups: background, surface, foreground, ...
```

Use `--json` to emit the full theme definition.

#### Apply a Theme

Inside a PohLang project:

```bash
python plhub.py style apply midnight_dark
```

This:
1. Copies the theme JSON to `ui/styles/themes/midnight_dark.json` (if not already present)
2. Updates `ui/styles/active_style.json` to reference the applied theme
3. Computes a checksum for integrity tracking

Use `--force` to overwrite existing theme files.

#### Create a Custom Theme

```bash
python plhub.py style create "Sunset Glow" --base default_light --description "Warm color palette"
```

This:
1. Clones the base theme
2. Updates the name and description
3. Saves it to `ui/styles/themes/sunset_glow.json`

Add `--activate` to immediately apply the new theme after creation.

### Theme Structure

Example theme JSON (`ui/styles/themes/default_light.json`):

```json
{
  "name": "Default Light",
  "description": "Baseline light theme...",
  "tokens": {
    "background": "#FFFFFF",
    "surface": "#F5F7FA",
    "foreground": "#1F2933",
    "primary": "#2563EB",
    "accent": "#F97316",
    "error": "#EF4444",
    ...
  },
  "typography": {
    "fontFamily": "Inter, Segoe UI, sans-serif",
    "fontSizeBase": 16,
    "lineHeight": 1.6,
    ...
  },
  "elevation": {
    "level0": "none",
    "level1": "0px 1px 2px rgba(...)",
    ...
  },
  "components": {
    "button": {
      "padding": "0.6rem 1.25rem",
      "radius": "0.5rem",
      ...
    },
    "card": { ... },
    "input": { ... }
  }
}
```

### Active Theme Manifest

`ui/styles/active_style.json`:

```json
{
  "activeTheme": "midnight_dark",
  "displayName": "Midnight Dark",
  "themePath": "themes/midnight_dark.json",
  "source": "builtin",
  "appliedAt": "2025-10-05T02:50:01Z",
  "checksum": "64dce4b3b3e87e7eb0000160096dd758..."
}
```

### Integration Notes

- Themes are currently **manifest-only**; the PohLang runtime does not interpret them directly.
- Future tooling (transpilers, LSP, editors) can read these manifests to apply styling during code generation or preview.
- For now, themes serve as a centralized design system for projects and a foundation for upcoming UI features.

---

## Widget Library

### Concepts

- **Widget Template**: A JSON descriptor defining simple `.poh` files using natural PohLang statements
- **Built-in Templates**: Shipped with PLHub under `PLHub/widgets/templates/`
- **Project Templates**: Custom templates stored in `<project>/ui/widgets/templates/`
- **Generated Widgets**: Simple `.poh` programs using Set, Write, and basic control structures

> **Design Philosophy**: Widgets are simple, standalone programs written in natural PohLang. They use only basic statements (Set, Write, If/Otherwise, Repeat times) with natural operators. No complex function parameters or imports needed.

### CLI Commands

#### List Widget Templates

```bash
python plhub.py widget list
```

Output:
```
Widget templates:
  - button: Button Widget (display; button, action, interactive) - ...
  - card: Card Widget (display; card, display, text) - ...
  - stack: Stack Layout (layout; stack, layout, list) - ...

Project widgets:
  - ui\widgets\welcome_card.poh
  - ui\widgets\primary_button.poh
```

Use `--json` for structured output.

#### Preview a Widget Template

```bash
python plhub.py widget preview card
```

Output:
```
Template: Card Widget (card)
Framed content block with a title and body text - simple display format.
  File: ui/widgets/{{widget_snake}}.poh - Widget definition

Preview snippet:

Set card_title to "Welcome"
Set card_body to "This is the card content"
Write "========================"
Write card_title
Write "------------------------"
Write card_body
Write "========================"
```

Use `--json` to get the full template metadata.

#### Generate a Widget

Inside a PohLang project:

```bash
python plhub.py widget generate button --name PrimaryButton
```

This:
1. Resolves the `button` template
2. Renders placeholders using the provided name (`PrimaryButton` → `primary_button.poh`)
3. Writes `ui/widgets/primary_button.poh` as a simple, standalone program

Use `--force` to overwrite existing files.  
Use `--dry-run` to preview file paths without writing.

### Widget Template Structure

Example template (`PLHub/widgets/templates/button.json`):

```json
{
  "key": "button",
  "name": "Button Widget",
  "description": "Simple interactive button display using natural PohLang statements.",
  "category": "display",
  "tags": ["button", "action", "interactive"],
  "preview": [
    "Set button_text to \"Click Me\"",
    "Write \"▶ \" plus button_text plus \" ◀\""
  ],
  "files": [
    {
      "path": "ui/widgets/{{widget_snake}}.poh",
      "description": "Button widget with customizable text",
      "content": [
        "Start Program",
        "",
        "# {{widget_title}} - Button Widget",
        "# Simple button display",
        "",
        "Set button_text to \"My Button\"",
        "Write \"▶ \" plus button_text plus \" ◀\"",
        "",
        "End Program"
      ]
    }
  ]
}
```

### Placeholder Variables

When generating a widget with `--name MyAwesomeWidget`, the following placeholders are available:

| Placeholder | Example Value | Description |
|-------------|---------------|-------------|
| `{{widget_name}}` | `MyAwesomeWidget` | Original name as provided |
| `{{widget_snake}}` | `my_awesome_widget` | snake_case version |
| `{{widget_pascal}}` | `MyAwesomeWidget` | PascalCase version |
| `{{widget_kebab}}` | `my-awesome-widget` | kebab-case version |
| `{{widget_title}}` | `My Awesome Widget` | Title Case with spaces |

### Using Generated Widgets

Generated widgets are standalone PohLang programs. You can customize the variable values and run them directly:

**Example: `ui/widgets/primary_button.poh`**
```poh
Start Program

# Primary Button - Button Widget
# Simple button display

Set button_text to "Submit"
Write "▶ " plus button_text plus " ◀"

End Program
```

**Example: `ui/widgets/info_card.poh`**
```poh
Start Program

# Info Card - Card Widget
# Displays content in a framed box

Set card_title to "Welcome"
Set card_body to "Thanks for using PohLang!"

Write "========================"
Write card_title
Write "------------------------"
Write card_body
Write "========================"

End Program
```

To use a widget in your main program, simply copy the relevant code and adjust variable values as needed.

---

## Project Scaffolding

When you create a new project, PLHub automatically:

1. Creates `ui/styles/` with an active theme and README
2. Copies the default theme to `ui/styles/themes/`
3. Creates `ui/widgets/` with a sample widget and README
4. Generates a `WelcomeCard` widget as a starting point

### Customizing During Creation

```bash
# Use a different default theme
python plhub.py create my_app --ui-theme midnight_dark

# Skip UI scaffolding entirely
python plhub.py create my_app --no-ui
```

If you skip UI scaffolding during creation, you can manually apply a theme later:

```bash
cd my_app
python plhub.py style apply default_light
```

---

## Examples

### Full Workflow: Creating a Themed Project with Custom Widgets

```bash
# 1. Create project with dark theme
python plhub.py create dashboard_app --ui-theme midnight_dark
cd dashboard_app

# 2. List available themes
python plhub.py style list

# 3. Create a custom theme
python plhub.py style create "Dashboard Blue" --base midnight_dark --activate

# 4. Generate widgets
python plhub.py widget generate card --name MetricsCard
python plhub.py widget generate stack --name SidebarMenu

# 5. Edit and use widgets in src/main.poh
```

### Sharing Themes Across Projects

To reuse a custom theme:

1. Copy the theme JSON from one project's `ui/styles/themes/` folder
2. Place it in `PLHub/styles/` (requires modifying PLHub directly) or another project's themes folder
3. Apply it via `python plhub.py style apply <theme_key>`

Alternatively, store project-specific templates in `ui/widgets/templates/` or `ui/styles/themes/` and commit them to version control.

---

## Advanced Topics

### Theme Validation

PLHub does not currently validate theme schemas at runtime. Ensure your JSON is well-formed and includes expected keys (`tokens`, `typography`, `elevation`, `components`) to avoid tooling issues in future integrations.

### Widget Nesting

Widgets can import other widgets:

**`ui/widgets/form.poh`**
```poh
Import "ui/widgets/primary_button.poh"
Import "ui/widgets/input_field.poh"

Make render_form with title
    Write title
    Use render_input_field with label set to "Name"
    Use render_primary_button with label set to "Submit" and action set to None
End
```

### Custom Widget Templates

Create your own templates in `ui/widgets/templates/my_template.json` following the same structure as built-in templates. They will be discovered automatically by `plhub widget list`.

---

## Troubleshooting

**Issue**: `Error: Style application must be run inside a PohLang project`

- **Solution**: Ensure you are in a directory containing `plhub.json`. Run `python plhub.py init` if needed.

**Issue**: `Error: Widget file '...' already exists`

- **Solution**: Use `--force` to overwrite, or rename/delete the existing file.

**Issue**: Theme changes not reflected

- **Reminder**: Themes are manifest-only. Check that your tooling (transpiler, editor, etc.) reads `ui/styles/active_style.json` to apply styles.

---

## Future Enhancements

- **Live Preview**: Real-time theme preview in VS Code extension
- **Schema Validation**: Enforce theme structure at CLI level
- **Widget Composition**: GUI for combining widgets visually
- **Theme Variants**: Light/dark mode switching with a single command

---

For more details, see:
- [UI Toolkit Plan](UI_TOOLKIT_PLAN.md) – Development roadmap
- [PLHub README](../README.md) – Main documentation
- [PohLang Vocabulary](../../PohLang/spec/Vocabulary.md) – Language reference
