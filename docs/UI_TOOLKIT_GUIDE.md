# PLHub UI Toolkit Documentation

## Overview

The PLHub UI Toolkit provides a comprehensive set of reusable UI components and themes for building PohLang applications. It includes 16+ widget templates and 6 professionally designed themes.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Theme Management](#theme-management)
3. [Widget Templates](#widget-templates)
4. [CLI Commands](#cli-commands)
5. [Best Practices](#best-practices)

---

## Getting Started

### Installation

The UI Toolkit is included with PLHub v0.5.0+. No additional installation needed!

### Quick Start

```bash
# Create a new project with UI scaffolding
python plhub.py create my_app --template basic

# List available themes
python plhub.py style list

# Apply a theme
python plhub.py style apply ocean_blue

# List available widgets
python plhub.py widget list

# Generate a widget
python plhub.py widget generate button --name PrimaryButton
```

---

## Theme Management

### Available Themes

#### 1. **Default Light** (default_light.json)
- **Purpose**: General-purpose light theme
- **Best For**: Business applications, productivity tools
- **Colors**: White background, blue primary, clean borders
- **Typography**: Inter, 16px base, 1.6 line height

#### 2. **Midnight Dark** (midnight_dark.json)
- **Purpose**: High-contrast dark theme for low-light environments
- **Best For**: Developer tools, night mode applications
- **Colors**: Dark blue-gray background, cyan primary, purple secondary
- **Typography**: Inter, 16px base, 1.7 line height

#### 3. **Ocean Blue** (ocean_blue.json)
- **Purpose**: Calm, professional blue-themed design
- **Best For**: Corporate applications, data dashboards
- **Colors**: Light blue background, ocean blue primary
- **Typography**: Inter, 16px base, 1.6 line height

#### 4. **Sunset Warm** (sunset_warm.json)
- **Purpose**: Warm, inviting color palette
- **Best For**: Creative applications, user-friendly interfaces
- **Colors**: Warm orange/peach tones, welcoming feel
- **Typography**: Inter, 16px base, 1.65 line height

#### 5. **Forest Green** (forest_green.json)
- **Purpose**: Natural, calming green palette
- **Best For**: Environmental apps, wellness applications
- **Colors**: Green-based color scheme, natural feel
- **Typography**: Inter, 16px base, 1.65 line height

#### 6. **High Contrast** (high_contrast.json)
- **Purpose**: WCAG AAA compliant accessibility theme
- **Best For**: Accessibility, public kiosks, elderly users
- **Colors**: Pure black/white, high contrast ratios
- **Typography**: Arial, 18px base (larger), 1.75 line height

### Theme Structure

Each theme JSON contains:

```json
{
  "name": "Theme Name",
  "description": "Theme description",
  "tokens": {
    "background": "#FFFFFF",
    "surface": "#F5F7FA",
    "foreground": "#1F2933",
    "primary": "#2563EB",
    "secondary": "#10B981",
    "accent": "#F97316",
    "error": "#EF4444",
    "warning": "#F59E0B",
    "info": "#3B82F6",
    "success": "#10B981"
  },
  "typography": {
    "fontFamily": "Inter, sans-serif",
    "fontSizeBase": 16,
    "headingScale": [2.25, 1.75, 1.5, 1.25, 1.0, 0.875],
    "lineHeight": 1.6
  },
  "elevation": {
    "level0": "none",
    "level1": "0px 1px 2px rgba(...)",
    "level2": "0px 4px 12px rgba(...)",
    "level3": "0px 12px 24px rgba(...)"
  },
  "components": {
    "button": {"padding": "...", "radius": "...", "fontWeight": 600},
    "card": {"radius": "...", "padding": "...", "border": "..."},
    "input": {"padding": "...", "radius": "...", "border": "..."}
  }
}
```

### CLI Commands

```bash
# List all themes
python plhub.py style list

# Show theme details
python plhub.py style show ocean_blue

# Apply a theme to current project
python plhub.py style apply midnight_dark

# Create a custom theme
python plhub.py style create "My Theme" --base default_light --description "Custom theme"

# Create and activate immediately
python plhub.py style create "My Theme" --base ocean_blue --activate
```

---

## Widget Templates

### Categories

1. **Form Widgets**: input, dropdown, checkbox, form
2. **Display Widgets**: button, card, table, progress, alert
3. **Layout Widgets**: navbar, footer, grid, stack
4. **Navigation Widgets**: tabs, accordion
5. **Overlay Widgets**: modal, tooltip

### Widget Reference

#### 1. Button Widget
**Category**: Display  
**File**: `ui/widgets/button.poh`

**Features**:
- Simple button display with label
- Bracket-style formatting
- Customizable text

**Preview**:
```pohlang
Set button_text to "Click Me"
Write "[ " plus button_text plus " ]"
```

**Usage**:
```bash
python plhub.py widget generate button --name SubmitButton
```

---

#### 2. Input Widget
**Category**: Form  
**File**: `ui/widgets/input.poh`

**Features**:
- Text input collection
- Label and placeholder support
- Input validation placeholder

**Preview**:
```pohlang
Set label to "Enter text"
Ask for value
Write "You entered: " plus value
```

**Usage**:
```bash
python plhub.py widget generate input --name UsernameInput
```

---

#### 3. Card Widget
**Category**: Display  
**File**: `ui/widgets/card.poh`

**Features**:
- Framed content block
- Title and body sections
- Border decoration

**Preview**:
```pohlang
Write "========================"
Write "Card Title"
Write "------------------------"
Write "Card content here"
Write "========================"
```

**Usage**:
```bash
python plhub.py widget generate card --name ProfileCard
```

---

#### 4. Dropdown Widget
**Category**: Form  
**File**: `ui/widgets/dropdown.poh`

**Features**:
- Multiple option selection
- Numbered menu format
- Choice validation

**Preview**:
```pohlang
Write "1. Option 1"
Write "2. Option 2"
Write "3. Option 3"
Ask for choice
```

**Usage**:
```bash
python plhub.py widget generate dropdown --name ColorPicker
```

---

#### 5. Checkbox Widget
**Category**: Form  
**File**: `ui/widgets/checkbox.poh`

**Features**:
- Boolean on/off selection
- Visual checkbox symbols [X] / [ ]
- State management

**Preview**:
```pohlang
Set is_checked to false
Write "[X] Accept terms" # if checked
Write "[ ] Accept terms" # if unchecked
```

**Usage**:
```bash
python plhub.py widget generate checkbox --name TermsCheckbox
```

---

#### 6. Modal Dialog Widget
**Category**: Overlay  
**File**: `ui/widgets/modal.poh`

**Features**:
- Full-screen overlay effect
- Title, message, and actions
- OK/Cancel buttons

**Preview**:
```pohlang
Write "========================================"
Write "  Confirmation Required"
Write "========================================"
Write "Are you sure?"
Write "[OK]    [Cancel]"
```

**Usage**:
```bash
python plhub.py widget generate modal --name ConfirmDialog
```

---

#### 7. Alert Widget
**Category**: Feedback  
**File**: `ui/widgets/alert.poh`

**Features**:
- Status notifications (success, warning, error, info)
- Icon indicators
- Dismiss action

**Preview**:
```pohlang
Write "⚠️  WARNING: Please save your work"
Write "[Dismiss]"
```

**Usage**:
```bash
python plhub.py widget generate alert --name WarningAlert
```

---

#### 8. Navigation Bar Widget
**Category**: Layout  
**File**: `ui/widgets/navbar.poh`

**Features**:
- Top navigation with logo
- Multiple menu items
- Active state indicator

**Preview**:
```pohlang
Write "║ MyApp  [Home] About  Contact ║"
```

**Usage**:
```bash
python plhub.py widget generate navbar --name MainNav
```

---

#### 9. Footer Widget
**Category**: Layout  
**File**: `ui/widgets/footer.poh`

**Features**:
- Page footer with links
- Copyright information
- Link separator formatting

**Preview**:
```pohlang
Write "About | Privacy | Terms | Contact"
Write "© 2025 MyApp. All rights reserved."
```

**Usage**:
```bash
python plhub.py widget generate footer --name MainFooter
```

---

#### 10. Grid Layout Widget
**Category**: Layout  
**File**: `ui/widgets/grid.poh`

**Features**:
- Multi-column grid layout
- Responsive design support
- Box-drawing characters

**Preview**:
```pohlang
Write "┌──────┬──────┬──────┐"
Write "│ Col1 │ Col2 │ Col3 │"
Write "└──────┴──────┴──────┘"
```

**Usage**:
```bash
python plhub.py widget generate grid --name ProductGrid
```

---

#### 11. Table Widget
**Category**: Display  
**File**: `ui/widgets/table.poh`

**Features**:
- Structured data display
- Headers and rows
- Column alignment

**Preview**:
```pohlang
Write "│ Name     │ Age │ City        │"
Write "│ John Doe │ 25  │ New York    │"
```

**Usage**:
```bash
python plhub.py widget generate table --name UserTable
```

---

#### 12. Tabs Widget
**Category**: Navigation  
**File**: `ui/widgets/tabs.poh`

**Features**:
- Tabbed interface
- Multiple content sections
- Active tab highlighting

**Preview**:
```pohlang
Write "[Tab 1] Tab 2  Tab 3"
Write "Content for Tab 1"
```

**Usage**:
```bash
python plhub.py widget generate tabs --name SettingsTabs
```

---

#### 13. Accordion Widget
**Category**: Navigation  
**File**: `ui/widgets/accordion.poh`

**Features**:
- Collapsible sections
- Expand/collapse indicators
- Multiple sections

**Preview**:
```pohlang
Write "▼ Section 1 (Expanded)"
Write "  Content here..."
Write "► Section 2 (Collapsed)"
```

**Usage**:
```bash
python plhub.py widget generate accordion --name FAQAccordion
```

---

#### 14. Progress Bar Widget
**Category**: Feedback  
**File**: `ui/widgets/progress.poh`

**Features**:
- Visual progress indicator
- Percentage display
- Loading states

**Preview**:
```pohlang
Write "[█████████       ] 65%"
Write "Loading...Please wait."
```

**Usage**:
```bash
python plhub.py widget generate progress --name UploadProgress
```

---

#### 15. Tooltip Widget
**Category**: Overlay  
**File**: `ui/widgets/tooltip.poh`

**Features**:
- Contextual help hints
- Hover/focus popups
- Information icon

**Preview**:
```pohlang
Write "Hover for help ℹ️ "
Write "┌─────────────────────┐"
Write "│ Tooltip information │"
Write "└─────────────────────┘"
```

**Usage**:
```bash
python plhub.py widget generate tooltip --name HelpTooltip
```

---

#### 16. Form Widget
**Category**: Form  
**File**: `ui/widgets/form.poh`

**Features**:
- Multi-field form
- Submit/Cancel actions
- Field validation placeholders

**Preview**:
```pohlang
Write "Name: [input]"
Write "Email: [input]"
Write "[Submit] [Cancel]"
```

**Usage**:
```bash
python plhub.py widget generate form --name RegistrationForm
```

---

## CLI Commands

### Style Commands

```bash
# List all available themes
python plhub.py style list

# List themes as JSON
python plhub.py style list --json

# Show theme details
python plhub.py style show <theme_name>
python plhub.py style show ocean_blue

# Show theme as raw JSON
python plhub.py style show midnight_dark --json

# Apply theme to project
python plhub.py style apply <theme_name>
python plhub.py style apply sunset_warm

# Force overwrite existing theme
python plhub.py style apply forest_green --force

# Create new theme
python plhub.py style create "My Theme" --base default_light

# Create with description
python plhub.py style create "Corporate Theme" --base ocean_blue --description "Company branding colors"

# Create and activate
python plhub.py style create "Dark Mode" --base midnight_dark --activate
```

### Widget Commands

```bash
# List all widget templates
python plhub.py widget list

# List as JSON
python plhub.py widget list --json

# Preview widget template
python plhub.py widget preview <template_name>
python plhub.py widget preview button

# Preview as JSON
python plhub.py widget preview card --json

# Generate widget
python plhub.py widget generate <template_name>
python plhub.py widget generate input

# Generate with custom name
python plhub.py widget generate button --name PrimaryButton

# Force overwrite existing files
python plhub.py widget generate modal --name ConfirmModal --force

# Dry run (show what would be created)
python plhub.py widget generate table --name UserTable --dry-run
```

---

## Best Practices

### Theme Selection

1. **Default Light**: Use for most business applications
2. **Midnight Dark**: Use for developer tools or night mode
3. **Ocean Blue**: Use for corporate/professional apps
4. **Sunset Warm**: Use for creative/friendly interfaces
5. **Forest Green**: Use for environmental/wellness apps
6. **High Contrast**: Use for accessibility requirements

### Widget Usage

#### Form Widgets
- Always validate input before processing
- Provide clear error messages
- Use labels for all input fields
- Group related fields together

#### Display Widgets
- Keep button text concise (2-4 words)
- Use cards for grouped content
- Ensure tables have clear headers
- Show progress for long operations

#### Layout Widgets
- Limit navbar items to 5-7 for usability
- Include copyright info in footers
- Use grids for consistent spacing
- Keep stack layouts simple

#### Navigation Widgets
- Default to first tab on load
- Keep accordion sections concise
- Provide clear section labels
- Use icons where appropriate

#### Overlay Widgets
- Use modals sparingly (they block interaction)
- Keep tooltips brief (1-2 sentences)
- Provide dismiss/close options
- Use appropriate alert types

### Customization

#### Creating Custom Themes

1. Start with a base theme similar to your needs
2. Adjust colors for branding
3. Modify typography for readability
4. Test contrast ratios (use WCAG guidelines)
5. Create multiple variations (light/dark)

#### Creating Custom Widgets

1. Copy an existing template as a base
2. Modify the content array
3. Update placeholders ({{widget_title}}, etc.)
4. Test with sample data
5. Add to project templates directory

### Performance Tips

- Load themes once at startup
- Cache widget instances
- Minimize re-rendering
- Use appropriate data structures

### Accessibility

- Always provide text alternatives
- Ensure sufficient color contrast
- Support keyboard navigation
- Test with screen readers
- Use High Contrast theme as reference

---

## Advanced Topics

### Theme Tokens

Tokens are design variables that ensure consistency:

- **Colors**: background, surface, foreground, primary, secondary, accent
- **Status Colors**: error, warning, info, success
- **Typography**: fontFamily, fontSizeBase, headingScale, lineHeight
- **Elevation**: Shadows for layered UI (level0-3)
- **Components**: Per-component styling overrides

### Widget Placeholders

Templates support these placeholders:

- `{{widget_title}}`: Capitalized widget name
- `{{widget_snake}}`: snake_case widget name
- `{{widget_pascal}}`: PascalCase widget name
- `{{widget_kebab}}`: kebab-case widget name

### Project Structure

```
my_project/
├── plhub.json
├── src/
│   └── main.poh
├── ui/
│   ├── styles/
│   │   ├── active_style.json       # Active theme manifest
│   │   └── themes/
│   │       └── my_theme.json      # Custom themes
│   └── widgets/
│       ├── button.poh             # Generated widgets
│       ├── card.poh
│       └── templates/             # Custom templates
│           └── custom.json
└── tests/
```

---

## Troubleshooting

### Theme not applying
- Ensure you're in a project directory (plhub.json exists)
- Check active_style.json was created in ui/styles/
- Verify theme file path is correct

### Widget generation fails
- Ensure template name is correct (use `widget list`)
- Check project has plhub.json
- Use `--force` to overwrite existing files
- Use `--dry-run` to preview before generating

### Customizations not working
- Custom themes go in `ui/styles/themes/`
- Custom templates go in `ui/widgets/templates/`
- Follow JSON structure exactly
- Check for syntax errors in JSON

---

## Examples

See `UI_TOOLKIT_GALLERY.poh` for a comprehensive showcase of all widgets and themes in action!

---

## Support

For issues, questions, or contributions:
- GitHub: https://github.com/AlhaqGH/PLHub
- Issues: https://github.com/AlhaqGH/PLHub/issues

---

**PLHub UI Toolkit** - Version 0.5.0  
© 2025 PohLang Project. MIT License.
