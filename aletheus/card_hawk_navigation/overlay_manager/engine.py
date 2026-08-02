from __future__ import annotations

from dataclasses import replace
from typing import ClassVar

from .models import NavigationContext


class Engine:
    PLATFORM_OVERLAYS: ClassVar[frozenset[str]] = frozenset(
        {
            "A•3ye",
            "THORᵡ",
            "Council",
            "Evidence",
            "Knowledge",
            "Reason",
            "Memory",
            "Predictive",
            "Temporal",
            "Truth",
            "Principle X",
            "Balance",
            "Radar",
            "Signal",
        }
    )

    def open(self, context: NavigationContext, overlay: str) -> NavigationContext:
        if overlay not in self.PLATFORM_OVERLAYS:
            raise KeyError(f"Unknown platform overlay: {overlay}")
        return (
            context
            if overlay in context.overlays
            else replace(context, overlays=context.overlays + (overlay,))
        )

    def close(self, context: NavigationContext, overlay: str) -> NavigationContext:
        return replace(
            context, overlays=tuple(x for x in context.overlays if x != overlay)
        )
