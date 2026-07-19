from __future__ import annotations
from dataclasses import dataclass, field

from aletheus.span.provider_registry import ProviderRegistry
from aletheus.span.analyzer_registry import AnalyzerRegistry
from aletheus.span.evidence_store import EvidenceStore
from aletheus.span.metric_registry import MetricRegistry
from aletheus.span.digital_twin import ArchitecturalDigitalTwin

@dataclass
class LivePipelineResult:
    providers:int=0
    analyzers:int=0
    evidence_records:int=0
    findings:int=0
    metrics:int=0
    status:str="ok"
    details:dict=field(default_factory=dict)

class LivePipeline:
    """Canonical executable SPAN pipeline."""

    def __init__(self):
        self.providers=ProviderRegistry.default()
        self.analyzers=AnalyzerRegistry.default()
        self.evidence=EvidenceStore()
        self.metric_registry=MetricRegistry()
        self.twin=ArchitecturalDigitalTwin.from_span(
            self.providers.providers(),
            self.analyzers.analyzers()
        )

    def collect(self):
        # Future provider execution hook.
        return 0

    def analyze(self):
        # Future analyzer execution hook.
        return 0,0

    def execute(self)->LivePipelineResult:
        evidence=self.collect()
        findings,metrics=self.analyze()
        return LivePipelineResult(
            providers=len(self.providers.providers()),
            analyzers=len(self.analyzers.analyzers()),
            evidence_records=evidence,
            findings=findings,
            metrics=metrics,
            details=self.twin.summary(),
        )
