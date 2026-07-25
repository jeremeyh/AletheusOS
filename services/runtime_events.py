from __future__ import annotations

import json
import os
import uuid
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(UTC).isoformat()


@dataclass
class RuntimeEvent:
    event_type: str
    payload: dict[str, Any]
    source: str = "CardHawkOS"
    request_id: str | None = None
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = field(default_factory=utc_now_iso)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class EventStore:
    def __init__(self, path: str = "data/runtime_events.jsonl") -> None:
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)

    def append(self, event: RuntimeEvent) -> None:
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(event.to_dict(), default=str) + "\n")

    def read_recent(self, limit: int = 100) -> list[dict[str, Any]]:
        if not os.path.exists(self.path):
            return []
        with open(self.path, "r", encoding="utf-8") as f:
            lines = f.readlines()[-limit:]
        return [json.loads(line) for line in lines if line.strip()]

    def find_by_type(self, event_type: str, limit: int = 100) -> list[dict[str, Any]]:
        return [e for e in self.read_recent(limit=1000) if e.get("event_type") == event_type][-limit:]
