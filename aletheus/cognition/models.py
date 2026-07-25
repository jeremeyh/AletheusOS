from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any

from aletheus.time_utils import utc_now_iso


def now() -> str:
    return utc_now_iso()


@dataclass
class Goal:
    title: str
    description: str = ""
    priority: str = "medium"
    status: str = "active"
    owner: str = "Founder"
    application: str = "system"
    goal_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)
    completed_at: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


@dataclass
class Plan:
    goal_id: str
    title: str
    steps: list[str]
    plan_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


@dataclass
class ReasoningSession:
    prompt: str
    conclusion: str
    confidence: float
    evidence: list[str]
    assumptions: list[str]
    risks: list[str]
    recommended_actions: list[str]
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


@dataclass
class Decision:
    title: str
    decision: str
    rationale: str
    confidence: float
    evidence: list[str]
    outcome: str = "pending"
    decision_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__
