from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar

from .models import MissionSpec


@dataclass(slots=True)
class Bucket:
    capacity: float
    refill_rate: float
    tokens: float
    updated_at: float


class Engine:
    """Token-bucket polling governance with adaptive mission cadence."""

    VERSION: ClassVar[str] = "33.6.0"

    def consume(self, bucket: Bucket, now: float, cost: float = 1.0) -> bool:
        elapsed = max(0.0, now - bucket.updated_at)
        bucket.tokens = min(
            bucket.capacity,
            bucket.tokens + elapsed * bucket.refill_rate,
        )
        bucket.updated_at = now
        if bucket.tokens < cost:
            return False
        bucket.tokens -= cost
        return True

    def cadence(self, confidence: float, urgency: float) -> int:
        signal = max(0.0, min(1.0, confidence * 0.6 + urgency * 0.4))
        return max(30, int(3600 * (1.0 - signal)))

    def evaluate(self, mission: MissionSpec) -> dict[str, Any]:
        bucket = Bucket(5.0, 1.0, 5.0, 0.0)
        return {
            "missionId": mission.mission_id,
            "pollAllowed": self.consume(bucket, 0.0),
            "nextPollSeconds": self.cadence(0.8, mission.priority / 100),
        }
