# PohLang Vocabulary (Phrasal Only v0.2)

PohLang uses natural, English-like commands. Each line is a statement. No symbol mode; the entire language is phrasal.

See also:
- Comprehensive guide: [PohLang_Guide.md](../PohLang_Guide.md)
- Syntax reference: [syntax.md](./syntax.md)

## Core Statements

| Intent | Syntax | Notes |
|--------|--------|-------|
| Output text/value | `Write <expression>` | Prints the evaluated expression (legacy: `Say`) |
| Input (string) | `Ask for <name>` | Prompts user; stores input in `<name>` |
| Assignment | `Set <name> to <expression>` | Also accepts `Set <name> <expression>` |
| Increase | `Increase <name> by <number>` | Makes the number bigger (default 1 if omitted) |
| Decrease | `Decrease <name> by <number>` | Makes the number smaller (default 1 if omitted) |
| Conditional (inline) | `If <condition> Write <expr> Otherwise Write <expr>` | Single-line conditional |
| Conditional (block) | `If <condition>` … `[Otherwise …]` `End` | Multi-line with optional `Otherwise` block |
| Repeat (inline) | `Repeat <count> Write <expr>` | `times` keyword optional |
| Repeat (block) | `Repeat <count-or-collection>` … `End` | Number: repeat N times. List/Dict: iterate; implicit `it` inside |
| While (inline) | `While <condition> Write <expr>` | Single-line while form |
| While (block) | `While <condition>` … `End` | Multi-line while loop |
| Make function (inline) | `Make <name> with <params> Write <expr>` | Creates a function that returns the expression |
| Use function | `Use <name> with <args>` | Runs a function |
| Anonymous block | `Begin` (lines...) `End` | Introduces a new lexical scope without control flow |
| Function block | `Make <name> with <params>` ... `Return <expr>` ... `End` | Multi-line function; explicit Return (else returns nothing) |
| Break / Continue | `Stop` / `Skip` | Inside loops: break/continue |
| Import module | `Import "path/to/file.poh"` | Executes another file with circular import detection |
| Debug tracing | `Debug on` / `Debug off` | Toggles rich runtime tracing |
| List ops (mutating) | `Add <value> to <list>`; `Remove <value> from <list>` | Requires a mutable list (see Collections) |
| List ops (index/last) | `Set the <N> item in <list> to <value>`; `Remove the last item from <list>` | 1-based index |
| Dict ops (mutating) | `Add "key": <value> to <dict>`; `Remove "key" from <dict>` | Requires a mutable dictionary |

## Expressions
Numbers (e.g., `5`, `12`), strings (`"Hello"`), booleans (`true`, `false`), `nothing`, identifiers (`age`, `name`).

Arithmetic & logic:
- `+ - * /` with standard precedence (string concat allowed with `+`)
- Comparisons: `is`, `is not`, `is greater than`, `is less than`, `is at least`, `is at most` (normalized to `== != > < >= <=`)
- Logical: `and`, `or`, `not` (normalized to `&& || !`)

Predicates (numeric):
- `x is even`, `x is odd`, `x is positive`, `x is negative`

Random:
- `random between A and B` (integer)
- `random decimal between A and B` (float)
- `random from <collection>` (random element/value)

Collections (construction):
- Immutable list: `Make a list of 1, 2, and 3`
- Mutable list: `Make a mutable list of 1, 2, and 3`
- Immutable dictionary: `Make a dictionary with "a" as 1 and "b" as 2`
- Mutable dictionary: `Make a mutable dictionary with "a" as 1 and "b" as 2`

Collections (access & queries):
- `Take the <N> item from <list>` (1-based)
- `Take the value of <key> from <dict>`
- Postfix `at`: `xs at 2`, `d at "a"` (advanced)
- `keys of <dict>`, `values of <dict>`
- `contains <item> in <collection>`; `Check if <dict> has <key>`

### Built‑In Functions
These are always available (no import needed):

| Name | Forms | Result | Notes |
|------|-------|--------|-------|
| `length(x)` | `length List contains 1,2,3` | Number | Works on strings, lists, dictionaries (count of keys) |
| `sum(list)` | `sum List contains 1,2,3` | Number | Elements must be numeric |
| `min(list)` | `min List contains 4,2,9` | Number | Non‑empty numeric list |
| `max(list)` | `max List contains 4,2,9` | Number | Non‑empty numeric list |
| `range(n)` | `range(5)` | List | `[0,1,2,3,4]` |
| `range(start,end)` | `range(2,5)` | List | `[2,3,4]` (end exclusive) |
| `range(start,end,step)` | `range(0,10,2)` | List | `[0,2,4,6,8]` |
| `join(list, sep)` | `join(nums, "-")` | String | Coerces each element to string; sep optional; default empty |
| `split(text, sep)` | `split("a,b,c", ",")` | List | Does not trim whitespace automatically |
| `now()` | `now()` | String | Current timestamp (ISO 8601, seconds precision) |

