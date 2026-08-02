from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class PlanState(StrEnum):
    DRAFT = "DRAFT"
    ANALYZED = "ANALYZED"
    AWAITING_AUTHORIZATION = "AWAITING_AUTHORIZATION"
    AUTHORIZED = "AUTHORIZED"
    BLOCKED = "BLOCKED"


class RiskBand(StrEnum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass(frozen=True, slots=True)
class StrategicObjective:
    objective_id: str
    title: str
    value: float = 0.5
    urgency: float = 0.5
    constitutional_weight: float = 1.0
    deadline_epoch: int | None = None
    constraints: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class MissionCandidate:
    mission_id: str
    objective_id: str
    estimated_value: float = 0.0
    urgency: float = 0.0
    resource_cost: float = 0.0
    risk: float = 0.0
    confidence: float = 0.5
    dependencies: tuple[str, ...] = ()
    required_resources: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class StrategyPolicy:
    require_human_authorization: bool = True
    max_risk: float = 0.65
    max_resource_commitment: float = 1_000_000.0
    allowed_actions: tuple[str, ...] = ("OBSERVE", "ANALYZE", "RECOMMEND")
    prohibited_actions: tuple[str, ...] = ("SILENT_COMMITMENT",)
    constitutional_principles: tuple[str, ...] = (
        "TRUTH",
        "INTEGRITY",
        "HUMILITY",
        "JUSTICE",
        "WISDOM",
        "HUMAN_AUTHORITY",
    )


@dataclass(frozen=True, slots=True)
class AgentRecommendation:
    agent_id: str
    recommendation: str
    confidence: float
    evidence_ids: tuple[str, ...] = ()
    risk: float = 0.0


@dataclass(frozen=True, slots=True)
class ResourceCapacity:
    resource_id: str
    capacity: float
    committed: float = 0.0
    unit_cost: float = 1.0
    security_classification: str = "INTERNAL"


@dataclass(frozen=True, slots=True)
class TimelineTask:
    task_id: str
    duration: float
    dependencies: tuple[str, ...] = ()
    earliest_start: float = 0.0
    deadline: float | None = None
    priority: float = 0.5
