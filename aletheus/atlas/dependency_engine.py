from __future__ import annotations

import ast
from pathlib import Path
from typing import Iterable

from .models import ArchitectureGraph, AtlasEdge, AtlasEdgeType


class DependencyEngine:
    """Extracts lightweight import-based dependency edges."""

    def enrich_from_imports(self, graph: ArchitectureGraph, aletheus_root: Path) -> ArchitectureGraph:
        known = {node.name for node in graph.nodes.values()}

        for py_file in aletheus_root.rglob("*.py"):
            try:
                tree = ast.parse(py_file.read_text(encoding="utf-8"))
            except Exception:
                continue

            source_subsystem = self._subsystem_for_file(py_file, aletheus_root)
            if not source_subsystem:
                continue

            for node in ast.walk(tree):
                dep = None
                if isinstance(node, ast.ImportFrom) and node.module:
                    dep = self._extract_aletheus_dependency(node.module, known)
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        dep = self._extract_aletheus_dependency(alias.name, known)
                        if dep:
                            break

                if dep and dep != source_subsystem:
                    graph.add_edge(
                        AtlasEdge(
                            source_id=f"subsystem:{source_subsystem}",
                            target_id=f"subsystem:{dep}",
                            type=AtlasEdgeType.DEPENDS_ON,
                            confidence=0.85,
                            metadata={"source_file": str(py_file)},
                        )
                    )

        return graph

    def _subsystem_for_file(self, py_file: Path, root: Path) -> str | None:
        try:
            rel = py_file.relative_to(root)
        except ValueError:
            return None
        if len(rel.parts) < 2:
            return None
        return rel.parts[0]

    def _extract_aletheus_dependency(self, module: str, known: set[str]) -> str | None:
        parts = module.split(".")
        if not parts:
            return None
        if parts[0] == "aletheus" and len(parts) > 1 and parts[1] in known:
            return parts[1]
        return None
