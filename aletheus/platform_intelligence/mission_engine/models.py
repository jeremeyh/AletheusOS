"""Immutable models for the Constitutional Mission Engine."""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import UTC, datetime
from enum import StrEnum
from types import MappingProxyType
from typing import Any, Mapping
from uuid import UUID, uuid4


class ConstitutionalMissionPriority(StrEnum):
    """Canonical mission priority."""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class ConstitutionalMissionState(StrEnum):
    """Mission lifecycle owned by the Mission Engine."""

    CREATED = "created"
    BLOCKED = "blocked"
    READY = "ready"
    SCHEDULED = "scheduled"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


_TERMINAL_STATES = frozenset(
    {
        ConstitutionalMissionState.COMPLETED,
        ConstitutionalMissionState.FAILED,
        ConstitutionalMissionState.CANCELLED,
    }
)


@dataclass(frozen=True, slots=True)
class ConstitutionalMission:
    """Immutable constitutional mission."""

    mission_id: UUID
    address: str
    title: str
    objective: str
    description: str
    priority: ConstitutionalMissionPriority
    state: ConstitutionalMissionState
    dependencies: frozenset[str]
    required_evidence: tuple[str, ...]
    owner: str
    authority: str
    created_at: datetime
    modified_at: datetime
    metadata: Mapping[str, Any]
    failure_reason: str | None = None

    def __post_init__(self) -> None:
        if self.created_at.tzinfo is None:
            raise ValueError(
                "created_at must include timezone information."
            )

        if self.modified_at.tzinfo is None:
            raise ValueError(
                "modified_at must include timezone information."
            )

        object.__setattr__(
            self,
            "created_at",
            self.created_at.astimezone(UTC),
        )
        object.__setattr__(
            self,
            "modified_at",
            self.modified_at.astimezone(UTC),
        )
        object.__setattr__(
            self,
            "metadata",
            MappingProxyType(dict(self.metadata)),
        )

    @classmethod
    def create(
        cls,
        *,
        address: str,
        title: str,
        objective: str,
        description: str = "",
        priority: ConstitutionalMissionPriority = (
            ConstitutionalMissionPriority.NORMAL
        ),
        dependencies: (
            set[str]
            | frozenset[str]
            | tuple[str, ...]
            | list[str]
            | None
        ) = None,
        required_evidence: (
            tuple[str, ...]
            | list[str]
            | None
        ) = None,
        owner: str = "Platform Intelligence",
        authority: str = "AletheusOS Constitution",
        metadata: Mapping[str, Any] | None = None,
        mission_id: UUID | None = None,
        created_at: datetime | None = None,
    ) -> "ConstitutionalMission":
        normalized_address = address.strip().lower()

        if not normalized_address:
            raise ValueError(
                "Mission address cannot be empty."
            )

        dependency_set = frozenset(
            dependency.strip().lower()
            for dependency in (dependencies or ())
        )

        if normalized_address in dependency_set:
            raise ValueError(
                "A mission cannot depend on itself."
            )

        now = created_at or datetime.now(UTC)

        return cls(
            mission_id=mission_id or uuid4(),
            address=normalized_address,
            title=title.strip(),
            objective=objective.strip(),
            description=description.strip(),
            priority=priority,
            state=(
                ConstitutionalMissionState.CREATED
            ),
            dependencies=dependency_set,
            required_evidence=tuple(
                required_evidence or ()
            ),
            owner=owner.strip(),
            authority=authority.strip(),
            created_at=now,
            modified_at=now,
            metadata=MappingProxyType(
                dict(metadata or {})
            ),
        )

    @property
    def terminal(self) -> bool:
        return self.state in _TERMINAL_STATES

    def with_state(
        self,
        state: ConstitutionalMissionState,
        *,
        failure_reason: str | None = None,
        modified_at: datetime | None = None,
    ) -> "ConstitutionalMission":
        return replace(
            self,
            state=state,
            failure_reason=failure_reason,
            modified_at=(
                modified_at or datetime.now(UTC)
            ),
        )

    def to_snapshot(self) -> dict[str, Any]:
        return {
            "mission_id": str(self.mission_id),
            "address": self.address,
            "title": self.title,
            "objective": self.objective,
            "description": self.description,
            "priority": self.priority.value,
            "state": self.state.value,
            "dependencies": sorted(
                self.dependencies
            ),
            "required_evidence": list(
                self.required_evidence
            ),
            "owner": self.owner,
            "authority": self.authority,
            "created_at": self.created_at.isoformat(),
            "modified_at": self.modified_at.isoformat(),
            "metadata": dict(self.metadata),
            "failure_reason": self.failure_reason,
        }


@dataclass(frozen=True, slots=True)
class MissionEngineStatistics:
    """Immutable mission-engine statistics."""

    total: int
    created: int
    blocked: int
    ready: int
    scheduled: int
    running: int
    completed: int
    failed: int
    cancelled: int
    dependency_edges: int

    def to_dict(self) -> dict[str, int]:
        return {
            "total": self.total,
            "created": self.created,
            "blocked": self.blocked,
            "ready": self.ready,
            "scheduled": self.scheduled,
            "running": self.running,
            "completed": self.completed,
            "failed": self.failed,
            "cancelled": self.cancelled,
            "dependency_edges": (
                self.dependency_edges
            ),
        }
