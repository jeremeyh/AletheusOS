from __future__ import annotations

from typing import ClassVar

from .models import WorkspacePriority, WorkspaceRegion


class Engine:
    MODE_LAYOUTS: ClassVar[dict[str, tuple[WorkspaceRegion, ...]]] = {
        "BUYING": (
            WorkspaceRegion("war_room", "war_room", WorkspacePriority.PRIMARY, 1.0),
            WorkspaceRegion(
                "scouting", "scouting_report", WorkspacePriority.SECONDARY, 0.7
            ),
            WorkspaceRegion("field", "field_vision", WorkspacePriority.SECONDARY, 0.6),
        ),
        "RESEARCHING": (
            WorkspaceRegion(
                "scouting", "scouting_report", WorkspacePriority.PRIMARY, 1.0
            ),
            WorkspaceRegion("game_film", "game_film", WorkspacePriority.SECONDARY, 0.8),
        ),
        "MONITORING": (
            WorkspaceRegion("field", "field_vision", WorkspacePriority.PRIMARY, 1.0),
            WorkspaceRegion(
                "mission", "mission_control", WorkspacePriority.SECONDARY, 0.8
            ),
        ),
        "CATALOGING": (
            WorkspaceRegion("vault", "vault", WorkspacePriority.PRIMARY, 1.0),
            WorkspaceRegion("gallery", "gallery", WorkspacePriority.SECONDARY, 0.7),
        ),
    }

    def layout_for(self, mode: str) -> tuple[WorkspaceRegion, ...]:
        key = mode.upper()
        if key not in self.MODE_LAYOUTS:
            raise KeyError(f"Unknown workspace mode: {mode}")
        return self.MODE_LAYOUTS[key]
