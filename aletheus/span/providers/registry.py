"""Registry structure provider for SPAN™."""

from __future__ import annotations

import ast

from ..evidence_store import EvidenceRecord
from .base import Provider, ProviderContext


class RegistryProvider(Provider):
    name = "registry"
    version = "1.0.0"
    description = (
        "Collect static service, engine, capability, and plugin registry evidence."
    )

    def collect(self, context: ProviderContext):
        root = context.root.resolve()

        for path in sorted(root.rglob("*.py")):
            relative = path.relative_to(root)
            if "registry" not in path.name.lower() and "registries" not in {
                part.lower() for part in relative.parts
            }:
                continue
            if any(
                part in {".git", ".venv", "venv", "__pycache__"}
                for part in relative.parts
            ):
                continue

            try:
                tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            except (OSError, UnicodeDecodeError, SyntaxError):
                continue

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef) and "registry" in node.name.lower():
                    yield EvidenceRecord(
                        kind="registry_component",
                        provider=self.name,
                        source=relative.as_posix(),
                        location=f"{path}:{node.lineno}",
                        payload={
                            "path": relative.as_posix(),
                            "name": node.name,
                            "line": node.lineno,
                        },
                        tags=("registry", "component"),
                    )

                elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    lowered = node.name.lower()
                    if any(
                        marker in lowered
                        for marker in (
                            "register",
                            "resolve",
                            "discover",
                            "unregister",
                            "list_services",
                            "list_engines",
                            "list_capabilities",
                        )
                    ):
                        yield EvidenceRecord(
                            kind="registry_operation",
                            provider=self.name,
                            source=relative.as_posix(),
                            location=f"{path}:{node.lineno}",
                            payload={
                                "path": relative.as_posix(),
                                "name": node.name,
                                "line": node.lineno,
                                "async": isinstance(node, ast.AsyncFunctionDef),
                            },
                            tags=("registry", "operation"),
                        )
