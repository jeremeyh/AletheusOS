from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(slots=True)
class TimelineEntry:
    event_type: str
    source: str
    message: str = ""
    payload: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(
        default_factory=lambda: datetime.now(UTC).isoformat()
    )

    def to_dict(self):
        return {
            "event_type": self.event_type,
            "source": self.source,
            "message": self.message,
            "payload": self.payload,
            "timestamp": self.timestamp,
        }
