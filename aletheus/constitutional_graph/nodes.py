from __future__ import annotations

from .models import GraphNode, new_node_id


class ConstitutionalNodeFactory:
    GENESIS = "20.0"
    VERSION = "0.1.0"

    def create(self, node_type: str, label: str, data: dict | None = None):
        return GraphNode(
            node_id=new_node_id(),
            node_type=node_type,
            label=label,
            data=data or {},
        )


constitutional_node_factory = ConstitutionalNodeFactory()
