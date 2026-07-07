from __future__ import annotations

from pathlib import Path

from .dependency_engine import DependencyEngine
from .models import ArchitectureGraph
from .relationship_engine import RelationshipEngine
from .topology import TopologyEngine


class ArchitectureGraphBuilder:
    """Builds the Atlas architecture graph."""

    def __init__(
        self,
        topology: TopologyEngine | None = None,
        dependencies: DependencyEngine | None = None,
        relationships: RelationshipEngine | None = None,
    ) -> None:
        self.topology = topology or TopologyEngine()
        self.dependencies = dependencies or DependencyEngine()
        self.relationships = relationships or RelationshipEngine()

    def build(self, aletheus_root: Path) -> ArchitectureGraph:
        snapshot = self.topology.discover_from_path(aletheus_root)
        graph = snapshot.graph
        graph = self.dependencies.enrich_from_imports(graph, aletheus_root)
        graph = self.relationships.enrich_family_relationships(graph)
        return graph
