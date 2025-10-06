"""Widget templating utilities for PLHub UI toolkit."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple
import json
import re


@dataclass(slots=True)
class WidgetFileSpec:
    """Definition of a single file emitted by a widget template."""

    path: str
    content: str
    description: Optional[str]
    overwrite: bool


@dataclass(slots=True)
class WidgetTemplate:
    """Metadata and file definitions for a widget template."""

    key: str
    name: str
    description: Optional[str]
    category: Optional[str]
    tags: Sequence[str]
    source: str
    path: Path
    files: Sequence[WidgetFileSpec]
    preview: Optional[str]


class WidgetManager:
    """Helper for discovering and instantiating widget templates."""

    BUILTIN_DIR = Path("widgets") / "templates"
    PROJECT_WIDGETS_DIR = Path("ui") / "widgets"
    PROJECT_TEMPLATES_DIR = PROJECT_WIDGETS_DIR / "templates"
    README_NAME = "README.md"

    def __init__(self, plhub_root: Path, project_root: Optional[Path] = None) -> None:
        self.plhub_root = plhub_root
        self.project_root = project_root
        self.builtin_dir = plhub_root / self.BUILTIN_DIR
        self.project_widgets_dir = (
            project_root / self.PROJECT_WIDGETS_DIR if project_root else None
        )
        self.project_templates_dir = (
            project_root / self.PROJECT_TEMPLATES_DIR if project_root else None
        )

        self._builtin_templates: Dict[str, WidgetTemplate] = self._load_templates(
            self.builtin_dir, source="builtin"
        )
        self._project_templates: Dict[str, WidgetTemplate] = (
            self._load_templates(self.project_templates_dir, source="project")
            if self.project_templates_dir
            else {}
        )
        self._templates: Dict[str, WidgetTemplate] = {
            **self._builtin_templates,
            **self._project_templates,
        }
        self._aliases: Dict[str, str] = {}
        self._register_aliases(self._builtin_templates.values())
        self._register_aliases(self._project_templates.values())

    # ------------------------------------------------------------------
    # Template discovery helpers
    # ------------------------------------------------------------------
    @staticmethod
    def slugify(value: str) -> str:
        cleaned: List[str] = []
        for ch in value.strip().lower():
            if ch.isalnum():
                cleaned.append(ch)
            elif ch in {" ", "-", "_", "."}:
                cleaned.append("_")
        slug = "".join(cleaned)
        while "__" in slug:
            slug = slug.replace("__", "_")
        return slug.strip("_") or "widget"

    @staticmethod
    def _normalize(value: str) -> str:
        value = value.strip()
        if value.lower().endswith(".json"):
            value = value[:-5]
        return WidgetManager.slugify(value)

    def _register_aliases(self, templates: Iterable[WidgetTemplate]) -> None:
        for template in templates:
            key = template.key
            self._aliases[key] = key
            self._aliases[self._normalize(template.name)] = key
            self._aliases[self._normalize(template.path.stem)] = key
            self._aliases[self._normalize(template.path.name)] = key

    def _load_templates(
        self, directory: Optional[Path], *, source: str
    ) -> Dict[str, WidgetTemplate]:
        results: Dict[str, WidgetTemplate] = {}
        if not directory or not directory.exists():
            return results
        for json_path in sorted(directory.glob("*.json")):
            template = self._parse_template(json_path, source)
            if template:
                results[template.key] = template
        return results

    def _parse_template(
        self, json_path: Path, source: str
    ) -> Optional[WidgetTemplate]:
        try:
            raw = json.loads(json_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None

        key = raw.get("key") or self.slugify(json_path.stem)
        name = raw.get("name") or json_path.stem.replace("_", " ").title()
        description = raw.get("description")
        category = raw.get("category")
        tags = tuple(raw.get("tags", []))

        files: List[WidgetFileSpec] = []
        for file_def in raw.get("files", []):
            content = file_def.get("content", "")
            if isinstance(content, list):
                content_str = "\n".join(str(line) for line in content).rstrip() + "\n"
            else:
                content_str = str(content)
                if not content_str.endswith("\n"):
                    content_str += "\n"
            files.append(
                WidgetFileSpec(
                    path=str(file_def.get("path")),
                    content=content_str,
                    description=file_def.get("description"),
                    overwrite=bool(file_def.get("overwrite", False)),
                )
            )

        preview_lines = raw.get("preview")
        preview: Optional[str]
        if isinstance(preview_lines, list):
            preview = "\n".join(str(line) for line in preview_lines)
        elif isinstance(preview_lines, str):
            preview = preview_lines
        else:
            preview = None

        return WidgetTemplate(
            key=self.slugify(key),
            name=name,
            description=description,
            category=category,
            tags=tags,
            source=source,
            path=json_path,
            files=tuple(files),
            preview=preview,
        )

    # ------------------------------------------------------------------
    # Public accessors
    # ------------------------------------------------------------------
    def builtin_templates(self) -> List[WidgetTemplate]:
        return sorted(self._builtin_templates.values(), key=lambda t: t.name.lower())

    def project_templates(self) -> List[WidgetTemplate]:
        return sorted(self._project_templates.values(), key=lambda t: t.name.lower())

    def all_templates(self) -> List[WidgetTemplate]:
        return sorted(self._templates.values(), key=lambda t: (t.source, t.name.lower()))

    def resolve(self, identifier: str) -> WidgetTemplate:
        norm = self._normalize(identifier)
        key = self._aliases.get(norm)
        if key and key in self._templates:
            return self._templates[key]
        if identifier.endswith(".json"):
            stem_norm = self._normalize(Path(identifier).stem)
            key = self._aliases.get(stem_norm)
            if key and key in self._templates:
                return self._templates[key]
        raise KeyError(
            f"Widget template '{identifier}' not found. Use 'plhub widget list' to inspect available templates."
        )

    # ------------------------------------------------------------------
    # Project helpers
    # ------------------------------------------------------------------
    def ensure_structure(self) -> None:
        if not self.project_root:
            raise RuntimeError("Widget operations that modify files require a project root.")
        assert self.project_widgets_dir is not None
        self.project_widgets_dir.mkdir(parents=True, exist_ok=True)
        assert self.project_templates_dir is not None
        self.project_templates_dir.mkdir(parents=True, exist_ok=True)

    def widgets_readme_path(self) -> Optional[Path]:
        if not self.project_widgets_dir:
            return None
        return self.project_widgets_dir / self.README_NAME

    def write_widgets_readme(self, force: bool = False) -> Optional[Path]:
        target = self.widgets_readme_path()
        if not target:
            return None
        if target.exists() and not force:
            return target
        content = (
            "# UI Widgets\n\n"
            "Use this directory to organize reusable widget snippets for your PohLang UI.\n\n"
            "Generated widgets will appear alongside hand-written components.\n\n"
            "Commands:\n\n"
            "```bash\n"
            "python plhub.py widget list\n"
            "python plhub.py widget generate button --name PrimaryButton\n"
            "python plhub.py widget preview card\n"
            "```\n"
        )
        target.write_text(content, encoding="utf-8")
        return target

    def project_widget_files(self) -> List[Path]:
        if not self.project_widgets_dir or not self.project_widgets_dir.exists():
            return []
        return sorted(self.project_widgets_dir.glob("*.poh"))

    # ------------------------------------------------------------------
    # Generation helpers
    # ------------------------------------------------------------------
    def generate(
        self,
        identifier: str,
        *,
        name: Optional[str] = None,
        force: bool = False,
        dry_run: bool = False,
    ) -> Tuple[WidgetTemplate, List[Path]]:
        if not self.project_root:
            raise RuntimeError("Widget generation requires running inside a project directory.")
        template = self.resolve(identifier)
        self.ensure_structure()
        assert self.project_widgets_dir is not None

        target_name = name or template.name
        context = self._build_context(target_name)
        created_paths: List[Path] = []

        for file_spec in template.files:
            relative_path = self._render_string(file_spec.path, context)
            if Path(relative_path).is_absolute() or relative_path.startswith(".."):
                raise ValueError(
                    f"Invalid widget file path '{relative_path}'. Paths must be project-relative."
                )
            destination = self.project_root / relative_path
            if destination.exists() and not (force or file_spec.overwrite):
                raise FileExistsError(
                    f"Widget file '{relative_path}' already exists. Use --force to overwrite."
                )
            if dry_run:
                created_paths.append(destination)
                continue
            destination.parent.mkdir(parents=True, exist_ok=True)
            content = self._render_string(file_spec.content, context)
            destination.write_text(content, encoding="utf-8")
            created_paths.append(destination)

        return template, created_paths

    # ------------------------------------------------------------------
    # Summaries / exports
    # ------------------------------------------------------------------
    def export_summary(self) -> Dict[str, Any]:
        project_files = []
        for path in self.project_widget_files():
            rel = str(path.relative_to(self.project_root)) if self.project_root else str(path)
            project_files.append(rel)
        return {
            "templates": [self._template_summary(t) for t in self.builtin_templates()],
            "projectTemplates": [self._template_summary(t) for t in self.project_templates()],
            "projectWidgets": project_files,
        }

    def preview(self, identifier: str) -> Dict[str, Any]:
        template = self.resolve(identifier)
        return self._template_summary(template, include_preview=True)

    # ------------------------------------------------------------------
    # Bootstrap helpers
    # ------------------------------------------------------------------
    @classmethod
    def bootstrap_project(
        cls,
        plhub_root: Path,
        project_root: Path,
        *,
        default_template: str = "card",
        widget_name: str = "WelcomeCard",
    ) -> Dict[str, Any]:
        manager = cls(plhub_root, project_root)
        manager.ensure_structure()
        manager.write_widgets_readme()
        info: Dict[str, Any] = {"template": None, "files": []}
        try:
            template, paths = manager.generate(default_template, name=widget_name, force=False)
            info["template"] = manager._template_summary(template)
            info["files"] = [str(p.relative_to(project_root)) for p in paths]
        except Exception:
            info["error"] = f"Failed to instantiate '{default_template}' widget template."
        return info

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _template_summary(template: WidgetTemplate, *, include_preview: bool = False) -> Dict[str, Any]:
        data = {
            "key": template.key,
            "name": template.name,
            "description": template.description,
            "category": template.category,
            "tags": list(template.tags),
            "source": template.source,
            "path": str(template.path),
            "files": [
                {
                    "path": spec.path,
                    "description": spec.description,
                    "overwrite": spec.overwrite,
                }
                for spec in template.files
            ],
        }
        if include_preview and template.preview:
            data["preview"] = template.preview
        return data

    @staticmethod
    def _build_context(name: str) -> Dict[str, str]:
        base = name.strip()
        if not base:
            base = "Widget"
        words = WidgetManager._split_words(base)
        slug_parts = [WidgetManager.slugify(word) for word in words]
        slug_parts = [part for part in slug_parts if part]
        snake = "_".join(slug_parts) if slug_parts else WidgetManager.slugify(base)
        snake = snake.replace("-", "_") or "widget"
        parts = [p for p in snake.split("_") if p]
        pascal = "".join(part.capitalize() for part in parts) or "Widget"
        kebab = "-".join(parts) or "widget"
        title = " ".join(part.capitalize() for part in parts) or base.title()
        return {
            "widget_name": base,
            "widget_snake": snake,
            "widget_pascal": pascal,
            "widget_kebab": kebab,
            "widget_title": title,
        }

    @staticmethod
    def _render_string(template: str, context: Dict[str, str]) -> str:
        result = template
        for key, value in context.items():
            result = result.replace(f"{{{{{key}}}}}", value)
        return result

    @staticmethod
    def _split_words(value: str) -> List[str]:
        if not value:
            return []
        matches = re.findall(r"[A-Z]?[a-z0-9]+|[A-Z]+(?=[A-Z][a-z]|\b)", value)
        if matches:
            return matches
        return re.findall(r"[a-z0-9]+", value, flags=re.IGNORECASE)
