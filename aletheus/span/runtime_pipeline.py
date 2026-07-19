from __future__ import annotations

from dataclasses import dataclass, field

from aletheus.span.provider_registry import ProviderRegistry
from aletheus.span.analyzer_registry import AnalyzerRegistry
from aletheus.span.evidence_store import EvidenceStore
from aletheus.span.metric_registry import MetricRegistry
from aletheus.span.governance import GovernanceEngine
from aletheus.span.fitness import FitnessEngine
from aletheus.span.digital_twin import ArchitecturalDigitalTwin


@dataclass
class PipelineResult:
    providers: int = 0
    analyzers: int = 0
    findings: int = 0
    metrics: int = 0
    twin_nodes: int = 0
    status: str = "ok"
    metadata: dict = field(default_factory=dict)


class RuntimePipeline:
    """Canonical SPAN runtime orchestration."""

    def __init__(self):
        self.providers = ProviderRegistry.default()
        self.analyzers = AnalyzerRegistry.default()
        self.evidence = EvidenceStore()
        self.metrics = MetricRegistry()
        self.governance = GovernanceEngine()
        self.fitness = FitnessEngine.default()
        self.twin = ArchitecturalDigitalTwin.from_span(
            self.providers.providers(),
            self.analyzers.analyzers(),
        )

    def execute(self) -> PipelineResult:
        # TODO: invoke providers to populate EvidenceStore
        # TODO: invoke analyzers against EvidenceStore
        # TODO: publish findings and metrics
        # TODO: evaluate governance and fitness
        return PipelineResult(
            providers=len(self.providers.providers()),
            analyzers=len(self.analyzers.analyzers()),
            twin_nodes=self.twin.summary()["nodes"],
            metadata={"phase": "Genesis 12.3"},
        )
