# PohLang Roadmap

PohLang is a tiny, fully phrasal English-like programming language that transpiles to Dart.  
This roadmap describes the path from experimental package → professional language.

---

## 0.0.x Series (Experimental)
✅ Core transpiler  
✅ Basic syntax (`Ask`, `Write`, `Set`, `Repeat`, `If/Otherwise`, `Make`, `Use`)  
✅ Docs: `syntax.md`, `vocabulary.md`  
✅ Examples folder

---

## 0.1.x — Tooling
- [ ] Create a CLI tool (`poh`) for running and transpiling
  - `poh run <name>.poh`
  - `poh transpile <name>.poh -o <name>.dart`
- [ ] Provide simple installation guide for CLI
- [ ] Add first tests for parser + transpiler
## or improve the current running method to be professional:


## 0.2.x — Developer Experience
- [ ] Improve error messages with line/column hints  
- [ ] Add comments support (`# comment`)  
- [ ] Write **tutorials** (`docs/tutorials/`)  
- [ ] Add CHANGELOG.md and CONTRIBUTING.md

---

## 0.3.x — Ecosystem
- [ ] VS Code extension:
  - Syntax highlighting  
  - Snippets for common phrases  
- [ ] GitHub repo website / landing page (pohlang.dev)  
- [ ] Playground (run PohLang in browser, compiled to Dart2JS)

---

## 0.4.x — Language Features
- [ ] Variables: reassignments, scoped variables  
- [ ] Functions with multiple params  
- [ ] Imports: `Use from other_file.poh`  
- [ ] Expanded vocabulary (loops, lists, maps)

---

## 0.5.x — Interoperability
- [ ] Allow calling Dart functions directly  
- [ ] Basic FFI-style integration with Dart libraries  
- [ ] Export transpiled Dart as a usable package

---

## 1.0.0 — Stable Release
- [ ] Freeze **syntax.md** and **vocabulary.md** as the official spec  
- [ ] Pass full test suite  
- [ ] Semantic versioning enforced  
- [ ] Publish docs website + tutorials  
- [ ] Guarantee backward compatibility for all 1.x releases  

---

## Long-Term Ideas
- Transpile to JavaScript and/or WASM  
- Support modules/packages written in PohLang  
- Extend VS Code extension with inline transpilation  
- Explore educational use cases (teach coding via English phrases)

---

## Contributing
We welcome suggestions for new **phrases**, **syntax improvements**, and **tooling support**.  
Please check `syntax.md` and `vocabulary.md` before proposing changes.
