from __future__ import annotations

from aletheus.span.analyzer_registry import AnalyzerRegistry
from aletheus.span.digital_twin import ArchitecturalDigitalTwin
from aletheus.span.fitness import FitnessEngine
from aletheus.span.governance import GovernanceEngine
from aletheus.span.metric_registry import MetricRegistry
from aletheus.span.provider_registry import ProviderRegistry


class SpanEngine:
    """High-level orchestration for SPAN."""

    def __init__(self):
        self.providers = ProviderRegistry.default()
        self.analyzers = AnalyzerRegistry.default()
        self.metrics = MetricRegistry()
        self.governance = GovernanceEngine()
        self.fitness = FitnessEngine.default()
        self.twin = ArchitecturalDigitalTwin.from_span(
            self.providers.providers(),
            self.analyzers.analyzers(),
        )

    def summary(self):
        return {
            "providers": len(self.providers.providers()),
            "analyzers": len(self.analyzers.analyzers()),
            "twin": self.twin.summary(),
        }

    def run(self):
        # Placeholder integration point.
        return self.summary()
