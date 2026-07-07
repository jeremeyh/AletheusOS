from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AtlasHealth:
    status: str
    graph_loaded: bool
    node_count: int
    edge_count: int


def build_health(graph) -> AtlasHealth:
    return AtlasHealth(
        status="healthy" if graph is not None else "degraded",
        graph_loaded=graph is not None,
        node_count=graph.node_count() if graph else 0,
        edge_count=graph.edge_count() if graph else 0,
    )
