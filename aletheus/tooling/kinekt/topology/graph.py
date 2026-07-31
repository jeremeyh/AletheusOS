"""Directed topology graph."""

from __future__ import annotations

from collections import defaultdict
from typing import Any


class DirectedGraph:
    def __init__(self) -> None:
        self.nodes: set[str] = set()
        self.outgoing: dict[str, set[str]] = defaultdict(set)
        self.incoming: dict[str, set[str]] = defaultdict(set)

    def add_node(self, node: str) -> None:
        self.nodes.add(node)

    def add_edge(self, source: str, target: str) -> None:
        self.nodes.update({source, target})
        self.outgoing[source].add(target)
        self.incoming[target].add(source)

    def fan_in(self, node: str) -> int:
        return len(self.incoming.get(node, set()))

    def fan_out(self, node: str) -> int:
        return len(self.outgoing.get(node, set()))


def _resolve_import(imported: str, known: set[str]) -> str | None:
    candidate = imported
    while candidate:
        if candidate in known:
            return candidate
        candidate = candidate.rpartition(".")[0]
    return None


def build_graph(modules: list[dict[str, Any]]) -> tuple[DirectedGraph, dict[str, str]]:
    graph = DirectedGraph()
    package_by_module: dict[str, str] = {}
    known: set[str] = set()

    for raw in modules:
        if not isinstance(raw, dict):
            continue
        module = raw.get("module")
        package = raw.get("package")
        if isinstance(module, str):
            known.add(module)
            graph.add_node(module)
            package_by_module[module] = (
                package if isinstance(package, str) else "unknown"
            )

    for raw in modules:
        if not isinstance(raw, dict):
            continue
        module = raw.get("module")
        imports = raw.get("imports", [])
        if not isinstance(module, str) or not isinstance(imports, list):
            continue
        for imported in imports:
            if not isinstance(imported, str):
                continue
            target = _resolve_import(imported, known)
            if target is not None and target != module:
                graph.add_edge(module, target)

    return graph, package_by_module
