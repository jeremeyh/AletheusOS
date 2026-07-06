from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
import uuid


def _timestamp() -> str:
    return datetime.now(UTC).isoformat()


def new_request_id() -> str:
    return f"REQ-{uuid.uuid4().hex[:12].upper()}"


# ============================================================
# Genesis 16
# Foundation Engine
# ============================================================

@dataclass(slots=True)
class FoundationEngine:

    engine_id: str

    name: str

    category: str

    description: str = ""

    aliases: list[str] = field(default_factory=list)

    supported_intents: list[str] = field(default_factory=list)

    required_capabilities: list[str] = field(default_factory=list)

    constitutional_articles: list[str] = field(default_factory=list)

    execution_priority: int = 100

    dependencies: list[str] = field(default_factory=list)

    enabled: bool = True

    metadata: dict = field(default_factory=dict)

    def to_dict(self):

        return {
            "engine_id": self.engine_id,
            "name": self.name,
            "category": self.category,
            "description": self.description,
            "aliases": self.aliases,
            "supported_intents": self.supported_intents,
            "required_capabilities": self.required_capabilities,
            "constitutional_articles": self.constitutional_articles,
            "execution_priority": self.execution_priority,
            "dependencies": self.dependencies,
            "enabled": self.enabled,
            "metadata": self.metadata,
        }

# ============================================================
# Genesis 22
# Foundation Request / Response
# ============================================================

@dataclass(slots=True)
class FoundationRequest:

    request_id: str

    identity: str

    application: str

    intent: str

    query: str

    context: dict = field(default_factory=dict)

    metadata: dict = field(default_factory=dict)

    created_at: str = field(default_factory=_timestamp)

    def to_dict(self):

        return {
            "request_id": self.request_id,
            "identity": self.identity,
            "application": self.application,
            "intent": self.intent,
            "query": self.query,
            "context": self.context,
            "metadata": self.metadata,
            "created_at": self.created_at,
        }


@dataclass(slots=True)
class FoundationResponse:

    request_id: str

    success: bool

    answer: object

    confidence: float = 1.0

    reasoning: list[str] = field(default_factory=list)

    constitutional_articles: list[str] = field(default_factory=list)

    metadata: dict = field(default_factory=dict)

    def to_dict(self):

        return {
            "request_id": self.request_id,
            "success": self.success,
            "answer": self.answer,
            "confidence": self.confidence,
            "reasoning": self.reasoning,
            "constitutional_articles": self.constitutional_articles,
            "metadata": self.metadata,
        }
