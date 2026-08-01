from __future__ import annotations

from dataclasses import asdict, dataclass

from .models import ConstitutionalState


@dataclass(frozen=True)
class Physics:
    mass: float
    gravity: float
    temperature: float
    rigidity: float
    viscosity: float
    turbulence: float
    luminosity: float
    elasticity: float


class Engine:
    def solve(self, state: ConstitutionalState) -> Physics:
        s = state.bounded()
        mass = s.veracity * s.consensus * s.provenance * (0.5 + 0.5 * s.crypto)
        rigidity = min(1.0, 0.5 * s.veracity + 0.3 * s.consensus + 0.2 * s.crypto)
        return Physics(
            mass,
            min(1.0, 0.55 * mass + 0.45 * s.priority),
            min(1.0, 0.65 * s.risk + 0.35 * (1 - s.freshness)),
            rigidity,
            min(1.0, 0.6 * (1 - s.confidence) + 0.4 * s.cognitive_load),
            min(1.0, 0.7 * s.entropy + 0.3 * (1 - s.consensus)),
            min(1.0, 0.6 * s.priority + 0.4 * s.freshness),
            min(1.0, 0.65 * (1 - rigidity) + 0.35 * s.confidence),
        )

    def report(self, state: ConstitutionalState) -> dict[str, float]:
        return asdict(self.solve(state))
