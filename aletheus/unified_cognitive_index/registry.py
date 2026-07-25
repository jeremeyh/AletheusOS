from __future__ import annotations

from .models import (
    UCIHealthReport,
    UCINode,
    UCIQueryResult,
    UCIRelationship,
)


class UnifiedCognitiveIndex:
    """
    Unified Cognitive Index (UCI)

    The UCI is NOT the source of truth.

    It is the platform's cognitive index, maintaining
    relationships between knowledge, memory, runtime,
    governance, execution, intent, evidence, and applications.
    """

    def __init__(self) -> None:
        self._nodes: dict[str, UCINode] = {}
        self._relationships: dict[str, UCIRelationship] = {}

    # ---------------------------------------------------------
    # Node Operations
    # ---------------------------------------------------------

    def register_node(self, node: UCINode) -> None:
        self._nodes[node.node_id] = node

    def get_node(self, node_id: str) -> UCINode | None:
        return self._nodes.get(node_id)

    def remove_node(self, node_id: str) -> None:
        self._nodes.pop(node_id, None)

    def all_nodes(self) -> list[UCINode]:
        return list(self._nodes.values())

    # ---------------------------------------------------------
    # Relationship Operations
    # ---------------------------------------------------------

    def register_relationship(
        self,
        relationship: UCIRelationship,
    ) -> None:
        self._relationships[
            relationship.relationship_id
        ] = relationship

    def get_relationship(
        self,
        relationship_id: str,
    ) -> UCIRelationship | None:
        return self._relationships.get(relationship_id)

    def remove_relationship(
        self,
        relationship_id: str,
    ) -> None:
        self._relationships.pop(relationship_id, None)

    def all_relationships(self) -> list[UCIRelationship]:
        return list(self._relationships.values())

    # ---------------------------------------------------------
    # Graph Queries
    # ---------------------------------------------------------

    def outgoing_relationships(
        self,
        node_id: str,
    ) -> list[UCIRelationship]:

        return [
            relationship
            for relationship in self._relationships.values()
            if relationship.source_node_id == node_id
        ]

    def incoming_relationships(
        self,
        node_id: str,
    ) -> list[UCIRelationship]:

        return [
            relationship
            for relationship in self._relationships.values()
            if relationship.target_node_id == node_id
        ]

    def connected_nodes(
        self,
        node_id: str,
    ) -> list[UCINode]:

        connected = []

        for relationship in self.outgoing_relationships(node_id):
            node = self.get_node(
                relationship.target_node_id
            )
            if node:
                connected.append(node)

        for relationship in self.incoming_relationships(node_id):
            node = self.get_node(
                relationship.source_node_id
            )
            if node:
                connected.append(node)

        return connected

    # ---------------------------------------------------------
    # Search
    # ---------------------------------------------------------

    def search(
        self,
        text: str,
    ) -> UCIQueryResult:

        text = text.lower()

        matches = [
            node
            for node in self._nodes.values()
            if (
                text in node.title.lower()
                or text in node.description.lower()
            )
        ]

        return UCIQueryResult(
            nodes=matches,
            relationships=[],
            total_nodes=len(matches),
            total_relationships=0,
        )

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def statistics(self) -> dict:

        return {
            "nodes": len(self._nodes),
            "relationships": len(self._relationships),
        }

    # ---------------------------------------------------------
    # Health
    # ---------------------------------------------------------

    def health(self) -> UCIHealthReport:

        orphan_nodes = 0

        for node in self._nodes.values():

            if (
                not self.outgoing_relationships(node.node_id)
                and not self.incoming_relationships(node.node_id)
            ):
                orphan_nodes += 1

        weights = [
            relationship.weight
            for relationship in self._relationships.values()
        ]

        average_weight = (
            sum(weights) / len(weights)
            if weights
            else 0.0
        )

        return UCIHealthReport(
            status="healthy",
            node_count=len(self._nodes),
            relationship_count=len(self._relationships),
            orphan_node_count=orphan_nodes,
            average_relationship_weight=average_weight,
        )


# ------------------------------------------------------------------
# Singleton Registry
# ------------------------------------------------------------------

uci = UnifiedCognitiveIndex()
