"""Core SPARTAN™ domain contracts and models."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Protocol, runtime_checkable
from uuid import UUID, uuid4


def utc_now() -> datetime:
    return datetime.now(UTC)


@dataclass(frozen=True, slots=True)
class DomainSignal:
    domain: str
    signal_type: str
    statement: str
    confidence: float
    source: str
    observed_at: datetime = field(default_factory=utc_now)
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.domain.strip():
            raise ValueError("Signal domain must not be empty")
        if not self.signal_type.strip():
            raise ValueError("signal_type must not be empty")
        if not self.statement.strip():
            raise ValueError("Signal statement must not be empty")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Signal confidence must be between 0.0 and 1.0")


@dataclass(frozen=True, slots=True)
class DomainContext:
    subject: str
    question: str
    state: Mapping[str, Any] = field(default_factory=dict)
    context_id: UUID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        if not self.subject.strip():
            raise ValueError("Context subject must not be empty")
        if not self.question.strip():
            raise ValueError("Context question must not be empty")


@dataclass(frozen=True, slots=True)
class DomainAnalysis:
    domain: str
    summary: str
    findings: tuple[str, ...]
    signals: tuple[DomainSignal, ...]
    confidence: float
    generated_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if not self.domain.strip():
            raise ValueError("Analysis domain must not be empty")
        if not self.summary.strip():
            raise ValueError("Analysis summary must not be empty")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Analysis confidence must be between 0.0 and 1.0")


@runtime_checkable
class IntelligenceDomain(Protocol):
    @property
    def name(self) -> str:
        """Canonical domain name."""

    def analyze(self, context: DomainContext) -> DomainAnalysis:
        """Analyze the supplied context and return domain-specific intelligence."""
