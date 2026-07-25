from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any

from aletheus.time_utils import utc_now_iso


def now() -> str:
    return utc_now_iso()


@dataclass
class Forecast:
    title: str
    horizon: str
    summary: str
    confidence: float
    signals: list[str] = field(default_factory=list)
    forecast_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


@dataclass
class Scenario:
    title: str
    premise: str
    expected_outcome: str
    confidence: float
    impacts: list[str] = field(default_factory=list)
    scenario_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


@dataclass
class PredictiveRisk:
    title: str
    description: str
    severity: str = "medium"
    confidence: float = 0.75
    mitigation: str = ""
    risk_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


@dataclass
class PredictiveOpportunity:
    title: str
    description: str
    score: float
    confidence: float
    next_action: str = ""
    opportunity_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


@dataclass
class PredictiveRecommendation:
    title: str
    recommendation: str
    priority: str
    expected_gain: float
    confidence: float
    recommendation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__
