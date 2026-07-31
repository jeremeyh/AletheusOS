"""Runtime structure provider for SPAN™.

This provider remains static and side-effect free. It discovers likely runtime
composition roots and registration calls from source code without importing or
starting the live AletheusOS runtime.
"""

from __future__ import annotations

import ast

from ..evidence_store import EvidenceRecord
from .base import Provider, ProviderContext

RUNTIME_PATH_MARKERS = {
    "runtime",
    "kernel",
    "bootstrap",
    "composition",
    "lifecycle",
}


class RuntimeProvider(Provider):
    name = "runtime"
    version = "1.0.0"
    description = "Collect static runtime composition and lifecycle evidence."

    def collect(self, context: ProviderContext):
        root = context.root.resolve()

        for path in sorted(root.rglob("*.py")):
            relative = path.relative_to(root)
            lowered_parts = {part.lower() for part in relative.parts}
            if not lowered_parts.intersection(RUNTIME_PATH_MARKERS):
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
                if isinstance(node, ast.ClassDef):
                    name_lower = node.name.lower()
                    if any(
                        marker in name_lower
                        for marker in ("runtime", "kernel", "lifecycle", "bootstrap")
                    ):
                        yield EvidenceRecord(
                            kind="runtime_component",
                            provider=self.name,
                            source=relative.as_posix(),
                            location=f"{path}:{node.lineno}",
                            payload={
                                "path": relative.as_posix(),
                                "name": node.name,
                                "line": node.lineno,
                                "component_type": "class",
                            },
                            tags=("runtime", "component"),
                        )

                elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    name_lower = node.name.lower()
                    if name_lower in {
                        "start",
                        "stop",
                        "initialize",
                        "shutdown",
                        "bootstrap",
                        "register",
                        "wire",
                    }:
                        yield EvidenceRecord(
                            kind="runtime_lifecycle",
                            provider=self.name,
                            source=relative.as_posix(),
                            location=f"{path}:{node.lineno}",
                            payload={
                                "path": relative.as_posix(),
                                "name": node.name,
                                "line": node.lineno,
                                "async": isinstance(node, ast.AsyncFunctionDef),
                            },
                            tags=("runtime", "lifecycle"),
                        )

                elif isinstance(node, ast.Call):
                    function_name = ""
                    try:
                        function_name = ast.unparse(node.func)
                    except Exception:
                        pass
                    if any(
                        marker in function_name.lower()
                        for marker in ("register", "add_service", "add_engine", "wire")
                    ):
                        yield EvidenceRecord(
                            kind="runtime_registration",
                            provider=self.name,
                            source=relative.as_posix(),
                            location=f"{path}:{node.lineno}",
                            payload={
                                "path": relative.as_posix(),
                                "call": function_name,
                                "line": node.lineno,
                            },
                            tags=("runtime", "registration"),
                        )
