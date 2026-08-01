from __future__ import annotations

from dataclasses import dataclass

from .models import DeterminationVector


@dataclass(frozen=True)
class Weights:
    alpha: float = 0.35
    beta: float = 0.35
    gamma: float = 0.15
    delta: float = 0.15

    def validate(self) -> None:
        if abs(self.alpha + self.beta + self.gamma + self.delta - 1.0) > 1e-9:
            raise ValueError("Balance Engine weights must sum to 1.0")


class Engine:
    def score(
        self,
        *,
        veracity: float,
        governance: float,
        predictive_stability: float,
        principle_x: float,
        entropy: float,
        weights: Weights | None = None,
    ) -> DeterminationVector:
        active = weights or Weights()
        active.validate()
        overall = (
            active.alpha * veracity
            + active.beta * governance
            + active.gamma * predictive_stability
            + active.delta * principle_x
        )
        overall *= 1.0 - min(1.0, max(0.0, entropy)) * 0.25
        return DeterminationVector(
            veracity, governance, predictive_stability, principle_x, entropy, overall
        ).bounded()
