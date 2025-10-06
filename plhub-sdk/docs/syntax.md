# PohLang Syntax (v0.1 Draft)

This document describes the phrasal grammar for the early prototype. It is a work in progress and subject to change. This document is not exhaustive but covers the core features. It is intended for developers and advanced users. It is a living document and will be updated as the language evolves. This document is a draft and may contain inaccuracies or omissions. For the latest updates, refer to the official repository. This document is a companion to the PohLang interpreter.

## High-Level Concepts
# PohLang Syntax (Phrasal v0.1)

This version defines ONLY the phrasal/English-like grammar. Symbol mode has been removed to keep the language focused and approachable.

## High-Level Concepts
- A program is a sequence of statements (one per line).
- Each statement starts with a verb-like keyword: Write / Ask / Set / Increase / Decrease / If / Repeat / Make / Use.
- Functions support both single-line (inline) and multi-line block forms with parameters and returns.

## Scoping Rules (Current)
PohLang uses lexical (static) scoping with block boundaries introduced by control structures (`If`, `While`, `Repeat`, function bodies) and explicit anonymous blocks using `Begin ... End`.

Rules:
1. Variables are created on first assignment (`Set`) in the current block scope.
2. An assignment to an existing variable name updates the nearest enclosing scope that already defines it (no implicit shadowing).
3. A name defined inside an `If`/`While`/`Repeat`/`Begin` block is not visible after the corresponding `End` unless it already existed outside (then it is a mutation instead of a new definition).
4. Loop iteration helper `it` (for `Repeat <list>` or `Repeat <dictionary>`) exists only inside each iteration body.
5. Function parameters live in their own function scope; blocks inside a function can define new locals that disappear when the block ends, while mutations to existing variables (including parameters) persist for the rest of the function.
6. Returning from inside a nested block immediately unwinds to the caller.
7. New variables created inside a block (`If`/`While`/`Repeat`/`Begin`) are confined to that block and do not leak outside.

### Function Scoping Specifics
- Parameters shadow outer variables with the same name.
- New names created via `Set` inside a function become function-locals unless they already exist in an outer scope.
- Inner blocks do not leak their fresh variables to the function body (true lexical block scoping).
- Recursion is supported; each call gets a fresh function environment.

### Anonymous Blocks
Use `Begin ... End` to introduce a new scope without control flow:
```
Set x to 1
Begin
	Set y to 2
	Set x to x + y   # mutates outer x
End
Write x    # 3
Write y    # error: y is not defined here
```

Nested `Begin` blocks behave exactly like nested `If` blocks with respect to scoping.

## Grammar (Current Subset)
Program          ::= { Statement NEWLINE }
Statement        ::= WriteStmt | AskStmt | SetStmt | IncStmt | DecStmt | IfInline | WhileInline | RepeatInline | FuncInline | CallStmt

WriteStmt        ::= 'Write' Expression
AskStmt          ::= 'Ask for' IDENT
SetStmt          ::= 'Set' IDENT 'to' Expression | 'Set' IDENT Expression
IncStmt          ::= 'Increase' IDENT 'by' NUMBER | 'Increase' IDENT NUMBER
DecStmt          ::= 'Decrease' IDENT 'by' NUMBER | 'Decrease' IDENT NUMBER
IfInline         ::= 'If' Condition 'Write' Expression 'Otherwise' 'Write' Expression
WhileInline      ::= 'While' Condition 'Write' Expression
RepeatInline     ::= 'Repeat' (NUMBER|IDENT) 'times' 'Write' Expression | 'Repeat' (NUMBER|IDENT) 'Write' Expression
FuncInline       ::= 'Make' IDENT 'with' ParamList 'Write' Expression  # inline form (implicit Return)
FuncBlock        ::= 'Make' IDENT 'with' ParamList NEWLINE { Statement | ReturnStmt } 'End'
ReturnStmt       ::= 'Return' [ Expression ]
CallStmt         ::= 'Use' IDENT 'with' ArgList

ParamList        ::= IDENT { ',' IDENT } | /* empty */
ArgList          ::= Expression { ',' Expression } | /* empty */

Condition        ::= BoolExpr
BoolExpr         ::= BoolExpr ' Or ' BoolExpr | BoolExpr ' And ' BoolExpr | 'Not ' BoolExpr | CompareExpr
CompareExpr      ::= Expression CompareOp Expression | Expression '=' Expression
CompareOp        ::= 'Greater Or Equal' | 'Less Or Equal' | 'Equals' | 'Not Equals' | 'Greater Than' | 'Less Than'

Expression       ::= Term { ('+' | '-') Term }
Term             ::= Factor { ('*' | '/') Factor }          // * and / may not yet be parsed in implementation
Factor           ::= NUMBER | STRING | IDENT | '(' Expression ')'

