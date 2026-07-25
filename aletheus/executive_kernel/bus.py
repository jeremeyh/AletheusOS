from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


class ExecutiveBusEventType(str, Enum):
    KERNEL_REGISTERED = "kernel_registered"
    CAPABILITY_REGISTERED = "capability_registered"
    POLICY_REGISTERED = "policy_registered"
    DECISION_REQUESTED = "decision_requested"
    DECISION_COMPLETED = "decision_completed"
    RUNTIME_ATTACHED = "runtime_attached"
    EXECUTIVE_STATUS = "executive_status"
    CUSTOM = "custom"


@dataclass(slots=True)
class ExecutiveBusEvent:
    event_type: ExecutiveBusEventType
    source: str
    payload: dict[str, Any] = field(default_factory=dict)
    event_id: str | None = None
    timestamp: str = field(default_factory=utc_now)


class ExecutiveBus:
    """
    Executive orchestration bus.

    Decouples executive components without becoming a runtime event bus.
    """

    def __init__(self) -> None:
        self._subscribers: dict[
            ExecutiveBusEventType,
            list[Callable[[ExecutiveBusEvent], None]],
        ] = {}
        self._history: list[ExecutiveBusEvent] = []

    def subscribe(
        self,
        event_type: ExecutiveBusEventType,
        handler: Callable[[ExecutiveBusEvent], None],
    ) -> None:
        self._subscribers.setdefault(event_type, []).append(handler)

    def publish(self, event: ExecutiveBusEvent) -> None:
        self._history.append(event)

        for handler in self._subscribers.get(event.event_type, []):
            handler(event)

        for handler in self._subscribers.get(ExecutiveBusEventType.CUSTOM, []):
            handler(event)

    def history(self) -> list[ExecutiveBusEvent]:
        return list(self._history)

    def recent(self, limit: int = 25) -> list[ExecutiveBusEvent]:
        return self._history[-limit:]

    def clear_history(self) -> None:
        self._history.clear()

    def summary(self) -> dict:
        return {
            "bus": "Executive Bus",
            "events_recorded": len(self._history),
            "subscriber_groups": {
                event_type.value: len(handlers)
                for event_type, handlers in self._subscribers.items()
            },
            "recent_events": [
                {
                    "event_type": event.event_type.value,
                    "source": event.source,
                    "timestamp": event.timestamp,
                    "payload": event.payload,
                }
                for event in self.recent(10)
            ],
        }
