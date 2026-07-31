"""Canonical relative-time models for TIME™."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any
from uuid import uuid4


def new_phase_id() -> str:
    return f"PHASE-{uuid4().hex[:12].upper()}"


class PhaseStatus(StrEnum):
    PENDING = "pending"
    ELIGIBLE = "eligible"
    RUNNING = "running"
    WAITING = "waiting"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"
    BLOCKED = "blocked"


@dataclass(frozen=True, slots=True)
class MissionPhaseContract:
    """
    Relative execution contract for one mission phase.

    Dependencies express causal order rather than wall-clock time.
    """

    phase_id: str
    canonical_name: str
    purpose: str

    dependencies: tuple[str, ...] = ()
    participating_institutions: tuple[str, ...] = ()

    required_evidence_types: tuple[str, ...] = ()
    produces: tuple[str, ...] = ()

    completion_criteria: tuple[str, ...] = ()
    failure_criteria: tuple[str, ...] = ()

    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class MissionPhaseState:
    phase_id: str
    status: PhaseStatus = PhaseStatus.PENDING

    relative_position: int | None = None
    attempts: int = 0

    participating_institutions: list[str] = field(default_factory=list)
    evidence: list[dict[str, Any]] = field(default_factory=list)
    failures: list[str] = field(default_factory=list)
    event_ids: list[str] = field(default_factory=list)

    def evidence_types(self) -> set[str]:
        return {item["evidence_type"] for item in self.evidence}

    def to_dict(self) -> dict[str, Any]:
        return {
            "phase_id": self.phase_id,
            "status": self.status.value,
            "relative_position": self.relative_position,
            "attempts": self.attempts,
            "participating_institutions": list(self.participating_institutions),
            "evidence": list(self.evidence),
            "failures": list(self.failures),
            "event_ids": list(self.event_ids),
        }


@dataclass(slots=True)
class MissionTemporalState:
    """
    Relative-time state for one constitutional mission.

    `relative_cursor` is an ordering counter, not a clock.
    """

    mission_id: str
    correlation_id: str

    phases: dict[str, MissionPhaseState] = field(default_factory=dict)

    relative_cursor: int = 0
    completed_order: list[str] = field(default_factory=list)
    failed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "mission_id": self.mission_id,
            "correlation_id": self.correlation_id,
            "relative_cursor": self.relative_cursor,
            "completed_order": list(self.completed_order),
            "failed": self.failed,
            "phases": {
                phase_id: state.to_dict() for phase_id, state in self.phases.items()
            },
        }
