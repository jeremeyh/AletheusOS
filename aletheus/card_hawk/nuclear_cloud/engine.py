from __future__ import annotations

from .models import DeterminationVector


class Engine:
    def project(self, vector: DeterminationVector) -> dict[str, object]:
        density = vector.reason_density
        topology = (
            "CRYSTALLINE_SOLID"
            if density >= 0.98
            else (
                "QUASI_CRYSTALLINE"
                if density >= 0.85
                else "FLUID_REACTIVE" if density >= 0.60 else "NEBULAR_PROBABILITY"
            )
        )
        return {
            "designation": "NUCLEAR_CLOUD",
            "meaning": "ACCUMULATED_REASON_DENSITY",
            "reasonDensity": density,
            "topology": topology,
            "informationMass": (
                vector.veracity * 0.25
                + vector.scarcity * 0.20
                + vector.momentum * 0.15
                + vector.portfolio_fit * 0.15
                + (1.0 - vector.downside_risk) * 0.25
            ),
            "determinationNotFact": True,
        }
