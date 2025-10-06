# Known Issues - PohLang v0.5.0 Official Release

## Parser Issue with Multi-line If Statements

**Status**: Known issue in PohLang v0.5.0 official release  
**Severity**: High  
**Impact**: Multi-line If statements with phrasal comparisons fail to parse

### Problem Description

The PohLang v0.5.0 official runtime (pohlang-v0.5.0-windows-x64.zip) has a parser issue with multi-line If statements using phrasal comparison operators.

### Affected Syntax

```poh
# This FAILS to parse:
If temperature is greater than 20
    Write "Warm"
Otherwise
    Write "Cool"
End If
```

**Error Message**:
```
Error: Could not parse expression: greater than 20.
Hint: Check for unmatched brackets [], braces {}, or parentheses ()
```

### What Works

1. **Phrasal Built-in Expressions** - ✅ WORK PERFECTLY
   ```poh
   Set sum to total of [1, 2, 3]          # ✅ Works
   Set max to largest in numbers           # ✅ Works
   Set upper to make uppercase "hello"     # ✅ Works
   ```

2. **Inline If Statements** - ✅ WORK
   ```poh
   If 5 is greater than 3 Write "Yes" Otherwise Write "No"  # ✅ Works
   ```

3. **All Other Features** - ✅ WORK
   - Variables, functions, collections
   - All 20 phrasal built-in expressions
   - Arithmetic operations
   - String concatenation
   - Loops (While, Repeat)

### Workaround

**Option 1**: Use inline If statements
```poh
If temperature is greater than 20 Write "Warm" Otherwise Write "Cool"
```

**Option 2**: Use symbol syntax (if supported in runtime)
```poh
If temperature > 20
    Write "Warm"
Otherwise
    Write "Cool"
End If
```

**Option 3**: Use intermediate variables
```poh
Set is_warm to temperature is greater than 20
If is_warm
    Write "Warm"
Otherwise
    Write "Cool"
End If
```

### Verification

Tested with:
- **Runtime**: pohlang.exe v0.5.0 from official release
- **Source**: https://github.com/AlhaqGH/PohLang/releases/download/v0.5.0/pohlang-v0.5.0-windows-x64.zip
- **Date**: October 5, 2025

Working examples from official release:
- ✅ `examples/poh/hello.poh` - Basic output
- ✅ `examples/poh/math_functions.poh` - All phrasal math expressions
- ✅ `examples/poh/collections_phrasal.poh` - Phrasal collection operations
- ❌ `examples/poh/if_block_greeting.poh` - Multi-line If with comparison
- ❌ `examples/poh/phrase_age_check.poh` - Multi-line If with comparison

### Impact on PLHub Templates

PLHub v0.5.0 templates include multi-line If statements with phrasal comparisons which will fail with the official v0.5.0 runtime.

**Affected Templates**:
- Basic template (`examples/example.poh`)
- Other templates with conditional logic

### Recommendation

**For Users**:
1. Use inline If statements for now
2. Wait for runtime patch release
3. Use locally built runtime with fix (if available)

**For PLHub**:
1. Update templates to use inline If statements
2. Add note about known issue
3. Test with next runtime release

### Status Updates

- **2025-10-05**: Issue identified in official v0.5.0 release
- **Tracking**: Will be fixed in next PohLang release
- **Workarounds**: Documented above

### Related

- PohLang Repository: https://github.com/AlhaqGH/PohLang
- Official Release: v0.5.0
- PLHub Version: v0.5.0

---

**Note**: This is a runtime parser issue, not a PLHub issue. All PLHub commands work correctly. The phrasal built-in expressions (all 20 of them) work perfectly. Only multi-line If statements with phrasal comparisons are affected.
