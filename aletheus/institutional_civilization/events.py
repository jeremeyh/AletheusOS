"""Institutional civilization bootstrap events."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4


def _timestamp() -> str:
    return datetime.now(UTC).isoformat()


@dataclass(frozen=True, slots=True)
class CivilizationEvent:
    event_id: str
    event_type: str
    source: str
    payload: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=_timestamp)

    @classmethod
    def create(
        cls,
        event_type: str,
        source: str,
        payload: dict[str, Any] | None = None,
    ) -> "CivilizationEvent":
        return cls(
            event_id=f"CIV-{uuid4().hex[:12].upper()}",
            event_type=event_type,
            source=source,
            payload=payload or {},
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
