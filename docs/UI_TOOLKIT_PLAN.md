# PLHub UI Toolkit Expansion Plan

## Goals

- Introduce first-class support for styling and theming in PohLang projects.
- Provide a reusable widget/component library that can be scaffolded into PohLang applications.
- Extend PLHub CLI with commands to manage styles and widgets, similar to toolkits like Flutter.
- Update project scaffolding, documentation, and examples to showcase new capabilities.

## Deliverables

1. **Styling System**
   - Global style manifest (`ui/styles/active_style.json`).
   - Prebuilt themes shipped with PLHub (`PLHub/styles/`).
   - CLI support: `plhub style list|apply|create|show`.
   - Project scaffolding generates default theme and style README.

2. **Widget Library**
   - Widget templates stored in `PLHub/widgets/templates/`.
   - CLI support: `plhub widget list|generate|preview`.
   - Project scaffolding creates `ui/widgets/` folder with sample widgets.
   - Example widget definitions (Button, Card, Layout, Form).

3. **Documentation & Examples**
   - New guide `PLHUB_UI_TOOLKIT.md`.
   - Quick reference updates for style/widget commands.
   - Example project `Examples/ui_showcase/` demonstrating styles & widgets.

4. **Integration**
   - Update `create_project` to generate UI folder structure.
   - Ensure `test` and `build` commands respect new directories.
   - Add optional flag `--with-ui` (defaults to true) for scaffolding.

## Timeline / Task Breakdown

1. Audit current editor/tooling (completed).
2. Implement CLI commands and supporting modules.
3. Ship default style and widget assets.
4. Update scaffolding + templates + docs.
5. Create showcase example and run regression tests.

## Assumptions

- Styles and widgets are manifest-driven (JSON and PohLang templates) without modifying Rust runtime.
- CLI commands operate on file templates; actual rendering remains up to transpilers/interpreters.
- Future work may integrate with VS Code extension for live previews.

## Open Questions (Future Work)

- Live preview support in editors.
- Integration with transpilers (e.g., Dart) to emit styled UI.
- Synchronization with upcoming LSP features.