Examples:
```
Set nums to range(5)
Write join(nums, ",")            # 0,1,2,3,4
Write length(nums)                # 5
Write split("a|b|c", "|")        # [a, b, c]
Write now()                       # 2025-09-18T12:34:56
```

## Conditions
Boolean connectors and phrase-based comparators:
- Logical: `And`, `Or`, `Not`
- Comparisons: `Equals`, `Not Equals`, `Greater Than`, `Less Than`, `Greater Or Equal`, `Less Or Equal`
- Back-compat verbal forms also work: `is equal to`, `is not equal to`, `is greater than`, `is less than`, `is at least`, `is at most`
- Symbolic `=` inside conditions is treated as equality.

Examples:
```
If age Greater Than 18 And hasID Equals true Write "You may enter"
If age Less Or Equal 12 Or isStudent Equals true Write "Discount"
If Not hasPaid Write "Payment required"
```

## Sugars (Desugaring)
| Sugar | Expansion |
|-------|-----------|
| `Increase x by 2` | `Set x x + 2` |
| `Decrease x by 1` | `Set x x - 1` |
| `Repeat 5 Write "Hi"` | Expand to internal counted loop |

## Collections (Immutable-by-default)
Lists and dictionaries are immutable unless created with the `mutable` keyword.

- Immutable list: `Make a list of 1, 2`
- Mutable list: `Make a mutable list of 1, 2`
- Immutable dictionary: `Make a dictionary with "a" as 1`
- Mutable dictionary: `Make a mutable dictionary with "a" as 1`

Legacy literal expressions are supported temporarily for migration:
- `List contains 1, 2, 3`
- `Dictionary contains "a": 1`

Mutating these legacy values emits a Warning advising to switch to explicit `mutable` forms.

## Design Principles
1. One way per concept (no synonyms like Print/Say/Show).
2. Natural ordering: verb first (`Set`, `Write`, `Repeat`).
3. Punctuation minimized; quotes only for strings.
4. Friendly for reading aloud.

## Example Program
```
Ask for name
Write "Hello " + name
Set count 3
Repeat count Write "Hi"
If count > 1 Write "Many" Otherwise Write "Few"
Make greet with who Write "Hi " + who
Use greet with "Poh"
```

## Error Messages (Updated)
Common enriched errors now include optional line/column:
| Situation | Example |
|-----------|---------|
| Unknown keyword | `[script.poh: Line 1: Col 4] Unknown statement 'Writ 5'. Did you mean 'write'?` |
| Arity mismatch | `[script.poh: Line 7: Col 1] Function 'sumTwo' defined at line 1 expects 2 argument(s) but got 1` |
| Type mismatch | `[script.poh: Line 9: Col 6] Type mismatch: cannot apply '-' to string operand(s)` |
| Undefined variable | `[script.poh: Line 3: Col 7] Undefined variable 'foo'` |
| Division by zero | `[script.poh: Line 5: Col 12] You tried to divide by zero.` |
| Immutable mutation | `[script.poh: Line 4: Col 1] Cannot modify immutable list. Did you mean "Make a mutable list ..."?` |

`Line N:` style messages appear for legacy parse errors where only the line number is known.

## Debug Controls
- Global flag: CLI `--debug` prints rich traces with file/line/col.
- In-script toggles: `Debug on` / `Debug off` statements.

Example:
```
Debug on
Set a to 1
Write a + 2
Debug off
```

Produces (abridged):
```
[example.poh: Line 1: Col 1] Executing: DebugStmt
[example.poh: Line 2: Col 1] Executing: SetStmt
[example.poh: Line 3: Col 1] Executing: WriteStmt
[example.poh: Line 3: Col 1] Evaluating: Identifier 'a' => 1
[example.poh: Line 3: Col 1] Evaluating: Literal => 2
[example.poh: Line 3: Col 1] Evaluating: Binary '+' => 3
3
```

---
This vocabulary will expand cautiously to avoid overwhelming beginners.

### Scoping Recap
Blocks (`If`, `While`, `Repeat`, function bodies, and `Begin`) create new scopes. New names disappear after `End`. Assigning to an existing outer name mutates it. The loop variable `it` only exists inside a `Repeat` body when iterating lists or dictionaries.

### Recipes (See syntax.md for more)
Common patterns:
| Goal | Sketch |
|------|--------|
| Join numbers 0..4 | `Write join(range(5), ",")` |
| Sum evens 0..9 | Use `Repeat range(10)` with `If it is even` accumulate `total` |
| Filter odds | Add `it` to list if `it is odd` |
| Timestamp | `Write now()` |
| Factorial | See recursion example in syntax.md |

---
Cross-links:
- Full guide: [../PohLang_Guide.md](../PohLang_Guide.md)
- Syntax: [./syntax.md](./syntax.md)
