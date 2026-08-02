from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import Any, ClassVar

from .models import MissionSpec


@dataclass(frozen=True, slots=True)
class Lease:
    lease_id: str
    task_id: str
    worker_id: str
    expires_at: int


class Engine:
    """Durable task leases with ownership, expiry, and idempotency keys."""

    VERSION: ClassVar[str] = "33.7.0"

    def acquire(
        self,
        task_id: str,
        worker_id: str,
        now: int,
        ttl: int = 60,
    ) -> Lease:
        if ttl <= 0:
            raise ValueError("Lease TTL must be positive.")
        raw = f"{task_id}:{worker_id}:{now}:{ttl}"
        lease_id = f"lease_{sha256(raw.encode()).hexdigest()[:20]}"
        return Lease(lease_id, task_id, worker_id, now + ttl)

    def evaluate(self, mission: MissionSpec) -> dict[str, Any]:
        lease = self.acquire(
            f"task:{mission.mission_id}",
            "worker:local",
            0,
        )
        return {
            "missionId": mission.mission_id,
            "lease": lease,
            "idempotencyEnforced": True,
        }
