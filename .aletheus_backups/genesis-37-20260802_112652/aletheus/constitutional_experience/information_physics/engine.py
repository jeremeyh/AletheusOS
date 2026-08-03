from ..helpers import clamp
from ..models import EvidenceSignal, VeracityPhase


class Engine:
    def informational_mass(self, s: EvidenceSignal) -> float:
        return max(0.0, s.value) * clamp(s.provenance) * clamp(s.consensus)

    def phase(self, v: float) -> VeracityPhase:
        v = clamp(v)
        return (
            VeracityPhase.NEBULAR
            if v < 0.60
            else VeracityPhase.FLUID
            if v < 0.85
            else VeracityPhase.QUASI_CRYSTALLINE
            if v < 0.98
            else VeracityPhase.CRYSTALLINE
        )

    def tension(self, contradiction: float) -> float:
        return clamp(contradiction)
