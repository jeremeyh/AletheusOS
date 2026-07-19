from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4

from .enums import MissionState


@dataclass(slots=True, frozen=True)
class MissionStep:
    name: str
    description: str = ""


@dataclass(slots=True)
class MissionExecution:

    id: UUID = field(default_factory=uuid4)

    state: MissionState = MissionState.CREATED

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    started_at: datetime | None = None

    completed_at: datetime | None = None

    error: str | None = None
