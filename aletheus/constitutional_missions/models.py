"""Canonical Constitutional Mission models."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4


def _timestamp() -> str:
    return datetime.now(UTC).isoformat()


def new_mission_id() -> str:
    return f"MISSION-{uuid4().hex[:12].upper()}"


class MissionStatus(StrEnum):
    PLANNED = "planned"
    AUTHORIZED = "authorized"
    READY = "ready"
    RUNNING = "running"
    WAITING = "waiting"
    RECOVERING = "recovering"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    ARCHIVED = "archived"


class MissionCriticality(StrEnum):
    SUPPORTING = "supporting"
    IMPORTANT = "important"
    CRITICAL = "critical"
    CONSTITUTIONAL = "constitutional"


@dataclass(frozen=True, slots=True)
class MissionContract:
    mission_type: str
    purpose: str

    required_institutions: tuple[str, ...]
    required_evidence_types: tuple[str, ...]
    success_criteria: tuple[str, ...]
    failure_criteria: tuple[str, ...]

    governance_required: bool = False
    council_required_on_failure: bool = True

    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ConstitutionalMission:
    mission_id: str
    mission_type: str
    canonical_name: str
    purpose: str
    authority: str
    jurisdiction: str

    contract: MissionContract

    status: MissionStatus = MissionStatus.PLANNED
    criticality: MissionCriticality = MissionCriticality.IMPORTANT

    correlation_id: str = ""
    case_id: str | None = None

    participating_institutions: list[str] = field(default_factory=list)
    evidence: list[dict[str, Any]] = field(default_factory=list)
    event_ids: list[str] = field(default_factory=list)
    failures: list[str] = field(default_factory=list)

    created_at: str = field(default_factory=_timestamp)
    authorized_at: str | None = None
    started_at: str | None = None
    completed_at: str | None = None

    genesis: str = "50"
    version: str = "0.1.0"
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.correlation_id:
            self.correlation_id = self.mission_id

    def to_dict(self) -> dict[str, Any]:
        return {
            "mission_id": self.mission_id,
            "mission_type": self.mission_type,
            "canonical_name": self.canonical_name,
            "purpose": self.purpose,
            "authority": self.authority,
            "jurisdiction": self.jurisdiction,
            "contract": self.contract.to_dict(),
            "status": self.status.value,
            "criticality": self.criticality.value,
            "correlation_id": self.correlation_id,
            "case_id": self.case_id,
            "participating_institutions": list(self.participating_institutions),
            "evidence": list(self.evidence),
            "event_ids": list(self.event_ids),
            "failures": list(self.failures),
            "created_at": self.created_at,
            "authorized_at": self.authorized_at,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "genesis": self.genesis,
            "version": self.version,
            "metadata": dict(self.metadata),
        }
