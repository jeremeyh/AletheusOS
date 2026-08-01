from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .models import ConstitutionalState


class Topology(StrEnum):
    NEBULAR = "NEBULAR"
    FLUID = "FLUID"
    QUASI_CRYSTALLINE = "QUASI_CRYSTALLINE"
    CRYSTALLINE_SOLID = "CRYSTALLINE_SOLID"


@dataclass(frozen=True)
class Phase:
    topology: Topology
    displacement: float
    refraction: float
    sharpness: float
    aberration: float
    mutable: bool
    consent_gate: bool
    locked: bool


class Engine:
    def compute(
        self, state: ConstitutionalState, *, previously_locked=False, invalidated=False
    ) -> Phase:
        s = state.bounded()
        if previously_locked and not invalidated:
            return Phase(
                Topology.CRYSTALLINE_SOLID, 0, 1.52, 1, 0.02, False, True, True
            )
        if s.veracity >= 0.98 and s.consensus >= 0.98:
            return Phase(
                Topology.CRYSTALLINE_SOLID, 0, 1.52, 1, 0.02, False, True, True
            )
        if s.veracity >= 0.85:
            return Phase(
                Topology.QUASI_CRYSTALLINE, 0.12, 1.46, 0.8, 0.12, False, True, False
            )
        if s.veracity >= 0.60:
            return Phase(Topology.FLUID, 0.42, 1.33, 0.35, 0.22, True, True, False)
        return Phase(Topology.NEBULAR, 0.85, 1.05, 0, 0.45, True, False, False)