## Functions

### Inline Function
```
Make greet with name Write "Hello, " + name
Write greet("World")   # Hello, World
```

### Block Function
```
Make add with a, b
	Set total to a + b
	Return total
End
Write add(3,4)   # 7
```

### Recursive Function
```
Make fact with n
	If n is 0
		Return 1
	End
	Return n * fact(n - 1)
End
Write fact(5)   # 120
```

Arity must match exactly; a mismatch raises a runtime error.

## Built-In Functions
The interpreter ships with a small standard library of pure helpers:

| Name | Forms | Result | Notes |
|------|-------|--------|-------|
| `length(x)` | `length List contains 1,2,3` | Number | Works on strings, lists, dictionaries |
| `sum(list)` | `sum List contains 1,2,3` | Number | Elements must be numeric |
| `min(list)` | `min List contains 4,2,9` | Number | Non-empty numeric list |
| `max(list)` | `max List contains 4,2,9` | Number | Non-empty numeric list |
| `range(n)` | `range(5)` | List | 0..n-1 |
| `range(start,end)` | `range(2,5)` | List | start..end-1 |
| `range(start,end,step)` | `range(0,10,2)` | List | step progression (no zero step) |
| `join(list, sep)` | `join(nums, ":")` | String | Coerces elements; sep optional (default "") |
| `split(text, sep)` | `split("a,b,c", ",")` | List | Simple separator split |
| `now()` | `now()` | String | ISO-8601 timestamp |

Example:
```
Set nums to range(5)
Write join(nums, ",")    # 0,1,2,3,4
Write length(nums)        # 5
Write now()
```

## Collections: Immutable-by-default (new)

Lists and dictionaries default to immutable values. Use the keyword "mutable" when you need in-place updates.

- Immutable list literal: `Make a list of 1, 2, and 3` → a fixed tuple (cannot be modified)
- Mutable list literal: `Make a mutable list of 1, 2, and 3` → can be changed with Add/Remove/Set Nth/Remove last

- Immutable dictionary literal: `Make a dictionary with "a" as 1 and "b" as 2` → a frozen dictionary (cannot be modified)
- Mutable dictionary literal: `Make a mutable dictionary with "a" as 1 and "b" as 2` → can be changed with Add/Remove

Legacy literal expressions remain supported for a transition period:

- `List contains 1, 2, 3`
- `Dictionary contains "a": 1, "b": 2`

Behavior for legacy literals:
- They evaluate to special wrapper values that allow mutation, but the first mutation will emit a Warning:
	`[file.poh: Line N: Col M] Warning: Implicit mutable list/dictionary is deprecated. Use 'mutable list/dictionary' instead.`
- Please migrate to the new explicit forms.

Mutation on immutable collections raises a clear runtime error with location info, for example:
`[script.poh: Line 4: Col 1] Cannot modify immutable list. Did you mean "Make a mutable list ..."?`

Common operations affected:
- Lists: `Add X to xs`, `Remove X from xs`, `Set the N item in xs to V`, `Remove the last item from xs`
- Dictionaries: `Add "k": v to d`, `Remove "k" from d`

Non-mutating reads like `Take the 2 item from xs`, `Take the value of "a" from d`, `keys of d`, `values of d`, and `length(xs)` work for both immutable and mutable collections.

### Misuse Examples (Runtime Errors)
These demonstrate error conditions the runtime reports:

| Code | Error (summary) | Reason |
|------|------------------|--------|
| `range(1,5,0)` | "range expects 1 to 3 arguments" or infinite-step prevention (future explicit check) | Zero step unsupported |
| `join(5, ",")` | "join expects a list" | First arg must be list/tuple |
| `sum List contains 1,"a"` | "sum expects numeric values" | Non-numeric in numeric fold |
| `min List contains` | parse error | Empty literal / syntax issue |
| `split("abc", "")` | Valid (returns every char) | Edge but allowed |

Future improvement: specific message for zero step in `range`.

## Recipes
Practical multi-line idioms using existing primitives.

### Join Numbers 1..N
```
Set out to ""
Repeat range(1,6)
	Set out to out + it + ","
End
Write out
```

### Sum Only Even Numbers 0..9
```
Set total to 0
Repeat range(10)
	If it is even
		Set total to total + it
	End
End
Write total   # 20
```

### Filter (Collect) Odd Numbers
```
Set odds to List contains
Repeat range(10)
	If it is odd
		Add it to odds
	End
End
Write odds
```

### Timestamped Log Line
```
Write "Started at " + now()
```

