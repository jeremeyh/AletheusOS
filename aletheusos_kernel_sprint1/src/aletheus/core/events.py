from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from types import MappingProxyType
from typing import Any
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class Event:
    event_type: str
    source: str
    payload: Mapping[str, Any] = field(default_factory=dict)
    correlation_id: UUID | None = None
    id: UUID = field(default_factory=uuid4)
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self):
        if not self.event_type.strip():
            raise ValueError("Event type cannot be empty.")
        if not self.source.strip():
            raise ValueError("Event source cannot be empty.")
        object.__setattr__(self, "payload", MappingProxyType(dict(self.payload)))
