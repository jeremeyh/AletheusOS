from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class ObservatoryAlert:
    code: str
    severity: str
    message: str
    evidence: tuple[str, ...] = ()


@dataclass(slots=True)
class ObservatoryReport:
    generated_at: str
    health_score: float
    readiness: str
    authority_coverage: float
    unresolved_modules: int
    execution_units: int
    alerts: list[ObservatoryAlert] = field(default_factory=list)
    provenance: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
