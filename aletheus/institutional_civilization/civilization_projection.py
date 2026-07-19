"""Projection of Civilizations into the Constitutional Knowledge Graph."""

from __future__ import annotations

from dataclasses import dataclass

from aletheus.constitutional_graph import ConstitutionalKnowledgeGraph

from .civilization_models import CivilizationRecord
from .civilization_registry import CivilizationRegistry
from .registry import InstitutionRegistry


@dataclass(frozen=True, slots=True)
class CivilizationProjectionResult:
    civilization_id: str
    graph_node_id: str
    resolved_institutions: int
    unresolved_institutions: tuple[str, ...]

    def to_dict(self) -> dict:
        return {
            "civilization_id": self.civilization_id,
            "graph_node_id": self.graph_node_id,
            "resolved_institutions": self.resolved_institutions,
            "unresolved_institutions": list(
                self.unresolved_institutions
            ),
        }


class CivilizationProjector:
    """
    Projects civilization domains and membership relationships.

    Unimplemented canonical institutions remain visible as unresolved
    membership declarations rather than being falsely represented as
    operational institution records.
    """

    def __init__(
        self,
        civilization_registry: CivilizationRegistry,
        institution_registry: InstitutionRegistry,
        constitutional_graph: ConstitutionalKnowledgeGraph,
    ) -> None:
        self.civilization_registry = civilization_registry
        self.institution_registry = institution_registry
        self.constitutional_graph = constitutional_graph

        self._civilization_nodes: dict[str, str] = {}
        self._institution_nodes: dict[str, str] = {}

    def bind_institution_node(
        self,
        institution_id: str,
        graph_node_id: str,
    ) -> None:
        self._institution_nodes[institution_id] = graph_node_id

    def project(
        self,
        record: CivilizationRecord,
    ) -> CivilizationProjectionResult:
        existing = self.civilization_registry.get(
            record.civilization_id
        )

        if existing is None:
            self.civilization_registry.register(record)
        elif existing != record:
            raise ValueError(
                f"Civilization {record.civilization_id!r} already "
                "exists with a different definition."
            )

        civilization_node_id = self._civilization_nodes.get(
            record.civilization_id
        )

        if civilization_node_id is None:
            node = self.constitutional_graph.add_node(
                node_type="constitutional_civilization",
                label=record.canonical_name,
                data=record.to_dict(),
            )
            civilization_node_id = node["node_id"]
            self._civilization_nodes[
                record.civilization_id
            ] = civilization_node_id

        unresolved = []
        resolved = 0

        for institution_id in record.institution_ids:
            institution = self.institution_registry.get(
                institution_id
            )
            institution_node_id = self._institution_nodes.get(
                institution_id
            )

            if (
                institution is None
                or institution_node_id is None
            ):
                unresolved.append(institution_id)
                continue

            self.constitutional_graph.connect(
                source_id=civilization_node_id,
                target_id=institution_node_id,
                relationship="CONTAINS_INSTITUTION",
                data={
                    "civilization_id": record.civilization_id,
                    "institution_id": institution_id,
                },
            )
            resolved += 1

        return CivilizationProjectionResult(
            civilization_id=record.civilization_id,
            graph_node_id=civilization_node_id,
            resolved_institutions=resolved,
            unresolved_institutions=tuple(unresolved),
        )

    def project_all(
        self,
        records: tuple[CivilizationRecord, ...],
    ) -> tuple[CivilizationProjectionResult, ...]:
        return tuple(
            self.project(record)
            for record in records
        )
