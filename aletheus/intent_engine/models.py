from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4


def now() -> str:
    return datetime.now(UTC).isoformat()


def new_intent_id() -> str:
    return f"INTENT-{uuid4().hex[:12].upper()}"


@dataclass(slots=True)
class Intent:
    intent_id: str
    identity: str
    application: str
    query: str
    intent_type: str
    objective: str
    capability_request: str
    priority: str = "normal"
    confidence: float = 1.0
    constraints: list[str] = field(default_factory=list)
    expected_outcome: str = ""
    context: dict[str, Any] = field(default_factory=dict)
    constitutional_articles: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=now)

    def to_dict(self) -> dict[str, Any]:
        return {
            "intent_id": self.intent_id,
            "identity": self.identity,
            "application": self.application,
            "query": self.query,
            "intent_type": self.intent_type,
            "objective": self.objective,
            "capability_request": self.capability_request,
            "priority": self.priority,
            "confidence": self.confidence,
            "constraints": self.constraints,
            "expected_outcome": self.expected_outcome,
            "context": self.context,
            "constitutional_articles": self.constitutional_articles,
            "created_at": self.created_at,
        }
