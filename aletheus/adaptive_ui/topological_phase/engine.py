from .models import *


class Engine:
    def resolve(self, v, d):
        v = max(0.0, min(1.0, v))
        if v < 0.6:
            return TopologicalState.NEBULAR_PROBABILITY
        if v >= 0.98:
            return TopologicalState.CRYSTALLINE_SOLID
        if (
            d in {DensityLevel.HIGH_DENSITY_FOCUS, DensityLevel.CRITICAL_CRYSTALLINE}
            and v >= 0.85
        ):
            return TopologicalState.QUASI_CRYSTALLINE
        return TopologicalState.FLUID_REACTIVE

    def phase_scalar(self, v):
        v = max(0.0, min(1.0, v))
        return 0.0 if v < 0.6 else 1.0 if v >= 0.98 else (v - 0.6) / 0.38
