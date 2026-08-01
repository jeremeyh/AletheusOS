from __future__ import annotations

from .models import PrimitiveDefinition


class Engine:
    NAMES = (
        "Meter",
        "Gauge",
        "Signal",
        "Trend",
        "Timeline",
        "Pulse",
        "Spectrum",
        "Status",
        "Instrument",
        "Graph",
        "Radar",
        "Consensus",
    )

    def catalog(self) -> tuple[PrimitiveDefinition, ...]:
        return tuple(
            PrimitiveDefinition(
                name=n,
                layer="visualization",
                purpose=f"Canonical {n} visualization primitive.",
                props=("data", "scale", "label", "thresholds", "accessible_text"),
            )
            for n in self.NAMES
        )
