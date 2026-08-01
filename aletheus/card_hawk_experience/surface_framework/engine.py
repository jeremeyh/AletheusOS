from __future__ import annotations

from typing import ClassVar

from .models import ExperienceSurface, SurfaceKind


class Engine:
    RESERVED_PLATFORM_OVERLAYS: ClassVar[frozenset[str]] = frozenset(
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

    def validate(self, surface: ExperienceSurface) -> dict[str, object]:
        findings = []
        if not surface.surface_id.strip():
            findings.append("surface_id is required")
        if not surface.display_name.strip():
            findings.append("display_name is required")
        if surface.kind == SurfaceKind.ROOM and not surface.hydration_sources:
            findings.append("room surfaces require hydration sources")
        return {"valid": not findings, "findings": findings}
