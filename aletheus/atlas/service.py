from __future__ import annotations

from pathlib import Path

from .analyzer import AtlasAnalyzer
from .architecture_graph import ArchitectureGraphBuilder
from .health import build_health
from .metrics import build_metrics
from .models import ArchitectureGraph, AtlasReport
from .registry import AtlasRegistry


class AtlasService:
    """
    Sovereign Authority: Atlas™

    Atlas knows architecture.
    """

    authority = "Atlas™"
    family = "Platform Intelligence"
    knows = "Architecture"

    def __init__(
        self,
        builder: ArchitectureGraphBuilder | None = None,
        analyzer: AtlasAnalyzer | None = None,
        registry: AtlasRegistry | None = None,
    ) -> None:
        self.builder = builder or ArchitectureGraphBuilder()
        self.analyzer = analyzer or AtlasAnalyzer()
        self.registry = registry or AtlasRegistry()

    def discover(self, aletheus_root: Path) -> AtlasReport:
        graph = self.builder.build(aletheus_root)
        self.registry.publish(graph)
        return self.analyzer.analyze(graph)

    def graph(self) -> ArchitectureGraph | None:
        return self.registry.current()

    def health(self):
        return build_health(self.registry.current())

    def metrics(self) -> dict:
        return build_metrics(self.registry.current())
