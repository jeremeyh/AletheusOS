"""
AletheusOS
Genesis 50.0

Foundation Execution Graph™

Graph Registry
"""

from __future__ import annotations

from .models import (
    GraphEdge,
    GraphNode,
    NodeType,
)


class ExecutionGraphRegistry:
    """
    Canonical registry for graph nodes
    and graph edges.

    The graph preserves relationships
    between constitutional objects.

    It does not determine truth.
    It preserves lineage.
    """

    GENESIS = "50.0"
    VERSION = "1.0.0"

    def __init__(self) -> None:

        self._nodes: dict[str, GraphNode] = {}
        self._edges: dict[str, GraphEdge] = {}

    #
    # Node Operations
    #

    def register_node(
        self,
        node: GraphNode,
    ) -> GraphNode:

        self._nodes[node.node_id] = node

        return node

    def get_node(
        self,
        node_id: str,
    ) -> GraphNode | None:

        return self._nodes.get(node_id)

    def all_nodes(self) -> list[GraphNode]:

        return sorted(
            self._nodes.values(),
            key=lambda n: n.created_at,
        )

    def nodes_by_type(
        self,
        node_type: NodeType,
    ) -> list[GraphNode]:

        return [
            node
            for node in self._nodes.values()
            if node.node_type == node_type
        ]

    #
    # Edge Operations
    #

    def register_edge(
        self,
        edge: GraphEdge,
    ) -> GraphEdge:

        self._edges[edge.edge_id] = edge

        return edge

    def get_edge(
        self,
        edge_id: str,
    ) -> GraphEdge | None:

        return self._edges.get(edge_id)

    def all_edges(self) -> list[GraphEdge]:

        return sorted(
            self._edges.values(),
            key=lambda e: e.created_at,
        )

    #
    # Graph Queries
    #

    def outgoing(
        self,
        node_id: str,
    ) -> list[GraphEdge]:

        return [
            edge
            for edge in self._edges.values()
            if edge.source == node_id
        ]

    def incoming(
        self,
        node_id: str,
    ) -> list[GraphEdge]:

        return [
            edge
            for edge in self._edges.values()
            if edge.target == node_id
        ]

    def neighbors(
        self,
        node_id: str,
    ) -> list[str]:

        connected = set()

        for edge in self._edges.values():

            if edge.source == node_id:
                connected.add(edge.target)

            if edge.target == node_id:
                connected.add(edge.source)

        return sorted(connected)

    #
    # Diagnostics
    #

    def health(self) -> dict:

        return {
            "name": "Foundation Execution Graph Registry",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "healthy",
            "nodes": len(self._nodes),
            "edges": len(self._edges),
        }

    def statistics(self) -> dict:

        node_types: dict[str, int] = {}

        edge_types: dict[str, int] = {}

        for node in self._nodes.values():

            key = node.node_type.value

            node_types.setdefault(key, 0)

            node_types[key] += 1

        for edge in self._edges.values():

            key = edge.edge_type.value

            edge_types.setdefault(key, 0)

            edge_types[key] += 1

        return {
            "name": "Foundation Execution Graph Registry",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "nodes": len(self._nodes),
            "edges": len(self._edges),
            "node_types": node_types,
            "edge_types": edge_types,
        }


execution_graph_registry = ExecutionGraphRegistry()
