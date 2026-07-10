from __future__ import annotations

from aletheus.time_utils import utc_now, utc_now_iso

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List
import uuid


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

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__


@dataclass
class ExecutiveRisk:
    title: str
    description: str
    severity: str = "medium"
    confidence: float = 0.75
    risk_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__


@dataclass
class ExecutiveBrief:
    title: str
    summary: str
    highlights: List[str]
    recommendations: List[Dict[str, Any]]
    risks: List[Dict[str, Any]]
    brief_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__
