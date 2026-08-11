from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


def now() -> str:
    return datetime.utcnow().isoformat()


@dataclass
class FounderJournalEntry:
    title: str
    body: str
    category: str = "general"
    tags: list[str] = field(default_factory=list)
    entry_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


@dataclass
class StrategicObjective:
    title: str
    description: str = ""
    priority: str = "medium"
    status: str = "active"
    application: str = "system"
    objective_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


@dataclass
class FounderNotification:
    title: str
    message: str
    severity: str = "info"
    source: str = "aletheus"
    read: bool = False
    notification_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__
