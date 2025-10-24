# Extension Separation Guide

## Overview

PohLang now uses **two separate VS Code extensions** to avoid conflicts and provide clean separation of concerns:

### 1. PohLang Language Support Extension
**Location**: `C:\Users\habib\POHLANG\PohLang-VS_code_extention\`  
**Package ID**: `pohlang`  
**Purpose**: Core language support and IDE features

**Provides**:
- ✅ Language definition (`.poh` file association)
- ✅ Syntax highlighting (TextMate grammar)
- ✅ Code snippets
- ✅ Language configuration (brackets, comments, etc.)
- ✅ IntelliSense suggestions
- ✅ Basic language features

**Does NOT Provide**:
- ❌ Runtime execution
- ❌ SDK management
- ❌ Project management commands

---

### 2. PLHub Extension
**Location**: `C:\Users\habib\POHLANG\PLHub\Editor\`  
**Package ID**: `plhub`  
**Purpose**: SDK integration and development tools

**Provides**:
- ✅ Runtime execution commands (`PLHub.runFile`, etc.)
- ✅ Project creation and management
- ✅ SDK version management and auto-updates
- ✅ Environment example runner
- ✅ GitHub integration for SDK downloads
- ✅ Configuration settings for SDK repos

**Does NOT Provide**:
- ❌ Language definition
- ❌ Syntax highlighting
- ❌ Code snippets
- ❌ Language grammar

---

## Why Two Extensions?

### Problem
When both extensions provided language support features, VS Code would:
- Register duplicate language definitions
- Create conflicting grammars
- Cause crashes or deactivate extensions
- Show errors about duplicate contributions

### Solution
**Separation of Concerns**:
- **Language Extension**: "What is PohLang?" (syntax, structure, highlighting)
- **PLHub Extension**: "How do I run PohLang?" (execution, tools, SDK)

This follows VS Code best practices where language support and tooling are separate concerns.

---

## Installation Order

Users should install **both** extensions:

1. **Install PohLang Language Support** (required first)
   - Provides basic language recognition
   - Enables syntax highlighting
   - Adds code snippets

2. **Install PLHub** (optional but recommended)
   - Adds runtime execution
   - Enables project management
   - Provides SDK tools

---

## Extension Dependencies

The PLHub extension's `package.json` now includes a note:
```json
"description": "PohLang v0.5.4 SDK development environment with project management, package tools, and runtime integration (requires PohLang Language Support extension)"
```

Consider adding an `extensionDependencies` field in future versions:
```json
"extensionDependencies": [
  "pohlang.pohlang"
]
```

---

## Key Changes Made (October 12, 2025)

### PLHub Extension Cleanup

**Removed from `package.json`**:
```json
// REMOVED: Language definition
"languages": [{ "id": "pohlang", ... }]

// REMOVED: Grammar
"grammars": [{ "language": "pohlang", ... }]

// REMOVED: Snippets
"snippets": [{ "language": "pohlang", ... }]
```

**Updated**:
- `name`: `"PLHub"` → `"plhub"` (npm convention)
- `categories`: Removed `"Programming Languages"` and `"Snippets"`
- `description`: Added note about language extension dependency

**Kept**:
- All commands (`PLHub.runFile`, etc.)
- All keybindings (`Ctrl+F5`)
- All menus and context menus
- All configuration settings
- Activation event `onLanguage:pohlang` (to activate when .poh files open)

---

## Testing the Separation

### Test 1: Install Only Language Extension
**Expected**:
- ✅ `.poh` files have syntax highlighting
- ✅ Snippets work
- ❌ No "PL-Hub: Run File" command
- ❌ No Ctrl+F5 keybinding

### Test 2: Install Only PLHub
**Expected**:
- ❌ `.poh` files show as plain text
- ✅ Commands available in palette
- ✅ Ctrl+F5 works (but no highlighting)

### Test 3: Install Both Extensions
**Expected**:
- ✅ `.poh` files have syntax highlighting
- ✅ Snippets work
- ✅ "PL-Hub: Run File" command available
- ✅ Ctrl+F5 runs file
- ✅ NO conflicts or crashes

---

## Future Considerations

### Extension Pack (Optional)
Create a third "extension pack" that bundles both:

**`pohlang-extension-pack`**:
```json
{
  "extensionPack": [
    "pohlang.pohlang",
    "pohlang.plhub"
  ]
}
```

This allows users to install everything with one click.

### Publisher Naming
Consider using consistent publisher names:
- `pohlang.pohlang-language`
- `pohlang.plhub`
- `pohlang.pohlang-pack`

---

## Maintenance Notes

### When to Update Each Extension

**PohLang Language Extension**:
- New language features (syntax changes)
- Grammar updates
- New snippets
- Language configuration changes
- IntelliSense improvements

**PLHub Extension**:
- New SDK features
- Command additions
- Runtime improvements
- Configuration options
- GitHub integration updates

---

## Verification Checklist

Before publishing updates:

**PLHub Extension** (`PLHub\Editor\package.json`):
- [ ] NO `languages` contribution
- [ ] NO `grammars` contribution  
- [ ] NO `snippets` contribution
- [ ] Has all SDK commands
- [ ] Has keybindings and menus
- [ ] Description mentions language extension dependency

**PohLang Language Extension** (`PohLang-VS_code_extention\package.json`):
- [ ] Has `languages` contribution
- [ ] Has `grammars` contribution
- [ ] Has `snippets` contribution
- [ ] NO SDK management commands
- [ ] Focuses on language features only

---

## Quick Reference

| Feature | Language Extension | PLHub Extension |
|---------|-------------------|-----------------|
| Syntax Highlighting | ✅ | ❌ |
| Snippets | ✅ | ❌ |
| Language Definition | ✅ | ❌ |
| Run File Command | ❌ | ✅ |
| SDK Management | ❌ | ✅ |
| Project Creation | ❌ | ✅ |
| GitHub Integration | ❌ | ✅ |
| Configuration | ❌ | ✅ |

---

**Status**: Separation complete as of October 12, 2025  
**Next Step**: Test both extensions together to verify no conflicts
