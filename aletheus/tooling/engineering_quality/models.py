from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class Metric:
    name: str
    score: float
    weight: float = 1.0
    evidence: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Assessment:
    standard: str
    score: float
    status: str
    metrics: tuple[Metric, ...]
    rationale: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "standard": self.standard,
            "score": self.score,
            "status": self.status,
            "metrics": [item.to_dict() for item in self.metrics],
            "rationale": list(self.rationale),
        }
