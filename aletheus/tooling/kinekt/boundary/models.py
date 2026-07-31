"""Models for runtime boundary analysis."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class BoundaryFinding:
    code: str
    severity: str
    source: str
    target: str
    source_layer: str
    target_layer: str
    message: str
    evidence: tuple[str, ...] = ()
    recommendation: str = ""


@dataclass(frozen=True, slots=True)
class PackagePressure:
    package: str
    inbound_edges: int
    outbound_edges: int
    violations: int
    seam_candidates: int
    score: float
    status: str


@dataclass(slots=True)
class BoundaryReport:
    generated_at: str
    dependency_report: str
    cohesion_report: str
    findings: list[BoundaryFinding] = field(default_factory=list)
    package_pressure: list[PackagePressure] = field(default_factory=list)
    unresolved_relationships: int = 0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
