from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Plan:
    visual: str
    audio: str
    haptic: str
    spatial: str
    textual_equivalent: bool
    reduced_motion: bool


class Engine:
    def plan(
        self,
        topology: str,
        risk: float,
        cognitive_load: float,
        reduced_motion=False,
        haptics=True,
        audio=True,
    ) -> Plan:
        modes = {
            "NEBULAR": ("diffuse_granular", "soft_diffuse_pulse", "wide_ambient"),
            "FLUID": ("flow_modulation", "rolling_wave", "responsive_field"),
            "QUASI_CRYSTALLINE": ("tonal_lattice", "segmented_ticks", "faceted_focus"),
            "CRYSTALLINE_SOLID": (
                "pure_localized_harmonic",
                "precise_lock",
                "anchored_solid",
            ),
        }
        a, h, s = modes[topology]
        if risk >= 0.80:
            a = "risk_tension_overlay"
        return Plan(
            topology,
            a if audio else "none",
            h if haptics else "none",
            s,
            True,
            reduced_motion or cognitive_load >= 0.80,
        )
