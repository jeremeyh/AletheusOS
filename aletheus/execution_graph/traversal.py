"""
AletheusOS
Genesis 50.0

Foundation Execution Graph™

Graph Traversal
"""

from __future__ import annotations

from .models import GraphEdge, GraphNode
from .registry import execution_graph_registry


class ExecutionGraphTraversal:
    """
    Constitutional graph traversal.

    Traversal does not determine meaning.
    Traversal reveals relationships.
    """

    GENESIS = "50.0"
    VERSION = "1.0.0"

    def outgoing_edges(
        self,
        node_id: str,
    ) -> list[GraphEdge]:

        return execution_graph_registry.outgoing(node_id)

    def incoming_edges(
        self,
        node_id: str,
    ) -> list[GraphEdge]:

        return execution_graph_registry.incoming(node_id)

    def neighbors(
        self,
        node_id: str,
    ) -> list[GraphNode]:

        nodes: list[GraphNode] = []

        for neighbor_id in execution_graph_registry.neighbors(node_id):

            node = execution_graph_registry.get_node(neighbor_id)

            if node:
                nodes.append(node)

        return nodes

    def trace_forward(
        self,
        node_id: str,
        *,
        depth: int = 3,
    ) -> list[GraphNode]:

        visited: set[str] = set()
        result: list[GraphNode] = []

        def walk(current: str, remaining: int) -> None:

            if remaining < 0 or current in visited:
                return

            visited.add(current)

            node = execution_graph_registry.get_node(current)

            if node:
                result.append(node)

            for edge in execution_graph_registry.outgoing(current):
                walk(edge.target, remaining - 1)

        walk(node_id, depth)

        return result

    def trace_backward(
        self,
        node_id: str,
        *,
        depth: int = 3,
    ) -> list[GraphNode]:

        visited: set[str] = set()
        result: list[GraphNode] = []

        def walk(current: str, remaining: int) -> None:

            if remaining < 0 or current in visited:
                return

            visited.add(current)

            node = execution_graph_registry.get_node(current)

            if node:
                result.append(node)

            for edge in execution_graph_registry.incoming(current):
                walk(edge.source, remaining - 1)

        walk(node_id, depth)

        return result

    def health(self) -> dict:

        return {
            "name": "Foundation Execution Graph Traversal",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "healthy",
        }


execution_graph_traversal = ExecutionGraphTraversal()
