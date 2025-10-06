# PLHub Widget Templates

PLHub ships with reusable widget templates you can scaffold into any project using the CLI.

```bash
python plhub.py widget list
python plhub.py widget preview card
python plhub.py widget generate button --name PrimaryButton
```

Templates live inside `PLHub/widgets/templates/` as JSON descriptors. Each template may define one
or more files and leverages simple placeholders like `{{widget_snake}}` or `{{widget_pascal}}` to
match your chosen widget name during generation.

Project-specific templates can be added under `ui/widgets/templates/` inside your project directory.
They are discovered automatically by the CLI alongside the built-in set.
