"""Analyzer contracts and lifecycle helpers for SPAN™."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Protocol, runtime_checkable

from .finding import Finding


@runtime_checkable
class EvidenceReader(Protocol):
    """Minimal evidence-store protocol required by analyzers."""

    def query(
        self,
        *,
        kind: str | None = None,
        provider: str | None = None,
        source: str | None = None,
        tags: Iterable[str] | None = None,
    ) -> tuple[Any, ...]:
        ...


@dataclass(frozen=True, slots=True)
class AnalyzerContext:
    """Execution context supplied to every analyzer."""

    root: str
    run_id: str
    graph: Any | None = None
    configuration: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class AnalyzerResult:
    """Result envelope returned by every analyzer."""

    analyzer: str
    version: str
    findings: tuple[Finding, ...]
    started_at: datetime
    completed_at: datetime
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def duration_ms(self) -> float:
        return round((self.completed_at - self.started_at).total_seconds() * 1000, 3)

    def to_dict(self) -> dict[str, Any]:
        return {
            "analyzer": self.analyzer,
            "version": self.version,
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat(),
            "duration_ms": self.duration_ms,
            "findings": [finding.to_dict() for finding in self.findings],
            "metadata": dict(self.metadata),
        }


class Analyzer(ABC):
    """Base contract for bounded SPAN analyzers."""

    name = "analyzer"
    version = "1.0.0"
    description = ""
    required_evidence: tuple[str, ...] = ()

    def validate_requirements(self, evidence: EvidenceReader) -> tuple[str, ...]:
        missing: list[str] = []
        for kind in self.required_evidence:
            if not evidence.query(kind=kind):
                missing.append(kind)
        return tuple(missing)

    @abstractmethod
    def analyze(
        self,
        evidence: EvidenceReader,
        context: AnalyzerContext,
    ) -> Iterable[Finding]:
        """Analyze normalized evidence and return findings."""

    def run(
        self,
        evidence: EvidenceReader,
        context: AnalyzerContext,
    ) -> AnalyzerResult:
        started = datetime.now(UTC)
        missing = self.validate_requirements(evidence)
        if missing:
            raise RuntimeError(
                f"{self.name} missing required evidence: {', '.join(missing)}"
            )

        findings = tuple(self.analyze(evidence, context))
        completed = datetime.now(UTC)
        return AnalyzerResult(
            analyzer=self.name,
            version=self.version,
            findings=findings,
            started_at=started,
            completed_at=completed,
        )
