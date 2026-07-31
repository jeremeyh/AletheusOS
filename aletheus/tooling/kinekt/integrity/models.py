"""Models for platform integrity evaluation."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class IntegrityDimension:
    name: str
    score: float
    status: str
    deductions: tuple[str, ...] = ()


@dataclass(slots=True)
class IntegrityReport:
    generated_at: str
    source_repository_report: str
    source_resolution_report: str
    total_score: float
    status: str
    dimensions: list[IntegrityDimension] = field(default_factory=list)
    trend: str = "baseline"
    previous_score: float | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
