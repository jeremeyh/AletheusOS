from __future__ import annotations

from .models import GraphEdge, new_edge_id


class ConstitutionalEdgeFactory:
    GENESIS = "20.0"
    VERSION = "0.1.0"

    def create(
        self,
        source_id: str,
        target_id: str,
        relationship: str,
        data: dict | None = None,
    ):
        return GraphEdge(
            edge_id=new_edge_id(),
            source_id=source_id,
            target_id=target_id,
            relationship=relationship,
            data=data or {},
        )


constitutional_edge_factory = ConstitutionalEdgeFactory()
