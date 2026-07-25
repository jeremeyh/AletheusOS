"""SPARTAN™ network composition and orchestration."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
from statistics import fmean
from threading import RLock

from .domain import DomainAnalysis, DomainContext
from .recursive import RecursiveCycleRecord, RecursiveIntelligenceCycle
from .registry import DomainRegistry


@dataclass(frozen=True, slots=True)
class NetworkAnalysis:
    subject: str
    domain_analyses: tuple[DomainAnalysis, ...]
    recursive_cycle: RecursiveCycleRecord
    confidence: float


@dataclass(slots=True)
class SPARTANNetwork:
    """Distributed recursive intelligence network that powers SPAN™."""

    registry: DomainRegistry
    recursive_cycle: RecursiveIntelligenceCycle
    _started: bool = False
    _lock: RLock = field(default_factory=RLock, repr=False)

    @property
    def name(self) -> str:
        return "spartan"

    @property
    def is_started(self) -> bool:
        with self._lock:
            return self._started

    def start(self) -> None:
        with self._lock:
            self._started = True

    def stop(self) -> None:
        with self._lock:
            self._started = False

    def analyze(
        self,
        context: DomainContext,
        domains: Iterable[str] | None = None,
    ) -> NetworkAnalysis:
        if not self.is_started:
            raise RuntimeError("SPARTAN must be started before analysis")

        selected = (
            tuple(domains)
            if domains is not None
            else tuple(self.registry.names())
        )

        analyses = tuple(
            self.registry.resolve(name).analyze(context)
            for name in selected
        )

        confidence = (
            fmean(item.confidence for item in analyses)
            if analyses
            else 0.0
        )

        return NetworkAnalysis(
            subject=context.subject,
            domain_analyses=analyses,
            recursive_cycle=self.recursive_cycle.execute(context.subject),
            confidence=confidence,
        )
