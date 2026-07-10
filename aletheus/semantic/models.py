from __future__ import annotations

from aletheus.time_utils import utc_now, utc_now_iso

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List
import uuid


def now() -> str:
    return utc_now_iso()


@dataclass
class SemanticConcept:
    name: str
    concept_type: str = "concept"
    description: str = ""
    aliases: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    concept_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__


@dataclass
class SemanticAssertion:
    subject: str
    predicate: str
    object_value: str
    confidence: float = 0.75
    source: str = "aletheus"
    metadata: Dict[str, Any] = field(default_factory=dict)
    assertion_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__
