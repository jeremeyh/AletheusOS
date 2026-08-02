from __future__ import annotations

from difflib import SequenceMatcher
from typing import Any, ClassVar

from .models import MissionSpec


class Engine:
    """Detects relistings and recurrence using bounded similarity evidence."""

    VERSION: ClassVar[str] = "33.10.0"

    def similarity(self, first: dict[str, Any], second: dict[str, Any]) -> float:
        keys = sorted(set(first) | set(second))
        left = "|".join(f"{key}={first.get(key, '')}" for key in keys)
        right = "|".join(f"{key}={second.get(key, '')}" for key in keys)
        return SequenceMatcher(None, left, right).ratio()

    def detect(
        self,
        first: dict[str, Any],
        second: dict[str, Any],
        threshold: float = 0.92,
    ) -> dict[str, Any]:
        score = self.similarity(first, second)
        return {
            "relistingDetected": score >= threshold,
            "similarity": round(score, 6),
            "threshold": threshold,
        }

    def evaluate(self, mission: MissionSpec) -> dict[str, Any]:
        return self.detect(
            {"mission": mission.mission_id, "objective": mission.objective},
            {"mission": mission.mission_id, "objective": mission.objective},
        )
