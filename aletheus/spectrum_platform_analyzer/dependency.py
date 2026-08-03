"""
Spectrum Platform Analyzer Dependency Analysis

Genesis 54.0
"""

from __future__ import annotations

import ast
import os
from pathlib import Path


class DependencyAnalyzer:
    VERSION = "1.0.0"

    GENESIS = "54.0"

    def python_files(self, root: str) -> list[Path]:

        root_path = Path(root)

        results: list[Path] = []

        for current, dirs, files in os.walk(root_path):
            dirs[:] = [
                d
                for d in dirs
                if d != "__pycache__"
                and not d.startswith(".")
                and d not in {"venv", "venv_backup", "node_modules"}
            ]

            for file in files:
                if file.endswith(".py"):
                    results.append(Path(current) / file)

        return sorted(results)

    def module_name(
        self,
        file_path: Path,
        root: str,
    ) -> str:

        root_path = Path(root).resolve()

        relative = file_path.resolve().relative_to(root_path)

        parts = list(relative.with_suffix("").parts)

        if parts[-1] == "__init__":
            parts = parts[:-1]

        return ".".join(parts)

    def imports_for_file(
        self,
        file_path: Path,
    ) -> list[str]:

        imports: set[str] = set()

        try:
            tree = ast.parse(file_path.read_text(encoding="utf-8"))

        except Exception:
            return []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name)

            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module)

        return sorted(imports)

    def import_graph(
        self,
        root: str,
    ) -> dict[str, list[str]]:

        graph: dict[str, list[str]] = {}

        for file_path in self.python_files(root):
            module = self.module_name(
                file_path,
                root,
            )

            graph[module] = self.imports_for_file(file_path)

        return graph

    def internal_import_graph(
        self,
        root: str,
        package_prefix: str = "aletheus",
    ) -> dict[str, list[str]]:

        graph = self.import_graph(root)

        internal: dict[str, list[str]] = {}

        for module, imports in graph.items():
            internal[module] = [
                imp
                for imp in imports
                if imp == package_prefix or imp.startswith(f"{package_prefix}.")
            ]

        return internal

    def fan_out(
        self,
        root: str,
    ) -> dict[str, int]:

        graph = self.internal_import_graph(root)

        return {module: len(imports) for module, imports in graph.items()}

    def top_fan_out(
        self,
        root: str,
        limit: int = 20,
    ) -> list[dict]:

        fanout = self.fan_out(root)

        ranked = sorted(
            fanout.items(),
            key=lambda item: item[1],
            reverse=True,
        )

        return [
            {
                "module": module,
                "internal_imports": count,
            }
            for module, count in ranked[:limit]
        ]

    def fan_in(
        self,
        root: str,
    ) -> dict[str, int]:

        graph = self.internal_import_graph(root)

        counts: dict[str, int] = {}

        for imports in graph.values():
            for imported in imports:
                counts[imported] = counts.get(imported, 0) + 1

        return counts

    def top_fan_in(
        self,
        root: str,
        limit: int = 20,
    ) -> list[dict]:

        fanin = self.fan_in(root)

        ranked = sorted(
            fanin.items(),
            key=lambda item: item[1],
            reverse=True,
        )

        return [
            {
                "module": module,
                "imported_by": count,
            }
            for module, count in ranked[:limit]
        ]

    def health(self) -> dict:

        return {
            "name": "Spectrum Dependency Analyzer",
            "status": "healthy",
            "version": self.VERSION,
            "genesis": self.GENESIS,
        }


dependency_analyzer = DependencyAnalyzer()