### Split, Transform, Rejoin
```
Set parts to split("a-b-c", "-")
Repeat parts
	Set it to it + it   # (planned: future map sugar)
End
Write join(parts, ":")
```

### Factorial (Recursion Recipe)
```
Make fact with n
	If n is 0
		Return 1
	End
	Return n * fact(n - 1)
End
Write fact(6)  # 720
```

### Helper Function For Filtering
```
Set evens to List contains
Make pushIfEven with n
	If n is even
		Add n to evens
	End
	Return nothing
End
Repeat range(10)
	Use pushIfEven with it
End
Write evens
```

## Desugaring
Increase X by N => Set X X + N (make number bigger)
Decrease X by N => Set X X - N (make number smaller)
Repeat N Write E => internal counted loop => for i in [0..N)
Make f with a,b Write E => create a function returning E

## Planned (Not Implemented Yet)
- Multi-line If / Repeat blocks:
	If age > 18
		Write "Adult"
		Otherwise
		Write "Minor"
- Parentheses for grouping in boolean expressions.
- Data structures: lists, dictionaries.
- Random numbers, predicates (is even, etc.).

## Error Strategy (Planned)
- Unrecognized keyword suggestion (edit distance).
- Provide line/column in messages.
- Show expected pattern after failing a statement parse.

## Error Reporting (Updated)
PohLang now emits enriched parse and runtime errors with positional metadata when available.

Formats:
- Parse errors (with file + column): `[file.poh: Line 12: Col 7] Unknown statement 'Writ'. Did you mean 'write'?`
- Parse errors (legacy line-only): `Line 5: If block not closed with End/End If` (used when only line known)
- Runtime errors (function arity): `[script.poh: Line 3: Col 1] Function 'add' defined at line 1 expects 2 argument(s) but got 1`
- Type mismatch (numeric ops): `[script.poh: Line 8: Col 5] Type mismatch: cannot apply '-' to string operand(s)`
- Division by zero: `[calc.poh: Line 4: Col 10] You tried to divide by zero.`

Column Tracking:
The parser tracks the first non-whitespace column for statement keywords and token start columns inside expressions. Runtime errors now uniformly show `Line` / `Col` when originating node metadata is available.

## Debug Mode
Run with `--debug` (Python CLI) to enable execution tracing:
```
python -m Interpreter.cli program.poh --debug
```
Output includes lines like:
```
[script.poh: Line 3: Col 1] Executing: WriteStmt
[script.poh: Line 3: Col 1] Evaluating: Literal => 5
```
Use `Debug on` / `Debug off` statements inside a script to toggle at runtime.

## Imports
Use `Import "<path>.poh"` to execute another PohLang file.
- Paths are resolved relative to the current script's directory.
- Each imported file runs in its own module scope; its variables are exported via `modules` registry and can be injected into importer module scope.
- Functions defined in imports are available globally after import.
- Imports are cached (idempotent); the same file won't run twice.
- Circular imports are detected and reported as:
	`[script.poh: Line N: Col M] Error: Circular import detected with other.poh. Chain: <a -> b -> ...>`

CLI runs the main file and its imports:
```
python -m Interpreter.cli path\to\main.poh
```

Example session snippet:
```
Debug on
Set x to 5
Write x + 1
Debug off
```

Produces (abridged trace):
```
[example.poh: Line 1: Col 1] Executing: DebugStmt
[example.poh: Line 2: Col 1] Executing: SetStmt
[example.poh: Line 2: Col 1] Evaluating: Literal => 5
[example.poh: Line 2: Col 1] Set variable 'x' = 5
[example.poh: Line 3: Col 1] Executing: WriteStmt
[example.poh: Line 3: Col 1] Evaluating: Identifier 'x' => 5
[example.poh: Line 3: Col 1] Evaluating: Literal => 1
[example.poh: Line 3: Col 1] Evaluating: Binary '+' => 6
6
[example.poh: Line 4: Col 1] Executing: DebugStmt
```

Trace message forms:
- Statement execution: `[file: Line N: Col M] Executing: <StmtType>`
- Expression evaluation: `[file: Line N: Col M] Evaluating: <Kind> => <value>`
- Variable set/update: `[file: Line N: Col M] Set variable 'name' = <repr>`
- Function entry: `[file: Line N: Col M] Enter function fname(a=1, b=2)`
- Function return: `[file: Line N: Col M] Return <repr>`
- Import: `[import: otherfile.poh]`

Normal (non-debug) runs output only program results (e.g., Write statements) with no trace noise.

Example session snippet:
```
Debug on
Set x to 5
Write x + 1
Debug off
```

---
The syntax will evolve carefully; simplicity and readability take priority over feature breadth.
- Comparison chaining.
- Predicates (is even, etc.).

