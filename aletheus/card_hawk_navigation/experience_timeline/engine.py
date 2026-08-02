from __future__ import annotations

from typing import ClassVar

from .models import TimelineEvent


class Engine:
    ALLOWED_EVENT_TYPES: ClassVar[frozenset[str]] = frozenset(
        {
            "OBSERVED",
            "SCOUTED",
            "WATCHLISTED",
            "OFFER_SENT",
            "COUNTER_RECEIVED",
            "PURCHASED",
            "VAULTED",
            "VALUE_CHANGED",
            "SOLD",
            "PASSED",
        }
    )

    def append(
        self, timeline: tuple[TimelineEvent, ...], event: TimelineEvent
    ) -> tuple[TimelineEvent, ...]:
        if event.event_type not in self.ALLOWED_EVENT_TYPES:
            raise ValueError(f"Unsupported timeline event: {event.event_type}")
        return timeline + (event,)

    def for_subject(
        self, timeline: tuple[TimelineEvent, ...], subject_id: str
    ) -> tuple[TimelineEvent, ...]:
        return tuple(e for e in timeline if e.subject_id == subject_id)
