from __future__ import annotations

from dataclasses import replace
from typing import ClassVar

from .models import ExperienceSession


class Engine:
    UNIVERSAL_OVERLAYS: ClassVar[frozenset[str]] = frozenset(
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

    def open_overlay(
        self, session: ExperienceSession, overlay_name: str
    ) -> ExperienceSession:
        if overlay_name not in self.UNIVERSAL_OVERLAYS:
            raise KeyError(f"Unknown platform overlay: {overlay_name}")
        if overlay_name in session.overlay_stack:
            return session
        return replace(session, overlay_stack=session.overlay_stack + (overlay_name,))

    def close_overlay(
        self, session: ExperienceSession, overlay_name: str
    ) -> ExperienceSession:
        return replace(
            session,
            overlay_stack=tuple(x for x in session.overlay_stack if x != overlay_name),
        )
