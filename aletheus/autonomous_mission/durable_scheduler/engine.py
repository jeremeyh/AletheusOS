from __future__ import annotations

import heapq
from dataclasses import dataclass
from typing import Any, ClassVar

from .models import MissionSpec


@dataclass(order=True, slots=True)
class _Scheduled:
    sort_key: tuple[int, int]
    mission_id: str


class Engine:
    """Weighted durable scheduler using priority and next-run ordering."""

    VERSION: ClassVar[str] = "33.3.0"

    def __init__(self) -> None:
        self._queue: list[_Scheduled] = []

    def schedule(self, mission: MissionSpec, next_run_at: int) -> dict[str, Any]:
        if next_run_at < 0:
            raise ValueError("next_run_at cannot be negative.")
        item = _Scheduled((-mission.priority, next_run_at), mission.mission_id)
        heapq.heappush(self._queue, item)
        return {
            "missionId": mission.mission_id,
            "scheduled": True,
            "nextRunAt": next_run_at,
            "durableIntent": True,
        }

    def pop_next(self) -> str | None:
        if not self._queue:
            return None
        return heapq.heappop(self._queue).mission_id

    def evaluate(self, mission: MissionSpec) -> dict[str, Any]:
        return self.schedule(mission, 0)
