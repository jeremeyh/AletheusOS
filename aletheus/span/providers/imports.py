"""Normalized Python import provider for SPAN™."""

from __future__ import annotations

import ast
from pathlib import Path

from ..evidence_store import EvidenceRecord
from .base import Provider, ProviderContext


def _module_name(relative: Path) -> str:
    path = relative.with_suffix("")
    parts = list(path.parts)
    if parts and parts[-1] == "__init__":
        parts.pop()
    return ".".join(parts)


def _resolve_relative_import(current: str, module: str | None, level: int) -> str:
    parts = current.split(".")
    if current and not current.endswith("__init__"):
        parts = parts[:-1]
    if level:
        parts = parts[: max(0, len(parts) - level + 1)]
    if module:
        parts.extend(module.split("."))
    return ".".join(part for part in parts if part)


class ImportProvider(Provider):
    name = "imports"
    version = "1.0.0"
    description = "Collect Python import relationships."

    def collect(self, context: ProviderContext):
        root = context.root.resolve()

        for path in sorted(root.rglob("*.py")):
            relative = path.relative_to(root)
            if any(
                part in {".git", ".venv", "venv", "__pycache__"}
                for part in relative.parts
            ):
                continue

            current_module = _module_name(relative)
            try:
                tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            except (OSError, UnicodeDecodeError, SyntaxError):
                continue

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        yield EvidenceRecord(
                            kind="import",
                            provider=self.name,
                            source=relative.as_posix(),
                            location=f"{path}:{node.lineno}",
                            payload={
                                "source_module": current_module,
                                "target_module": alias.name,
                                "imported_name": None,
                                "alias": alias.asname,
                                "line": node.lineno,
                                "relative_level": 0,
                            },
                            tags=("python", "import", "dependency"),
                        )

                elif isinstance(node, ast.ImportFrom):
                    target_module = _resolve_relative_import(
                        current_module,
                        node.module,
                        node.level,
                    )
                    for alias in node.names:
                        yield EvidenceRecord(
                            kind="import",
                            provider=self.name,
                            source=relative.as_posix(),
                            location=f"{path}:{node.lineno}",
                            payload={
                                "source_module": current_module,
                                "target_module": target_module,
                                "imported_name": alias.name,
                                "alias": alias.asname,
                                "line": node.lineno,
                                "relative_level": node.level,
                            },
                            tags=("python", "import", "dependency"),
                        )
