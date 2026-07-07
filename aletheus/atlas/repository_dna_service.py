from __future__ import annotations

from pathlib import Path

from .analyzer import AtlasAnalyzer
from .registry import AtlasRegistry
from .relationship_engine import RelationshipEngine
from .repository_dna_adapter import RepositoryDNAAtlasAdapter

try:
    from aletheus.repository_dna.inventory_provider import RepositoryDNAInventoryProvider
except Exception:  # pragma: no cover
    RepositoryDNAInventoryProvider = None


class RepositoryAwareAtlasService:
    """Atlas service that consumes Repository DNA instead of walking the filesystem directly."""

    authority = "Atlas™"
    family = "Platform Intelligence"
    knows = "architecture from repository dna"

    def __init__(
        self,
        inventory_provider=None,
        adapter: RepositoryDNAAtlasAdapter | None = None,
        relationships: RelationshipEngine | None = None,
        analyzer: AtlasAnalyzer | None = None,
        registry: AtlasRegistry | None = None,
    ) -> None:
        if inventory_provider is not None:
            self.inventory_provider = inventory_provider
        elif RepositoryDNAInventoryProvider is not None:
            self.inventory_provider = RepositoryDNAInventoryProvider()
        else:
            self.inventory_provider = None

        self.adapter = adapter or RepositoryDNAAtlasAdapter()
        self.relationships = relationships or RelationshipEngine()
        self.analyzer = analyzer or AtlasAnalyzer()
        self.registry = registry or AtlasRegistry()

    def discover_from_repository_dna(self, aletheus_root: Path):
        if self.inventory_provider is None:
            raise RuntimeError("Repository DNA inventory provider is unavailable.")

        records = self.inventory_provider.inventory(aletheus_root)
        graph = self.adapter.graph_from_inventory(records)
        graph = self.relationships.enrich_family_relationships(graph)
        self.registry.publish(graph)
        return self.analyzer.analyze(graph)

    def graph(self):
        return self.registry.current()
