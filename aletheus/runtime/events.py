from __future__ import annotations

import uuid
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from aletheus.time_utils import utc_now_iso


@dataclass
class RuntimeEvent:
    event_type: str
    payload: dict[str, Any]
    source: str = "system"
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=lambda: utc_now_iso())

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "source": self.source,
            "payload": self.payload,
            "created_at": self.created_at,
        }


class EventBus:
    def __init__(self) -> None:
        self.events: list[RuntimeEvent] = []
        self.subscribers: dict[str, list[Callable[[RuntimeEvent], None]]] = {}

    def publish(
        self, event_type: str, payload: dict[str, Any], source: str = "system"
    ) -> RuntimeEvent:
        event = RuntimeEvent(event_type=event_type, payload=payload, source=source)
        self.events.append(event)
        for handler in self.subscribers.get(event_type, []):
            handler(event)
        for handler in self.subscribers.get("*", []):
            handler(event)
        return event

    def subscribe(
        self, event_type: str, handler: Callable[[RuntimeEvent], None]
    ) -> None:
        self.subscribers.setdefault(event_type, []).append(handler)

    def recent(self, limit: int = 100) -> list[dict[str, Any]]:
        return [event.to_dict() for event in self.events[-limit:]]

    def count(self) -> int:
        return len(self.events)
