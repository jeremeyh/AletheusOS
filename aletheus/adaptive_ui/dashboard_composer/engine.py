from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import ClassVar


class Engine:
    PRESETS: ClassVar[Mapping[str, tuple[str, ...]]] = MappingProxyType(
        {
            "MORNING": (
                "mission_control",
                "field_vision",
                "scoreboard",
            ),
            "RESEARCH": (
                "scouting_report",
                "game_film",
                "evidence",
            ),
            "NEGOTIATION": (
                "war_room",
                "marketplace",
                "thorx",
                "council",
            ),
            "COLLECTION": (
                "vault",
                "gallery",
                "chronicle",
                "registry",
            ),
        }
    )

    def compose(self, mode: str) -> tuple[str, ...]:
        normalized = mode.upper()
        if normalized not in self.PRESETS:
            raise KeyError(f"Unknown adaptive dashboard mode: {mode}")
        return self.PRESETS[normalized]
