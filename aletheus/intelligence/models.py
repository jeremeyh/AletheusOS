from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any

from aletheus.time_utils import utc_now_iso


def now() -> str:
    return utc_now_iso()


@dataclass
class IntelligenceContext:
    question: str
    runtime: dict[str, Any]
    memory: dict[str, Any]
    knowledge: dict[str, Any]
    semantic: dict[str, Any]
    planning: dict[str, Any]
    agents: dict[str, Any]
    executive: dict[str, Any]
    copilot: dict[str, Any]
    applications: dict[str, Any]
    context_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


@dataclass
class IntelligenceDecision:
    question: str
    decision: str
    confidence: float
    reasoning: list[str]
    risks: list[str]
    next_actions: list[str]
    decision_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__
