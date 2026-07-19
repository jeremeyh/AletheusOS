"""Shared domain models for SPAN™.

The types in this module form the stable contract shared by evidence
providers, analyzers, the knowledge graph, orchestration, and reporting.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Iterable, Mapping
from uuid import uuid4

DEFAULT_EXCLUDE_NAMES = frozenset(
    {".git", ".venv", "venv", "__pycache__", ".mypy_cache", ".pytest_cache"}
)


def utc_now_iso() -> str:
    """Return a timezone-aware UTC timestamp in ISO-8601 format."""
    return datetime.now(timezone.utc).isoformat()


class FindingSeverity(str, Enum):
    """Canonical finding severity levels."""

    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True, slots=True)
class SourceLocation:
    """A location inside a repository artifact."""

    path: str
    line: int | None = None
    column: int | None = None
    symbol: str | None = None

    @classmethod
    def from_path(
        cls,
        path: str | Path,
        *,
        line: int | None = None,
        column: int | None = None,
        symbol: str | None = None,
    ) -> "SourceLocation":
        return cls(str(path), line=line, column=column, symbol=symbol)


@dataclass(frozen=True, slots=True)
class Evidence:
    """A structured, immutable architectural observation."""

    kind: str
    source: str
    target: str | None = None
    confidence: float = 1.0
    location: SourceLocation | None = None
    attributes: Mapping[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid4()))
    observed_at: str = field(default_factory=utc_now_iso)

    def __post_init__(self) -> None:
        if not self.kind.strip():
            raise ValueError("Evidence kind cannot be empty")
        if not self.source.strip():
            raise ValueError("Evidence source cannot be empty")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Evidence confidence must be between 0.0 and 1.0")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class Finding:
    """An analyzer conclusion supported by evidence."""

    analyzer: str
    category: str
    title: str
    description: str
    severity: FindingSeverity = FindingSeverity.INFO
    confidence: float = 1.0
    evidence_ids: tuple[str, ...] = ()
    recommendation: str | None = None
    attributes: Mapping[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self) -> None:
        if not self.analyzer.strip():
            raise ValueError("Finding analyzer cannot be empty")
        if not self.title.strip():
            raise ValueError("Finding title cannot be empty")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Finding confidence must be between 0.0 and 1.0")

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["severity"] = self.severity.value
        return data


@dataclass(frozen=True, slots=True)
class Metric:
    """A named architectural fitness measurement."""

    name: str
    value: float
    unit: str = "count"
    description: str = ""
    attributes: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class GraphNode:
    """A node in the SPAN architectural knowledge graph."""

    id: str
    kind: str
    label: str
    attributes: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class GraphEdge:
    """A directed relationship in the architectural knowledge graph."""

    source: str
    target: str
    kind: str
    attributes: Mapping[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid4()))

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class AnalyzerResult:
    """The normalized result returned by every SPAN analyzer."""

    analyzer: str
    version: str
    findings: list[Finding] = field(default_factory=list)
    evidence: list[Evidence] = field(default_factory=list)
    metrics: list[Metric] = field(default_factory=list)
    started_at: str = field(default_factory=utc_now_iso)
    completed_at: str | None = None
    error: str | None = None

    @property
    def succeeded(self) -> bool:
        return self.error is None

    def complete(self) -> "AnalyzerResult":
        self.completed_at = utc_now_iso()
        return self

    def to_dict(self) -> dict[str, Any]:
        return {
            "analyzer": self.analyzer,
            "version": self.version,
            "succeeded": self.succeeded,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "error": self.error,
            "findings": [item.to_dict() for item in self.findings],
            "evidence": [item.to_dict() for item in self.evidence],
            "metrics": [item.to_dict() for item in self.metrics],
        }


@dataclass(frozen=True, slots=True)
class AnalysisContext:
    """Repository-scoped inputs supplied to analyzers."""

    repository_root: Path
    include_paths: tuple[Path, ...] = ()
    exclude_names: frozenset[str] = DEFAULT_EXCLUDE_NAMES
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        repository_root: str | Path,
        *,
        include_paths: Iterable[str | Path] | None = None,
        exclude_names: Iterable[str] | None = None,
        metadata: Mapping[str, Any] | None = None,
    ) -> "AnalysisContext":
        root = Path(repository_root).expanduser().resolve()
        includes = tuple(Path(item) for item in (include_paths or ()))
        excludes = DEFAULT_EXCLUDE_NAMES if exclude_names is None else frozenset(exclude_names)
        return cls(root, includes, excludes, metadata or {})
