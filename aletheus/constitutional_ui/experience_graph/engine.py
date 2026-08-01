from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class GraphNode:
    node_id: str
    kind: str
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class GraphEdge:
    source: str
    target: str
    relation: str
    weight: float = 1.0


class Engine:
    def build(
        self, nodes: tuple[GraphNode, ...], edges: tuple[GraphEdge, ...]
    ) -> dict[str, object]:
        ids = {n.node_id for n in nodes}
        findings = [
            f"missing endpoint: {e.source}->{e.target}"
            for e in edges
            if e.source not in ids or e.target not in ids
        ]
        return {
            "valid": not findings,
            "findings": findings,
            "nodes": [
                {"id": n.node_id, "kind": n.kind, "payload": n.payload} for n in nodes
            ],
            "edges": [
                {
                    "source": e.source,
                    "target": e.target,
                    "relation": e.relation,
                    "weight": e.weight,
                }
                for e in edges
            ],
        }
