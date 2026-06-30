from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List
import uuid


def now() -> str:
    return datetime.utcnow().isoformat()


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

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__


@dataclass
class Plan:
    goal_id: str
    title: str
    steps: List[str]
    plan_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__


@dataclass
class ReasoningSession:
    prompt: str
    conclusion: str
    confidence: float
    evidence: List[str]
    assumptions: List[str]
    risks: List[str]
    recommended_actions: List[str]
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__


@dataclass
class Decision:
    title: str
    decision: str
    rationale: str
    confidence: float
    evidence: List[str]
    outcome: str = "pending"
    decision_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__
