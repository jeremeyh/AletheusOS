from __future__ import annotations

from typing import ClassVar


class Engine:
    DOCK_ITEMS: ClassVar[tuple[str, ...]] = (
        "A•3ye",
        "THORᵡ",
        "Evidence",
        "Memory",
        "Radar",
        "Scoreboard",
        "Mission",
    )

    def items_for(self, surface_id: str) -> tuple[str, ...]:
        if surface_id == "gallery":
            return ("A•3ye", "Memory", "Mission")
        if surface_id == "war_room":
            return (
                "A•3ye",
                "THORᵡ",
                "Council",
                "Evidence",
                "Reason",
                "Truth",
                "Mission",
            )
        return self.DOCK_ITEMS
