from __future__ import annotations


def build_metrics(graph) -> dict:
    if graph is None:
        return {
            "atlas_graph_loaded": 0,
            "atlas_node_count": 0,
            "atlas_edge_count": 0,
        }

    return {
        "atlas_graph_loaded": 1,
        "atlas_node_count": graph.node_count(),
        "atlas_edge_count": graph.edge_count(),
    }
