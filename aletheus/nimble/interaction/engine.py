from __future__ import annotations

from .models import PrimitiveDefinition


class Engine:
    NAMES = (
        "Button",
        "Toggle",
        "Segment",
        "Input",
        "Search",
        "Slider",
        "Dropdown",
        "Command",
        "Hotkey",
        "ContextMenu",
    )

    def catalog(self) -> tuple[PrimitiveDefinition, ...]:
        return tuple(
            PrimitiveDefinition(
                name=n,
                layer="interaction",
                purpose=f"Canonical {n} interaction primitive.",
                props=("disabled", "loading", "intent", "size", "aria_label"),
            )
            for n in self.NAMES
        )
