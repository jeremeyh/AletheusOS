"""Models for repository cohesion analysis."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class CohesionSignal:
    name: str
    value: float
    note: str


@dataclass(frozen=True, slots=True)
class PackageCohesion:
    package: str
    score: float
    status: str
    modules: int
    internal_edges: int
    inbound_packages: int
    outbound_packages: int
    isolated_modules: int
    cycle_groups: int
    capability_count: int
    owner_count: int
    signals: tuple[CohesionSignal, ...] = ()
    recommendations: tuple[str, ...] = ()


@dataclass(slots=True)
class CohesionReport:
    generated_at: str
    topology_report: str
    dependency_report: str
    average_score: float
    status: str
    packages: list[PackageCohesion] = field(default_factory=list)
    hotspots: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
