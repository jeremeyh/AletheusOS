from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any

from aletheus.time_utils import utc_now_iso


def now() -> str:
    return utc_now_iso()


@dataclass
class ExecutiveRecommendation:
    title: str
    recommendation: str
    priority: str = "medium"
    confidence: float = 0.75
    source: str = "executive_intelligence"
    recommendation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


@dataclass
class ExecutiveRisk:
    title: str
    description: str
    severity: str = "medium"
    confidence: float = 0.75
    risk_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


@dataclass
class ExecutiveBrief:
    title: str
    summary: str
    highlights: list[str]
    recommendations: list[dict[str, Any]]
    risks: list[dict[str, Any]]
    brief_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__
