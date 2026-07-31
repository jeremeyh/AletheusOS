"""Optimization models."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class OptimizationCandidate:
    candidate_id: str
    category: str
    title: str
    severity: str
    effort: str
    risk: str
    confidence: float
    expected_health_gain: float
    priority_score: float
    evidence: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class WorkPackage:
    package_id: str
    title: str
    phase: int
    category: str
    candidate_ids: tuple[str, ...]
    estimated_effort: str
    risk: str
    expected_health_gain: float


@dataclass(slots=True)
class OptimizationPlan:
    generated_at: str
    current_health_score: float
    readiness: str
    candidates: list[OptimizationCandidate] = field(default_factory=list)
    work_packages: list[WorkPackage] = field(default_factory=list)
    quick_wins: list[str] = field(default_factory=list)
    abstentions: list[str] = field(default_factory=list)
    provenance: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
