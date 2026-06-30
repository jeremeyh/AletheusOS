from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List
import uuid


def now() -> str:
    return datetime.utcnow().isoformat()


@dataclass
class IntelligenceContext:
    question: str
    runtime: Dict[str, Any]
    memory: Dict[str, Any]
    knowledge: Dict[str, Any]
    semantic: Dict[str, Any]
    planning: Dict[str, Any]
    agents: Dict[str, Any]
    executive: Dict[str, Any]
    copilot: Dict[str, Any]
    applications: Dict[str, Any]
    context_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__


@dataclass
class IntelligenceDecision:
    question: str
    decision: str
    confidence: float
    reasoning: List[str]
    risks: List[str]
    next_actions: List[str]
    decision_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__
