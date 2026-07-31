"""
AletheusOS
Genesis 50.0

Foundation Execution Graph™

Statistics Interface
"""

from __future__ import annotations

from collections import Counter

from .registry import execution_graph_registry


def statistics() -> dict:
    """
    Canonical statistics interface.

    Statistics answer:

        "How is the Foundation connected?"
    """

    nodes = execution_graph_registry.all_nodes()
    edges = execution_graph_registry.all_edges()

    node_types = Counter()
    edge_types = Counter()

    for node in nodes:
        node_types[node.node_type.value] += 1

    for edge in edges:
        edge_types[edge.edge_type.value] += 1

    return {
        "name": "Foundation Execution Graph",
        "genesis": "50.0",
        "version": "1.0.0",
        "nodes": len(nodes),
        "edges": len(edges),
        "node_types": dict(node_types),
        "edge_types": dict(edge_types),
    }
