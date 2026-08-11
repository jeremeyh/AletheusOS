from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


def now() -> str:
    return datetime.utcnow().isoformat()


@dataclass
class Entity:
    label: str
    entity_type: str = "generic"
    properties: dict[str, Any] = field(default_factory=dict)
    entity_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


@dataclass
class Relationship:
    source_id: str
    target_id: str
    relationship_type: str
    properties: dict[str, Any] = field(default_factory=dict)
    relationship_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__
