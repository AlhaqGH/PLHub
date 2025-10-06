"""Utilities for managing PLHub style manifests and theme assets."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple
import datetime as _dt
import hashlib
import json
import shutil


@dataclass
class StyleRecord:
    """Metadata describing a single style/theme definition."""

    key: str
    name: str
    description: Optional[str]
    path: Path
    source: str
    data: Dict[str, Any]


class StyleManager:
    """High-level helper around style discovery, application, and authoring."""

    BUILTIN_DIR_NAME = "styles"
    PROJECT_RELATIVE_DIR = Path("ui") / "styles"
    THEMES_DIR_NAME = "themes"
    ACTIVE_MANIFEST_NAME = "active_style.json"
    README_NAME = "README.md"

    def __init__(self, plhub_root: Path, project_root: Optional[Path] = None) -> None:
        self.plhub_root = plhub_root
        self.project_root = project_root
        self.builtin_dir = plhub_root / self.BUILTIN_DIR_NAME
        self.project_styles_root = (
            project_root / self.PROJECT_RELATIVE_DIR if project_root else None
        )
        self.project_themes_dir = (
            self.project_styles_root / self.THEMES_DIR_NAME
            if self.project_styles_root
            else None
        )

        self._builtin_styles: Dict[str, StyleRecord] = self._load_styles(
            self.builtin_dir, source="builtin"
        )
        self._project_styles: Dict[str, StyleRecord] = (
            self._load_styles(self.project_themes_dir, source="project")
            if self.project_themes_dir
            else {}
        )
        self._index: Dict[str, StyleRecord] = {**self._builtin_styles, **self._project_styles}
        self._aliases: Dict[str, str] = {}
        self._register_aliases(self._builtin_styles.values())
        self._register_aliases(self._project_styles.values())

    # ------------------------------------------------------------------
    # Discovery helpers
    # ------------------------------------------------------------------
    @staticmethod
    def slugify(value: str) -> str:
        cleaned = []
        for ch in value.strip().lower():
            if ch.isalnum():
                cleaned.append(ch)
            elif ch in {" ", "-", "_", "."}:
                cleaned.append("_")
        slug = "".join(cleaned)
        while "__" in slug:
            slug = slug.replace("__", "_")
        slug = slug.strip("_")
        return slug or "style"

    @staticmethod
    def _normalize(value: str) -> str:
        if not value:
            return ""
        if value.lower().endswith(".json"):
            value = value[:-5]
        return StyleManager.slugify(value)

    def _register_aliases(self, records: Iterable[StyleRecord]) -> None:
        for record in records:
            key = record.key
            self._aliases[key] = key
            self._aliases[self._normalize(record.name)] = key
            self._aliases[self._normalize(record.path.stem)] = key
            self._aliases[self._normalize(record.path.name)] = key

    def _load_styles(self, directory: Optional[Path], source: str) -> Dict[str, StyleRecord]:
        results: Dict[str, StyleRecord] = {}
        if not directory or not directory.exists():
            return results
        for json_path in sorted(directory.glob("*.json")):
            record = self._load_style_from_path(json_path, source=source)
            if record:
                results[record.key] = record
        return results

    def _load_style_from_path(
        self, json_path: Path, source: str
    ) -> Optional[StyleRecord]:
        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None
        name = data.get("name") or json_path.stem.replace("_", " ").title()
        description = data.get("description")
        key = self.slugify(json_path.stem)
        return StyleRecord(key=key, name=name, description=description, path=json_path, source=source, data=data)

    # ------------------------------------------------------------------
    # Public accessors
    # ------------------------------------------------------------------
    def builtin_styles(self) -> List[StyleRecord]:
        return sorted(self._builtin_styles.values(), key=lambda r: r.name.lower())

    def project_styles(self) -> List[StyleRecord]:
        return sorted(self._project_styles.values(), key=lambda r: r.name.lower())

    def all_styles(self) -> List[StyleRecord]:
        return sorted(self._index.values(), key=lambda r: (r.source, r.name.lower()))

    def resolve(self, identifier: str) -> StyleRecord:
        norm = self._normalize(identifier)
        key = self._aliases.get(norm)
        if key and key in self._index:
            return self._index[key]
        if identifier.endswith(".json"):
            stem_norm = self._normalize(Path(identifier).stem)
            key = self._aliases.get(stem_norm)
            if key and key in self._index:
                return self._index[key]
        raise KeyError(f"Style '{identifier}' not found. Use 'plhub style list' to inspect available themes.")

    # ------------------------------------------------------------------
    # Project structure helpers
    # ------------------------------------------------------------------
    def ensure_structure(self) -> None:
        if not self.project_root:
            raise RuntimeError("A project root is required for this operation.")
        (self.project_root / "ui").mkdir(exist_ok=True)
        assert self.project_styles_root is not None
        self.project_styles_root.mkdir(exist_ok=True)
        assert self.project_themes_dir is not None
        self.project_themes_dir.mkdir(exist_ok=True)

    def styles_readme_path(self) -> Optional[Path]:
        if not self.project_styles_root:
            return None
        return self.project_styles_root / self.README_NAME

    def active_manifest_path(self) -> Optional[Path]:
        if not self.project_styles_root:
            return None
        return self.project_styles_root / self.ACTIVE_MANIFEST_NAME

    def write_styles_readme(self, force: bool = False) -> Optional[Path]:
        target = self.styles_readme_path()
        if not target:
            return None
        if target.exists() and not force:
            return target
        content = (
            "# UI Styles\n\n"
            "This directory stores theme definitions used by PLHub.\n\n"
            "- `active_style.json` selects the theme currently applied to the project.\n"
            "- `themes/` contains editable JSON themes.\n\n"
            "Manage themes via the CLI:\n\n"
            "```bash\n"
            "python plhub.py style list\n"
            "python plhub.py style apply default_light\n"
            "python plhub.py style create My Theme --base default_light\n"
            "```\n"
        )
        target.write_text(content, encoding="utf-8")
        return target

    # ------------------------------------------------------------------
    # Active manifest helpers
    # ------------------------------------------------------------------
    def read_manifest(self) -> Optional[Dict[str, Any]]:
        manifest_path = self.active_manifest_path()
        if not manifest_path or not manifest_path.exists():
            return None
        try:
            return json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None

    def write_manifest(self, data: Dict[str, Any]) -> Optional[Path]:
        manifest_path = self.active_manifest_path()
        if not manifest_path:
            return None
        manifest_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        return manifest_path

    def get_active(self) -> Tuple[Optional[Dict[str, Any]], Optional[StyleRecord]]:
        manifest = self.read_manifest()
        if not manifest:
            return None, None
        key = manifest.get("activeTheme")
        if key and key in self._index:
            return manifest, self._index[key]
        path_rel = manifest.get("themePath")
        if (
            path_rel
            and self.project_styles_root
            and (self.project_styles_root / path_rel).exists()
        ):
            loaded = self._load_style_from_path(
                self.project_styles_root / path_rel, source="project"
            )
            if loaded:
                self._project_styles[loaded.key] = loaded
                self._index[loaded.key] = loaded
                self._register_aliases([loaded])
                return manifest, loaded
        return manifest, None

    # ------------------------------------------------------------------
    # Theme operations
    # ------------------------------------------------------------------
    def apply(self, identifier: str, *, force: bool = False) -> Dict[str, Any]:
        if not self.project_root:
            raise RuntimeError("Style application requires a project root.")
        style = self.resolve(identifier)
        self.ensure_structure()
        assert self.project_themes_dir is not None
        dest_path = self.project_themes_dir / f"{style.key}.json"

        if style.source == "builtin":
            if not dest_path.exists() or force:
                shutil.copy2(style.path, dest_path)
            else:
                # If destination exists and not forcing, reuse on-disk file
                pass
        else:
            # For project styles, ensure the file is under the expected directory
            if style.path.resolve() != dest_path.resolve():
                if not dest_path.exists() or force:
                    shutil.copy2(style.path, dest_path)
        if not dest_path.exists():
            # As a fallback, copy the original definition
            shutil.copy2(style.path, dest_path)

        checksum = self._compute_checksum(dest_path)
        relative_theme_path = Path(self.THEMES_DIR_NAME) / dest_path.name
        manifest = {
            "activeTheme": style.key,
            "displayName": style.name,
            "themePath": str(relative_theme_path).replace("\\", "/"),
            "source": style.source,
            "appliedAt": _dt.datetime.utcnow().replace(microsecond=False).isoformat() + "Z",
            "checksum": checksum,
        }
        self.write_manifest(manifest)

        # Register/update local cache
        local_record = self._load_style_from_path(dest_path, source="project")
        if local_record:
            self._project_styles[local_record.key] = local_record
            self._index[local_record.key] = local_record
            self._register_aliases([local_record])

        return manifest

    def create_theme(
        self,
        name: str,
        *,
        base_identifier: Optional[str] = None,
        description: Optional[str] = None,
        force: bool = False,
    ) -> StyleRecord:
        if not self.project_root:
            raise RuntimeError("Creating themes requires a project root.")
        self.ensure_structure()
        base_key = base_identifier or "default_light"
        try:
            base_style = self.resolve(base_key)
        except KeyError as exc:
            raise KeyError(
                f"Base style '{base_key}' not found. Use 'plhub style list' to choose an existing theme."
            ) from exc

        slug = self.slugify(name)
        assert self.project_themes_dir is not None
        destination = self.project_themes_dir / f"{slug}.json"
        if destination.exists() and not force:
            raise FileExistsError(
                f"Theme '{slug}' already exists. Use --force to overwrite or choose a different name."
            )

        # Load base data and customise name/description
        base_data = json.loads(base_style.path.read_text(encoding="utf-8"))
        base_data["name"] = name
        if description:
            base_data["description"] = description
        else:
            base_data.setdefault(
                "description",
                f"Custom theme derived from {base_style.name}",
            )

        destination.write_text(json.dumps(base_data, indent=2) + "\n", encoding="utf-8")

        record = StyleRecord(
            key=slug,
            name=name,
            description=base_data.get("description"),
            path=destination,
            source="project",
            data=base_data,
        )
        self._project_styles[slug] = record
        self._index[slug] = record
        self._register_aliases([record])
        return record

    # ------------------------------------------------------------------
    # Bootstrap helpers
    # ------------------------------------------------------------------
    @classmethod
    def bootstrap_project(
        cls,
        plhub_root: Path,
        project_root: Path,
        *,
        default_style: str = "default_light",
    ) -> Dict[str, Any]:
        manager = cls(plhub_root, project_root)
        manager.ensure_structure()
        manager.write_styles_readme()
        return manager.apply(default_style)

    # ------------------------------------------------------------------
    # Utility helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _compute_checksum(path: Path) -> str:
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(65536), b""):
                digest.update(chunk)
        return digest.hexdigest()

    def export_summary(self) -> Dict[str, Any]:
        manifest, active = self.get_active()
        return {
            "builtin": [self._record_summary(r) for r in self.builtin_styles()],
            "project": [self._record_summary(r) for r in self.project_styles()],
            "active": manifest,
            "activeResolved": self._record_summary(active) if active else None,
        }

    @staticmethod
    def _record_summary(record: Optional[StyleRecord]) -> Optional[Dict[str, Any]]:
        if not record:
            return None
        return {
            "key": record.key,
            "name": record.name,
            "description": record.description,
            "path": str(record.path),
            "source": record.source,
        }
