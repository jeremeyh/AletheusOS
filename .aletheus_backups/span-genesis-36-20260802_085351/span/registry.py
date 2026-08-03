"""Analyzer registration and lifecycle management for SPAN™."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Protocol, runtime_checkable

from .evidence import EvidenceStore
from .graph import ArchitecturalGraph
from .models import AnalysisContext, AnalyzerResult


@runtime_checkable
class Analyzer(Protocol):
    """Contract implemented by all SPAN analyzers."""

    name: str
    version: str

    def analyze(
        self,
        context: AnalysisContext,
        evidence: EvidenceStore,
        graph: ArchitecturalGraph,
    ) -> AnalyzerResult:
        """Analyze the repository and return a normalized result."""


class AnalyzerRegistry:
    """Ordered registry of analyzer instances."""

    def __init__(self) -> None:
        self._analyzers: dict[str, Analyzer] = {}

    def register(self, analyzer: Analyzer, *, replace: bool = False) -> Analyzer:
        if not isinstance(analyzer, Analyzer):
            raise TypeError("Analyzer does not satisfy the SPAN analyzer protocol")
        if analyzer.name in self._analyzers and not replace:
            raise ValueError(f"Analyzer already registered: {analyzer.name}")
        self._analyzers[analyzer.name] = analyzer
        return analyzer

    def unregister(self, name: str) -> Analyzer | None:
        return self._analyzers.pop(name, None)

    def get(self, name: str) -> Analyzer:
        try:
            return self._analyzers[name]
        except KeyError as exc:
            raise KeyError(f"Analyzer not registered: {name}") from exc

    def all(self) -> tuple[Analyzer, ...]:
        return tuple(self._analyzers.values())

    def names(self) -> tuple[str, ...]:
        return tuple(self._analyzers)

    def extend(self, analyzers: Iterable[Analyzer], *, replace: bool = False) -> None:
        for analyzer in analyzers:
            self.register(analyzer, replace=replace)

    def __len__(self) -> int:
        return len(self._analyzers)
