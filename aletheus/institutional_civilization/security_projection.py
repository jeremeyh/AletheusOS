"""Projection of the canonical Security Civilization defense chain."""

from __future__ import annotations

from dataclasses import dataclass

from aletheus.constitutional_graph import ConstitutionalKnowledgeGraph

from .projection import InstitutionProjector


@dataclass(frozen=True, slots=True)
class SecurityRelationship:
    source_institution_id: str
    target_institution_id: str
    relationship: str

    def to_dict(self) -> dict[str, str]:
        return {
            "source_institution_id": self.source_institution_id,
            "target_institution_id": self.target_institution_id,
            "relationship": self.relationship,
        }


CANONICAL_SECURITY_RELATIONSHIPS = (
    SecurityRelationship(
        source_institution_id="aletheus.watch_tower",
        target_institution_id="aletheus.guardian",
        relationship="ESCALATES_TO",
    ),
    SecurityRelationship(
        source_institution_id="aletheus.guardian",
        target_institution_id="aletheus.conclave",
        relationship="REQUESTS_CONTAINMENT_FROM",
    ),
    SecurityRelationship(
        source_institution_id="aletheus.conclave",
        target_institution_id="aletheus.containment_vault",
        relationship="QUARANTINES_IN",
    ),
    SecurityRelationship(
        source_institution_id="aletheus.sentinel",
        target_institution_id="aletheus.conclave",
        relationship="PROTECTS",
    ),
    SecurityRelationship(
        source_institution_id="aletheus.sentinel",
        target_institution_id="aletheus.containment_vault",
        relationship="PROTECTS",
    ),
    SecurityRelationship(
        source_institution_id="aletheus.containment_vault",
        target_institution_id="aletheus.ledger",
        relationship="PRESERVES_CHAIN_OF_CUSTODY_IN",
    ),
    SecurityRelationship(
        source_institution_id="aletheus.guardian",
        target_institution_id="aletheus.council",
        relationship="ESCALATES_CONSTITUTIONAL_MATTERS_TO",
    ),
)


class SecurityCivilizationProjector:
    """Projects explicit defense relationships between security institutions."""

    def __init__(
        self,
        *,
        institution_projector: InstitutionProjector,
        constitutional_graph: ConstitutionalKnowledgeGraph,
    ) -> None:
        self.institution_projector = institution_projector
        self.constitutional_graph = constitutional_graph
        self._projected: set[
            tuple[str, str, str]
        ] = set()

    def project(
        self,
    ) -> tuple[dict, ...]:
        results = []

        for relationship in CANONICAL_SECURITY_RELATIONSHIPS:
            key = (
                relationship.source_institution_id,
                relationship.target_institution_id,
                relationship.relationship,
            )

            if key in self._projected:
                continue

            source_node_id = self.institution_projector.graph_node_id(
                relationship.source_institution_id
            )
            target_node_id = self.institution_projector.graph_node_id(
                relationship.target_institution_id
            )

            if source_node_id is None:
                raise KeyError(
                    "Security source institution has not been projected: "
                    f"{relationship.source_institution_id}"
                )

            if target_node_id is None:
                raise KeyError(
                    "Security target institution has not been projected: "
                    f"{relationship.target_institution_id}"
                )

            edge = self.constitutional_graph.connect(
                source_id=source_node_id,
                target_id=target_node_id,
                relationship=relationship.relationship,
                data=relationship.to_dict(),
            )

            self._projected.add(key)
            results.append(edge)

        return tuple(results)
