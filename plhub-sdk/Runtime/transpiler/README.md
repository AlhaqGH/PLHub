# PohLang

A beginner-focused, fully phrasal (English-like) language that transpiles to Dart. The canonical form is phrasal—prefer words over symbols for clarity.

## Goals
- Use plain-language statements: `Write "Hello"`, `Set count 5`, `Repeat count Write "Hi"`.
- Keep one clear form per concept (no synonyms like Print/Show). Use `Write`, not `Say/Print`.
- Provide a gentle path to programming concepts (variables, loops, conditionals, functions) without punctuation noise.
- Output readable Dart so learners can transition later.

## Example
```
Ask for name
Ask for age number
If age is greater than 1
	Write "Many"
Otherwise
	Write "Few"
End
Make greet with who Write "Hi " plus who
Use greet with "Poh"
```

## Running a Program
1. Ensure Dart SDK is installed.
2. Place a `.poh` file in the project root or `examples/`.
3. Transpile:
```
dart run src/transpiler.dart examples/phrase_repeat.poh
```
4. Run the generated Dart file (same basename with `.dart`).
```
dart run examples/phrase_repeat.dart
```

### CLI (bin/) usage

Once in this repo:

```
dart run bin/pohlang.dart examples/phrase_repeat.poh
```

Flags:
- `--no-run` — only transpile, don't execute the generated Dart
- `--compile` — compile the generated Dart to a native executable and run it (Windows: .exe)
- `--strict-phrases` — warn when symbol operators (+, -, *, /) are used; suggests using words (plus/minus/times/divided by)
- `-o <file.dart>` — write output to a custom path

You can also run with tasks in VS Code: use the Command Palette → Run Task → "Transpile + Run (invoice example)".

### Package & publish

Current version: `0.0.3`.
To dry-run a publish:

```
dart pub publish --dry-run
```

To run analyzer and format:

```
dart analyze
dart format .
```

### Install from pub.dev

Once published, users can install globally:

```
dart pub global activate pohlang
```

Run a program:

```
pohlang path/to/program.poh
```

Notes:
- You can add comments with `#`. Everything after `#` on a line is ignored.
- Parser errors include line numbers, for example: `Line 2: After 'Otherwise' you must add 'Write <expression>'`.
- Multi-line blocks supported: If/Otherwise/End (also End If) and While/End (also End While).
- Multi-file apps supported via `Import "path/to/file.poh"`.
- Numeric input: `Ask for <name> number`; decimals: `Ask for <name> decimal`.
- Loop control: `Stop` (break) and `Skip` (continue) inside `Repeat`/`While`.
- Special literal: `nothing` represents no value (null).

Strict phrasal mode example:

Input (with symbols):

```
Set r to 1 + 2 * 3
```

Warnings with `--strict-phrases`:

```
Strict phrasal: examples/math.poh:1: Avoid symbolic operator "+"; use words (plus/minus/times/divided by).
```

## Current Features
- Write, Ask for (string/number/decimal), Set, Increase, Decrease
- Conditionals: Inline and block If/Otherwise/End (End If also accepted)
- Loops: Inline Repeat, block While/End (End While also accepted)
- Loop control: Stop (break), Skip (continue)
- Functions: Inline and block (block definitions emitted as Dart functions)
- Expressions: phrasal operators (plus, minus, times, divided by) with proper precedence
- Conditions: phrasal comparisons (is, is not, is greater than/less than, is at least/at most), and/or/not
- Special literal: nothing (null)
- Import other .poh files (inlined before run)
- Compile to native executable with `--compile`
- Optional lint: `--strict-phrases` warns on +, -, *, /

## Roadmap
- Nested blocks (If inside While, etc.)
- Lists, dictionaries, predicates (is even, etc.)
- Parentheses for complex boolean expressions
- Random numbers, timers, date utilities
- More diagnostics and suggestions
- Optional extensions: Islamic-friendly helpers (prayer times, Hijri date, Quran recitation)
- Flutter integration examples

## Directory Structure
```
src/       Core transpiler sources
example/   Sample PohLang programs
doc/       Vocabulary & syntax references
lib/       Future runtime helpers / extensions
python/    Pure-Python AST, parser, interpreter, and tests
```
```
transpiler/src/     Core transpiler sources (Dart)
transpiler/bin/     CLI entrypoint (pohlang.dart)
lib/                Unified public Dart library (runtime exports)
example/            Root Dart examples using package:pohlang
Interpreter/        Python interpreter package (installed as 'pohlang')
doc/                Vocabulary & syntax references
```

### Run with the Python interpreter (optional)

There’s a pure-Python interpreter for PohLang under `python/` for environments without Dart:

```
python -m python.run_poh python/examples/hello.poh
```

Tests for the Dart transpiler E2E are also provided using `pytest` under `python/tests` and shell out to `dart` to validate generated output.

## Contributing
Open to experiments—keep syntax consistent and simple. Avoid adding multiple ways to express the same idea unless it aids learning progression.

## License
MIT © 2025 Habiburrahman Mukhlis — see LICENSE for details.
