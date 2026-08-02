from __future__ import annotations

from collections import defaultdict
from typing import Any, ClassVar

from .models import MissionSpec, ObservationFrame


class Engine:
    """Temporal graph for entity identity, lineage, and observation history."""

    VERSION: ClassVar[str] = "33.9.0"

    def __init__(self) -> None:
        self._observations: dict[str, list[ObservationFrame]] = defaultdict(list)
        self._links: set[tuple[str, str, str]] = set()

    def append(self, frame: ObservationFrame) -> None:
        self._observations[frame.entity_id].append(frame)

    def link(self, left: str, right: str, relation: str) -> None:
        self._links.add((left, relation, right))

    def history(self, entity_id: str) -> tuple[ObservationFrame, ...]:
        return tuple(
            sorted(
                self._observations.get(entity_id, []),
                key=lambda item: item.timestamp,
            )
        )

    def evaluate(self, mission: MissionSpec) -> dict[str, Any]:
        self.link(mission.mission_id, mission.domain, "BELONGS_TO_DOMAIN")
        return {
            "missionId": mission.mission_id,
            "temporalEntityGraph": True,
            "links": tuple(sorted(self._links)),
        }
