from __future__ import annotations

from dataclasses import asdict, dataclass

from .models import ConstitutionalState


@dataclass(frozen=True)
class Assessment:
    reason_density: float
    evidence_mass: float
    analytical_breadth: float
    contradiction_resolution: float
    governance_weight: float
    confidence: float
    determination_not_fact: bool = True


class Engine:
    def assess(
        self,
        state: ConstitutionalState,
        *,
        evidence_mass: float,
        analytical_breadth: float,
        contradiction_resolution: float,
    ) -> Assessment:
        s = state.bounded()
        e = min(1, max(0, evidence_mass))
        b = min(1, max(0, analytical_breadth))
        c = min(1, max(0, contradiction_resolution))
        g = 0.45 * s.consensus + 0.30 * s.provenance + 0.25 * s.crypto
        d = 0.28 * e + 0.20 * b + 0.17 * c + 0.20 * g + 0.15 * s.confidence
        return Assessment(min(1, d), e, b, c, min(1, g), s.confidence)

    def report(self, *args, **kwargs) -> dict[str, object]:
        return asdict(self.assess(*args, **kwargs))
