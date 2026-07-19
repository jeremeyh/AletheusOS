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
