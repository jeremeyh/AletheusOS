from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class MissionStatus(StrEnum):
    DRAFT = "DRAFT"
    VALIDATED = "VALIDATED"
    ACTIVATED = "ACTIVATED"
    SCHEDULED = "SCHEDULED"
    OBSERVING = "OBSERVING"
    EVALUATING = "EVALUATING"
    AWAITING_AUTHORIZATION = "AWAITING_AUTHORIZATION"
    EXECUTING = "EXECUTING"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    EXPIRED = "EXPIRED"
    CANCELLED = "CANCELLED"


@dataclass(frozen=True, slots=True)
class MissionSpec:
    mission_id: str
    objective: str
    domain: str
    budget: float = 0.0
    priority: int = 50
    allowed_resources: tuple[str, ...] = ()
    hard_constraints: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ObservationFrame:
    observation_id: str
    entity_id: str
    source_resource_id: str
    timestamp: int
    payload: dict[str, Any]
    content_hash: str = ""


@dataclass(frozen=True, slots=True)
class AuthorizationGrant:
    grant_id: str
    mission_id: str
    actor_id: str
    scopes: tuple[str, ...]
    issued_at: int
    expires_at: int
    mfa_verified: bool
    signature: str
