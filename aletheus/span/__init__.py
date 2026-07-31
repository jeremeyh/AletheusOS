"""SPAN™ — Spectrum Platform Analyzer for AletheusOS."""

from .models import (
    AnalysisContext,
    AnalyzerResult,
    Evidence,
    Finding,
    FindingSeverity,
    GraphEdge,
    GraphNode,
    Metric,
)

__all__ = [
    "AnalysisContext",
    "AnalyzerResult",
    "Evidence",
    "Finding",
    "FindingSeverity",
    "GraphEdge",
    "GraphNode",
    "Metric",
    "SpanEngine",
]


def __getattr__(name: str):
    if name == "SpanEngine":
        from .engine import SpanEngine

        return SpanEngine
    raise AttributeError(name)


__version__ = "11.0.0"

# Genesis 11.1 provider framework exports.
from .analyzer import Analyzer, AnalyzerContext, AnalyzerResult

# BEGIN GENESIS 14 PUBLIC API
from .api import SPAN
from .bootstrap import (
    BootstrapDiagnostic,
    BootstrapReport,
    BootstrapState,
    SPANBootstrap,
    bootstrap_span,
)
from .evidence_store import EvidenceRecord, EvidenceStore
from .finding import Finding, FindingSet, Severity
from .pipeline import PipelineResult, SPANPipeline, default_providers
from .profiles import RuleProfile, load_profile
from .reporter import SPANReport
# END GENESIS 14 PUBLIC API
