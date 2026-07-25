"""Configuration and architectural manifest provider for SPAN™."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..evidence_store import EvidenceRecord
from .base import Provider, ProviderContext

CONFIG_SUFFIXES = {".json", ".toml", ".yaml", ".yml"}
ARCHITECTURE_NAMES = {
    "architecture.json",
    "architecture.yaml",
    "architecture.yml",
    "span.json",
    "span.yaml",
    "span.yml",
    "namespace_registry.json",
    "ownership_registry.json",
    "repository_policy.json",
}


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_toml(path: Path) -> Any:
    import tomllib

    return tomllib.loads(path.read_text(encoding="utf-8"))


def _load_yaml(path: Path) -> Any:
    try:
        import yaml  # type: ignore
    except ImportError:
        return {"_span_notice": "PyYAML is not installed; YAML content not parsed."}
    return yaml.safe_load(path.read_text(encoding="utf-8"))


class ConfigurationProvider(Provider):
    name = "configuration"
    version = "1.0.0"
    description = "Collect configuration files and architectural manifests."

    def collect(self, context: ProviderContext):
        root = context.root.resolve()

        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            relative = path.relative_to(root)
            if any(part in {".git", ".venv", "venv", "__pycache__"} for part in relative.parts):
                continue
            if path.suffix.lower() not in CONFIG_SUFFIXES:
                continue

            is_architecture = (
                path.name.lower() in ARCHITECTURE_NAMES
                or "architecture" in path.name.lower()
                or "span" in path.name.lower()
            )

            payload: dict[str, Any] = {
                "path": relative.as_posix(),
                "suffix": path.suffix.lower(),
                "architectural": is_architecture,
            }

            try:
                if path.suffix.lower() == ".json":
                    payload["content"] = _load_json(path)
                elif path.suffix.lower() == ".toml":
                    payload["content"] = _load_toml(path)
                else:
                    payload["content"] = _load_yaml(path)
                payload["parsed"] = True
            except Exception as exc:
                payload["parsed"] = False
                payload["error"] = f"{exc.__class__.__name__}: {exc}"

            yield EvidenceRecord(
                kind="architectural_manifest" if is_architecture else "configuration",
                provider=self.name,
                source=relative.as_posix(),
                location=str(path),
                payload=payload,
                tags=(
                    "configuration",
                    "architecture" if is_architecture else "general",
                ),
            )
