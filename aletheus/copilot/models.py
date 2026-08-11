from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


def now() -> str:
    return datetime.utcnow().isoformat()


@dataclass
class CopilotExchange:
    prompt: str
    response: str
    intent: str = "general"
    actions: list[dict[str, Any]] = field(default_factory=list)
    exchange_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


@dataclass
class CopilotRecommendation:
    title: str
    recommendation: str
    priority: str = "medium"
    confidence: float = 0.8
    source: str = "founder_copilot"
    recommendation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__
