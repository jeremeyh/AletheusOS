from __future__ import annotations

from .models import GraphEdge, GraphNode


class ConstitutionalGraphRegistry:
    GENESIS = "20.0"
    VERSION = "0.1.0"

    def __init__(self):
        self._nodes: dict[str, GraphNode] = {}
        self._edges: dict[str, GraphEdge] = {}
        self._outgoing: dict[str, list[str]] = {}
        self._incoming: dict[str, list[str]] = {}

    def add_node(self, node: GraphNode):
        self._nodes[node.node_id] = node
        return node

    def add_edge(self, edge: GraphEdge):
        self._edges[edge.edge_id] = edge
        self._outgoing.setdefault(edge.source_id, []).append(edge.edge_id)
        self._incoming.setdefault(edge.target_id, []).append(edge.edge_id)
        return edge

    def get_node(self, node_id: str):
        return self._nodes.get(node_id)

    def get_edge(self, edge_id: str):
        return self._edges.get(edge_id)

    def nodes(self):
        return [node.to_dict() for node in self._nodes.values()]

    def edges(self):
        return [edge.to_dict() for edge in self._edges.values()]

    def outgoing(self, node_id: str):
        return [
            self._edges[edge_id]
            for edge_id in self._outgoing.get(node_id, [])
        ]

    def incoming(self, node_id: str):
        return [
            self._edges[edge_id]
            for edge_id in self._incoming.get(node_id, [])
        ]

    def statistics(self):
        return {
            "nodes": len(self._nodes),
            "edges": len(self._edges),
            "node_types": sorted(
                set(node.node_type for node in self._nodes.values())
            ),
            "relationships": sorted(
                set(edge.relationship for edge in self._edges.values())
            ),
        }
