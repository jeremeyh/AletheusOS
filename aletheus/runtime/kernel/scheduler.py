from __future__ import annotations

import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any


def utc_now() -> str:
    return datetime.utcnow().isoformat()


@dataclass
class ScheduledTask:
    scheduled_id: str
    task_id: str
    priority: int = 5
    status: str = "scheduled"
    created_at: str = field(default_factory=utc_now)


class IntelligenceScheduler:
    VERSION = "4.0.0"

    def __init__(self) -> None:
        self.queue: list[ScheduledTask] = []

    def schedule(self, task_id: str, priority: int = 5) -> dict[str, Any]:
        item = ScheduledTask(
            scheduled_id=str(uuid.uuid4()),
            task_id=task_id,
            priority=priority,
        )

        self.queue.append(item)
        self.queue.sort(key=lambda x: x.priority)

        return asdict(item)

    def next(self) -> dict[str, Any]:
        if not self.queue:
            return {"task": None}

        item = self.queue.pop(0)
        item.status = "dispatched"

        return asdict(item)

    def statistics(self) -> dict[str, Any]:
        return {
            "version": self.VERSION,
            "queued": len(self.queue),
            "health": "healthy",
        }


intelligence_scheduler = IntelligenceScheduler()
