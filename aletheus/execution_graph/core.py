"""
AletheusOS
Genesis 50.0

Foundation Execution Graph™

Core Services
"""

from __future__ import annotations

from .lineage import execution_graph_lineage
from .models import (
    EdgeType,
    GraphEdge,
    GraphNode,
    NodeType,
    new_edge_id,
    new_node_id,
)
from .registry import execution_graph_registry
from .traversal import execution_graph_traversal
from .visualization import execution_graph_visualization


class FoundationExecutionGraph:
    """
    Constitutional relationship graph.

    The Execution Graph connects canonical
    Foundation objects into explainable lineage.

    It does not determine truth.
    It preserves relationships.
    """

    GENESIS = "50.0"
    VERSION = "1.0.0"

    def create_node(
        self,
        *,
        node_type: NodeType,
        canonical_id: str,
        display_name: str,
        metadata: dict | None = None,
    ) -> GraphNode:

        node = GraphNode(
            node_id=new_node_id(),
            node_type=node_type,
            canonical_id=canonical_id,
            display_name=display_name,
            metadata=metadata or {},
        )

        execution_graph_registry.register_node(node)

        return node

    def connect(
        self,
        *,
        source: GraphNode | str,
        target: GraphNode | str,
        edge_type: EdgeType,
        metadata: dict | None = None,
    ) -> GraphEdge:

        source_id = source.node_id if isinstance(source, GraphNode) else source

        target_id = target.node_id if isinstance(target, GraphNode) else target

        edge = GraphEdge(
            edge_id=new_edge_id(),
            source=source_id,
            target=target_id,
            edge_type=edge_type,
            metadata=metadata or {},
        )

        execution_graph_registry.register_edge(edge)

        return edge

    def node(
        self,
        node_id: str,
    ) -> GraphNode | None:

        return execution_graph_registry.get_node(node_id)

    def edge(
        self,
        edge_id: str,
    ) -> GraphEdge | None:

        return execution_graph_registry.get_edge(edge_id)

    def nodes(self) -> list[GraphNode]:

        return execution_graph_registry.all_nodes()

    def edges(self) -> list[GraphEdge]:

        return execution_graph_registry.all_edges()

    def explain(
        self,
        node_id: str,
    ) -> dict:

        return execution_graph_lineage.explain(node_id)

    def trace_forward(
        self,
        node_id: str,
        *,
        depth: int = 3,
    ) -> list[GraphNode]:

        return execution_graph_traversal.trace_forward(
            node_id,
            depth=depth,
        )

    def trace_backward(
        self,
        node_id: str,
        *,
        depth: int = 3,
    ) -> list[GraphNode]:

        return execution_graph_traversal.trace_backward(
            node_id,
            depth=depth,
        )

    def mermaid(self) -> str:

        return execution_graph_visualization.mermaid()

    def health(self) -> dict:

        return {
            "name": "Foundation Execution Graph",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "healthy",
            "registry": execution_graph_registry.health(),
            "traversal": execution_graph_traversal.health(),
            "lineage": execution_graph_lineage.health(),
            "visualization": execution_graph_visualization.health(),
        }

    def statistics(self) -> dict:

        return execution_graph_registry.statistics()


foundation_execution_graph = FoundationExecutionGraph()
