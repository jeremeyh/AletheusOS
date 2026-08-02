from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from hashlib import sha256
from json import dumps
from typing import Any


class MissionStatus(StrEnum):
    ACTIVATED = "ACTIVATED"
    RUNNING = "RUNNING"
    DEGRADED = "DEGRADED"
    PAUSED = "PAUSED"
    BLOCKED = "BLOCKED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    EXPIRED = "EXPIRED"


class Severity(StrEnum):
    INFO = "INFO"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass(frozen=True, slots=True)
class MissionSnapshot:
    mission_id: str
    objective: str
    status: MissionStatus = MissionStatus.ACTIVATED
    progress: float = 0.0
    confidence: float = 0.0
    risk: float = 0.0
    constitutional_score: float = 1.0
    deadline_epoch: int | None = None
    last_updated_epoch: int = 0
    evidence_epoch: int = 0
    expected_outcomes: tuple[str, ...] = ()
    observed_outcomes: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class OperationalPolicy:
    require_human_authority: bool = True
    minimum_constitutional_score: float = 0.95
    maximum_risk: float = 0.70
    maximum_staleness_seconds: int = 3600
    escalation_threshold: Severity = Severity.HIGH
    allow_self_healing: bool = True
    allow_silent_external_execution: bool = False


@dataclass(frozen=True, slots=True)
class TelemetrySample:
    name: str
    value: float
    timestamp_epoch: int
    dimensions: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class OperationalEvent:
    event_id: str
    mission_id: str
    event_type: str
    severity: Severity
    timestamp_epoch: int
    payload: dict[str, Any] = field(default_factory=dict)


def clamp(value: float, lower: float = 0.0, upper: float = 1.0) -> float:
    return max(lower, min(upper, float(value)))


def stable_digest(*parts: Any) -> str:
    return sha256(dumps(parts, sort_keys=True, default=str).encode()).hexdigest()


def immutable_contract(payload: dict[str, Any], *inputs: Any) -> dict[str, Any]:
    result = dict(payload)
    result["immutableDecisionContract"] = True
    result["humanAuthorityPreserved"] = True
    result["silentExternalExecution"] = False
    result["digest"] = stable_digest(inputs, result)
    return result
