from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


def now() -> str:
    return datetime.utcnow().isoformat()


@dataclass
class SemanticConcept:
    name: str
    concept_type: str = "concept"
    description: str = ""
    aliases: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    concept_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


@dataclass
class SemanticAssertion:
    subject: str
    predicate: str
    object_value: str
    confidence: float = 0.75
    source: str = "aletheus"
    metadata: dict[str, Any] = field(default_factory=dict)
    assertion_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__
