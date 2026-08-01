from __future__ import annotations

from typing import ClassVar

from .models import ExperienceAction, ExperienceSurface, HydrationSource, SurfaceKind


class Engine:
    SURFACE: ClassVar[ExperienceSurface] = ExperienceSurface(
        surface_id="mission_control",
        display_name="Mission Control™",
        description="Operational command center for active acquisitions, automations, alerts, scans, imports, and A•3ye tasks.",
        kind=SurfaceKind.ROOM,
        hydration_sources=(
            HydrationSource("Mission Engine"),
            HydrationSource("Mission Scheduler"),
            HydrationSource("Production Telemetry Intelligence"),
            HydrationSource("Marketplace Intelligence"),
            HydrationSource("A•3ye Task Runtime"),
        ),
        overlays=(
            "A•3ye",
            "Evidence",
            "Memory",
            "Predictive",
        ),
        actions=(
            ExperienceAction(
                "create_mission", "Create Mission", "CREATE_MISSION", False, None
            ),
            ExperienceAction(
                "pause_mission", "Pause Mission", "PAUSE_MISSION", True, None
            ),
            ExperienceAction("open_alert", "Open Alert", "OPEN_ALERT", False, None),
        ),
        metadata={
            "regions": (
                "active_missions",
                "alerts",
                "saved_searches",
                "market_scans",
                "automations",
                "imports",
                "exports",
                "notifications",
                "a3ye_tasks",
            )
        },
    )

    def surface(self) -> ExperienceSurface:
        return self.SURFACE
