from __future__ import annotations

from typing import ClassVar

from .models import CompositionResult, ExperienceSession, ExperienceSurface


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
        }
    )

    def compose(
        self, session: ExperienceSession, surface: ExperienceSurface
    ) -> CompositionResult:
        resolved = tuple(x for x in surface.overlays if x in self.PLATFORM_OVERLAYS)
        rejected = sorted(set(surface.overlays).difference(resolved))
        warnings = (
            ("Rejected non-platform overlays: " + ", ".join(rejected),)
            if rejected
            else ()
        )
        return CompositionResult(
            session, surface, resolved, surface.hydration_sources, warnings
        )
