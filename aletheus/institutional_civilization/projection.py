"""Projection of institutional identity into existing platform services."""

from __future__ import annotations

from dataclasses import dataclass

from aletheus.constitutional_graph import ConstitutionalKnowledgeGraph
from aletheus.platform_registry import PlatformRegistry

from .models import InstitutionRecord
from .registry import InstitutionRegistry


@dataclass(frozen=True, slots=True)
class InstitutionProjectionResult:
    institution_id: str
    platform_component_id: str
    graph_node_id: str

    def to_dict(self) -> dict[str, str]:
        return {
            "institution_id": self.institution_id,
            "platform_component_id": self.platform_component_id,
            "graph_node_id": self.graph_node_id,
        }


class InstitutionProjector:
    """
    Projects canonical institutional identity into existing registries.

    Projection creates identity references only. It does not instantiate
    runtime services or alter their internal behavior.
    """

    def __init__(
        self,
        institution_registry: InstitutionRegistry,
        platform_registry: PlatformRegistry,
        constitutional_graph: ConstitutionalKnowledgeGraph,
    ) -> None:
        self.institution_registry = institution_registry
        self.platform_registry = platform_registry
        self.constitutional_graph = constitutional_graph
        self._graph_nodes: dict[str, str] = {}

    def project(
        self,
        record: InstitutionRecord,
        *,
        replace: bool = False,
    ) -> InstitutionProjectionResult:
        existing = self.institution_registry.get(record.institution_id)

        if existing is None:
            self.institution_registry.register(record)
        elif replace:
            self.institution_registry.register(record, replace=True)
        elif existing != record:
            raise ValueError(
                f"Institution {record.institution_id!r} already exists with "
                "a different constitutional definition."
            )

        self.platform_registry.register(
            component_id=record.institution_id,
            name=record.canonical_name,
            version=record.version,
            genesis=record.genesis,
            critical=record.criticality.value
            in {"critical", "constitutional"},
            dependencies=list(record.dependencies),
            metadata={
                "institution_id": record.institution_id,
                "purpose": record.purpose,
                "authority": record.authority,
                "jurisdiction": record.jurisdiction,
                "constitutional_layer": record.constitutional_layer.value,
                "pillar": record.pillar.value,
                "status": record.status.value,
                "criticality": record.criticality.value,
                "owner": record.owner,
                "repository_locations": list(record.repository_locations),
            },
        )

        graph_node_id = self._graph_nodes.get(record.institution_id)
        if graph_node_id is None:
            node = self.constitutional_graph.add_node(
                node_type="constitutional_institution",
                label=record.canonical_name,
                data=record.to_dict(),
            )
            graph_node_id = node["node_id"]
            self._graph_nodes[record.institution_id] = graph_node_id

        return InstitutionProjectionResult(
            institution_id=record.institution_id,
            platform_component_id=record.institution_id,
            graph_node_id=graph_node_id,
        )

    def project_all(
        self,
        records: tuple[InstitutionRecord, ...],
    ) -> tuple[InstitutionProjectionResult, ...]:
        results = tuple(self.project(record) for record in records)
        self._connect_institutional_relationships(records)
        return results

    def _connect_institutional_relationships(
        self,
        records: tuple[InstitutionRecord, ...],
    ) -> None:
        known_ids = {
            record.institution_id
            for record in records
        }

        for record in records:
            source_node_id = self._graph_nodes[record.institution_id]

            relationship_groups = (
                ("DEPENDS_ON", record.dependencies),
                ("GOVERNED_BY", record.governed_by),
                ("OBSERVED_BY", record.observed_by),
                ("CERTIFIED_BY", record.certified_by),
            )

            for relationship, targets in relationship_groups:
                for target_id in targets:
                    if target_id not in known_ids:
                        continue

                    target_node_id = self._graph_nodes[target_id]
                    self.constitutional_graph.connect(
                        source_id=source_node_id,
                        target_id=target_node_id,
                        relationship=relationship,
                        data={
                            "source_institution_id": record.institution_id,
                            "target_institution_id": target_id,
                        },
                    )

    def graph_node_id(self, institution_id: str) -> str | None:
        return self._graph_nodes.get(institution_id)
