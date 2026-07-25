"""Event bus statistics model."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EventBusStatistics:
    """Immutable snapshot of event bus activity."""

    published: int
    delivered: int
    failed_deliveries: int
    subscriber_count: int
    history_size: int
    next_sequence: int
    events_by_kind: Mapping[str, int]
    last_event_id: str | None
    last_event_kind: str | None

    def to_dict(self) -> dict[str, object]:
        return {
            "published": self.published,
            "delivered": self.delivered,
            "failed_deliveries": self.failed_deliveries,
            "subscriber_count": self.subscriber_count,
            "history_size": self.history_size,
            "next_sequence": self.next_sequence,
            "events_by_kind": dict(
                self.events_by_kind
            ),
            "last_event_id": self.last_event_id,
            "last_event_kind": self.last_event_kind,
        }
