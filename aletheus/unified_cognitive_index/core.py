from __future__ import annotations

from .models import (
    UCIHealthReport,
    UCINode,
    UCIQueryResult,
    UCIRelationship,
)
from .registry import uci


class UnifiedCognitiveIndexService:
    """
    Unified Cognitive Index Runtime Service

    The UCI provides the platform's cognitive map.

    It does NOT own information.
    It indexes relationships between information.

    Every subsystem may publish to it.

    Every subsystem may query it.
    """

    def __init__(self):

        self.registry = uci

    # -------------------------------------------------------
    # Publish
    # -------------------------------------------------------

    def publish_node(
        self,
        node: UCINode,
    ) -> None:

        self.registry.register_node(node)

    def publish_relationship(
        self,
        relationship: UCIRelationship,
    ) -> None:

        self.registry.register_relationship(
            relationship
        )

    # -------------------------------------------------------
    # Lookup
    # -------------------------------------------------------

    def node(
        self,
        node_id: str,
    ) -> UCINode | None:

        return self.registry.get_node(node_id)

    def related(
        self,
        node_id: str,
    ):

        return self.registry.connected_nodes(node_id)

    # -------------------------------------------------------
    # Search
    # -------------------------------------------------------

    def search(
        self,
        query: str,
    ) -> UCIQueryResult:

        return self.registry.search(query)

    # -------------------------------------------------------
    # Statistics
    # -------------------------------------------------------

    def statistics(self):

        return self.registry.statistics()

    # -------------------------------------------------------
    # Health
    # -------------------------------------------------------

    def health(
        self,
    ) -> UCIHealthReport:

        return self.registry.health()


uci_service = UnifiedCognitiveIndexService()
