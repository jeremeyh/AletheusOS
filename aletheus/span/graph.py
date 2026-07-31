"""In-memory architectural knowledge graph for SPAN™."""

from __future__ import annotations

import json
from collections import defaultdict, deque
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from .models import GraphEdge, GraphNode


class ArchitecturalGraph:
    """A small dependency-free directed multigraph implementation."""

    def __init__(self) -> None:
        self._nodes: dict[str, GraphNode] = {}
        self._edges: dict[str, GraphEdge] = {}
        self._outgoing: dict[str, set[str]] = defaultdict(set)
        self._incoming: dict[str, set[str]] = defaultdict(set)

    def add_node(self, node: GraphNode, *, replace: bool = True) -> GraphNode:
        if node.id in self._nodes and not replace:
            raise ValueError(f"Graph node already exists: {node.id}")
        self._nodes[node.id] = node
        return node

    def ensure_node(
        self,
        node_id: str,
        *,
        kind: str,
        label: str | None = None,
        attributes: dict[str, Any] | None = None,
    ) -> GraphNode:
        existing = self._nodes.get(node_id)
        if existing is not None:
            return existing
        return self.add_node(
            GraphNode(node_id, kind, label or node_id, attributes or {})
        )

    def add_edge(self, edge: GraphEdge) -> GraphEdge:
        if edge.source not in self._nodes:
            raise KeyError(f"Unknown graph source node: {edge.source}")
        if edge.target not in self._nodes:
            raise KeyError(f"Unknown graph target node: {edge.target}")
        self._edges[edge.id] = edge
        self._outgoing[edge.source].add(edge.id)
        self._incoming[edge.target].add(edge.id)
        return edge

    def connect(
        self,
        source: str,
        target: str,
        *,
        kind: str,
        attributes: dict[str, Any] | None = None,
    ) -> GraphEdge:
        return self.add_edge(GraphEdge(source, target, kind, attributes or {}))

    def node(self, node_id: str) -> GraphNode | None:
        return self._nodes.get(node_id)

    def nodes(self, *, kind: str | None = None) -> tuple[GraphNode, ...]:
        values: Iterable[GraphNode] = self._nodes.values()
        if kind is not None:
            values = (node for node in values if node.kind == kind)
        return tuple(values)

    def edges(self, *, kind: str | None = None) -> tuple[GraphEdge, ...]:
        values: Iterable[GraphEdge] = self._edges.values()
        if kind is not None:
            values = (edge for edge in values if edge.kind == kind)
        return tuple(values)

    def outgoing(
        self, node_id: str, *, kind: str | None = None
    ) -> tuple[GraphEdge, ...]:
        edges = (self._edges[item_id] for item_id in self._outgoing.get(node_id, ()))
        if kind is not None:
            edges = (edge for edge in edges if edge.kind == kind)
        return tuple(edges)

    def incoming(
        self, node_id: str, *, kind: str | None = None
    ) -> tuple[GraphEdge, ...]:
        edges = (self._edges[item_id] for item_id in self._incoming.get(node_id, ()))
        if kind is not None:
            edges = (edge for edge in edges if edge.kind == kind)
        return tuple(edges)

    def reachable(self, start: str, *, edge_kind: str | None = None) -> tuple[str, ...]:
        if start not in self._nodes:
            return ()
        seen = {start}
        queue: deque[str] = deque([start])
        while queue:
            current = queue.popleft()
            for edge in self.outgoing(current, kind=edge_kind):
                if edge.target not in seen:
                    seen.add(edge.target)
                    queue.append(edge.target)
        seen.remove(start)
        return tuple(sorted(seen))

    def dependency_cycles(
        self, *, edge_kind: str = "imports"
    ) -> tuple[tuple[str, ...], ...]:
        adjacency = {
            node.id: [edge.target for edge in self.outgoing(node.id, kind=edge_kind)]
            for node in self.nodes()
        }
        visiting: set[str] = set()
        visited: set[str] = set()
        stack: list[str] = []
        cycles: set[tuple[str, ...]] = set()

        def canonicalize(cycle: list[str]) -> tuple[str, ...]:
            body = cycle[:-1]
            if not body:
                return ()
            rotations = [
                tuple(body[index:] + body[:index]) for index in range(len(body))
            ]
            return min(rotations)

        def visit(node_id: str) -> None:
            if node_id in visited:
                return
            visiting.add(node_id)
            stack.append(node_id)
            for target in adjacency.get(node_id, []):
                if target in visiting:
                    index = stack.index(target)
                    normalized = canonicalize(stack[index:] + [target])
                    if normalized:
                        cycles.add(normalized)
                elif target not in visited:
                    visit(target)
            stack.pop()
            visiting.remove(node_id)
            visited.add(node_id)

        for node_id in adjacency:
            if node_id not in visited:
                visit(node_id)
        return tuple(sorted(cycles))

    def to_dict(self) -> dict[str, Any]:
        return {
            "nodes": [node.to_dict() for node in self.nodes()],
            "edges": [edge.to_dict() for edge in self.edges()],
        }

    def export_json(self, destination: str | Path) -> Path:
        path = Path(destination)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(self.to_dict(), indent=2, sort_keys=True), encoding="utf-8"
        )
        return path

    def export_dot(self, destination: str | Path) -> Path:
        path = Path(destination)
        path.parent.mkdir(parents=True, exist_ok=True)
        lines = ["digraph SPAN {"]
        for node in self.nodes():
            label = node.label.replace('"', '\\"')
            lines.append(f'  "{node.id}" [label="{label}"];')
        for edge in self.edges():
            label = edge.kind.replace('"', '\\"')
            lines.append(f'  "{edge.source}" -> "{edge.target}" [label="{label}"];')
        lines.append("}")
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return path
