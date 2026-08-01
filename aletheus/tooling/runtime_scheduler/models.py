from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime


@dataclass(slots=True)
class ScheduledTask:
    task_id: str
    trigger: str
    due_at: str
    payload: dict[str, object]
    status: str = "scheduled"

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

    @classmethod
    def immediate(
        cls,
        task_id: str,
        trigger: str,
        payload: dict[str, object],
    ) -> ScheduledTask:
        return cls(
            task_id=task_id,
            trigger=trigger,
            due_at=datetime.now(UTC).isoformat(),
            payload=payload,
        )
