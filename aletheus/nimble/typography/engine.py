from __future__ import annotations

from .models import PrimitiveDefinition


class Engine:
    NAMES = ("Display", "Heading", "Body", "Caption", "Telemetry", "Code", "Label")

    def catalog(self) -> tuple[PrimitiveDefinition, ...]:
        return tuple(
            PrimitiveDefinition(
                name=n,
                layer="typography",
                purpose=f"Canonical {n} typography primitive.",
                props=("as", "scale", "weight", "tone", "truncate"),
            )
            for n in self.NAMES
        )
