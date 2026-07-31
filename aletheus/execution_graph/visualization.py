"""
AletheusOS
Genesis 50.0

Foundation Execution Graph™

Visualization
"""

from __future__ import annotations

from .registry import execution_graph_registry


class ExecutionGraphVisualization:
    """
    Graph visualization services.

    Visualization represents
    constitutional relationships.

    It never alters the graph.
    """

    GENESIS = "50.0"
    VERSION = "1.0.0"

    def mermaid(self) -> str:
        """
        Generate a Mermaid graph.

        Suitable for GitHub, Markdown,
        Studio™, and documentation.
        """

        lines = ["graph TD"]

        #
        # Nodes
        #

        for node in execution_graph_registry.all_nodes():
            label = node.display_name.replace('"', "").replace("[", "").replace("]", "")

            lines.append(f'    {node.node_id}["{label}"]')

        #
        # Edges
        #

        for edge in execution_graph_registry.all_edges():
            lines.append(f"    {edge.source} -->|{edge.edge_type.value}| {edge.target}")

        return "\n".join(lines)

    def adjacency(self) -> dict:
        """
        Return adjacency representation.
        """

        graph: dict[str, list[str]] = {}

        for node in execution_graph_registry.all_nodes():
            graph[node.node_id] = [
                edge.target for edge in execution_graph_registry.outgoing(node.node_id)
            ]

        return graph

    def summary(self) -> dict:

        return {
            "nodes": len(execution_graph_registry.all_nodes()),
            "edges": len(execution_graph_registry.all_edges()),
            "graph_type": "Directed Constitutional Graph",
        }

    def health(self) -> dict:

        return {
            "name": "Foundation Execution Graph Visualization",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "healthy",
        }


execution_graph_visualization = ExecutionGraphVisualization()
