"""Models for constitutional health synthesis."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class HealthDimension:
    name: str
    score: float
    weight: float
    status: str
    evidence: tuple[str, ...] = ()
    risks: tuple[str, ...] = ()


@dataclass(slots=True)
class HealthReport:
    generated_at: str
    total_score: float
    status: str
    readiness: str
    dimensions: list[HealthDimension] = field(default_factory=list)
    top_risks: list[str] = field(default_factory=list)
    provenance: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
