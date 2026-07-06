"""
AletheusOS
Genesis 50.0

Foundation Execution Graph™

Lineage Services
"""

from __future__ import annotations

from .models import GraphNode
from .traversal import execution_graph_traversal


class ExecutionGraphLineage:
    """
    Constitutional lineage services.

    Lineage reconstructs the history of a
    constitutional object.

    Lineage never creates history.

    It reveals existing constitutional
    relationships.
    """

    GENESIS = "50.0"
    VERSION = "1.0.0"

    def ancestry(
        self,
        node_id: str,
        *,
        depth: int = 10,
    ) -> list[GraphNode]:
        """
        Return every known predecessor.

        Example

        Reason

            ↑

        Memory

            ↑

        Intent
        """

        return execution_graph_traversal.trace_backward(
            node_id,
            depth=depth,
        )

    def descendants(
        self,
        node_id: str,
        *,
        depth: int = 10,
    ) -> list[GraphNode]:
        """
        Return every known successor.

        Example

        Intent

            ↓

        Memory

            ↓

        Reason
        """

        return execution_graph_traversal.trace_forward(
            node_id,
            depth=depth,
        )

    def explain(
        self,
        node_id: str,
    ) -> dict:
        """
        Explain a constitutional object by
        returning both its ancestry and
        descendants.

        This becomes the basis of
        explainable cognition.
        """

        return {

            "node": node_id,

            "ancestry": [
                node.to_dict()
                for node in self.ancestry(node_id)
            ],

            "descendants": [
                node.to_dict()
                for node in self.descendants(node_id)
            ],
        }

    def health(self) -> dict:

        return {

            "name": "Foundation Execution Graph Lineage",

            "genesis": self.GENESIS,

            "version": self.VERSION,

            "status": "healthy",
        }


execution_graph_lineage = ExecutionGraphLineage()
