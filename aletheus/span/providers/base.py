"""Provider contracts and result envelopes for SPAN™."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping

from ..evidence_store import EvidenceRecord


@dataclass(frozen=True, slots=True)
class ProviderContext:
    """Execution context supplied to evidence providers."""

    root: Path
    run_id: str
    configuration: Mapping[str, Any] = field(default_factory=dict)

    def resolve(self, value: str | Path) -> Path:
        candidate = Path(value)
        return candidate if candidate.is_absolute() else self.root / candidate


@dataclass(frozen=True, slots=True)
class ProviderResult:
    """Normalized provider execution result."""

    provider: str
    version: str
    records: tuple[EvidenceRecord, ...]
    started_at: datetime
    completed_at: datetime
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def duration_ms(self) -> float:
        return round((self.completed_at - self.started_at).total_seconds() * 1000, 3)

    def to_dict(self) -> dict[str, Any]:
        return {
            "provider": self.provider,
            "version": self.version,
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat(),
            "duration_ms": self.duration_ms,
            "record_count": len(self.records),
            "metadata": dict(self.metadata),
        }


class Provider(ABC):
    """Base class for bounded SPAN evidence providers."""

    name = "provider"
    version = "1.0.0"
    description = ""

    @abstractmethod
    def collect(self, context: ProviderContext) -> Iterable[EvidenceRecord]:
        """Collect normalized architectural evidence."""

    def run(self, context: ProviderContext) -> ProviderResult:
        started = datetime.now(timezone.utc)
        records = tuple(self.collect(context))
        completed = datetime.now(timezone.utc)
        return ProviderResult(
            provider=self.name,
            version=self.version,
            records=records,
            started_at=started,
            completed_at=completed,
        )
