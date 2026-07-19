"""Immutable models for the Constitutional Mission Scheduler."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from types import MappingProxyType
from typing import Any, Mapping
from uuid import UUID, uuid4


class MissionPriority(StrEnum):
    """Canonical mission priority levels."""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class MissionState(StrEnum):
    """Scheduler-owned mission lifecycle states."""

    REGISTERED = "registered"
    WAITING = "waiting"
    READY = "ready"
    QUEUED = "queued"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"
    EXHAUSTED = "exhausted"


_PRIORITY_WEIGHT = {
    MissionPriority.LOW: 10,
    MissionPriority.NORMAL: 20,
    MissionPriority.HIGH: 30,
    MissionPriority.CRITICAL: 40,
}


@dataclass(frozen=True, slots=True)
class RetryPolicy:
    """Deterministic retry policy."""

    max_attempts: int = 1
    initial_delay: timedelta = timedelta(0)
    backoff_multiplier: float = 1.0
    maximum_delay: timedelta | None = None

    def __post_init__(self) -> None:
        if self.max_attempts < 1:
            raise ValueError(
                "max_attempts must be at least one."
            )

        if self.initial_delay < timedelta(0):
            raise ValueError(
                "initial_delay cannot be negative."
            )

        if self.backoff_multiplier < 1.0:
            raise ValueError(
                "backoff_multiplier cannot be below one."
            )

        if (
            self.maximum_delay is not None
            and self.maximum_delay < timedelta(0)
        ):
            raise ValueError(
                "maximum_delay cannot be negative."
            )

    def delay_for_attempt(
        self,
        attempt: int,
    ) -> timedelta:
        if attempt < 1:
            raise ValueError(
                "attempt must be at least one."
            )

        seconds = (
            self.initial_delay.total_seconds()
            * (
                self.backoff_multiplier
                ** max(0, attempt - 1)
            )
        )

        delay = timedelta(seconds=seconds)

        if (
            self.maximum_delay is not None
            and delay > self.maximum_delay
        ):
            return self.maximum_delay

        return delay


@dataclass(frozen=True, slots=True)
class MissionTrigger:
    """Time-based mission trigger."""

    run_at: datetime | None = None
    interval: timedelta | None = None

    def __post_init__(self) -> None:
        if self.run_at is None and self.interval is None:
            raise ValueError(
                "A mission trigger requires run_at or interval."
            )

        if (
            self.run_at is not None
            and self.run_at.tzinfo is None
        ):
            raise ValueError(
                "run_at must include timezone information."
            )

        if (
            self.interval is not None
            and self.interval <= timedelta(0)
        ):
            raise ValueError(
                "interval must be positive."
            )

        if self.run_at is not None:
            object.__setattr__(
                self,
                "run_at",
                self.run_at.astimezone(UTC),
            )

    @classmethod
    def once(
        cls,
        run_at: datetime,
    ) -> "MissionTrigger":
        return cls(run_at=run_at)

    @classmethod
    def recurring(
        cls,
        *,
        interval: timedelta,
        first_run_at: datetime | None = None,
    ) -> "MissionTrigger":
        return cls(
            run_at=first_run_at,
            interval=interval,
        )


@dataclass(frozen=True, slots=True)
class MissionDefinition:
    """Declarative constitutional mission definition."""

    mission_id: str
    name: str
    priority: MissionPriority
    trigger: MissionTrigger
    dependencies: frozenset[str]
    retry_policy: RetryPolicy
    cooldown: timedelta
    enabled: bool
    metadata: Mapping[str, Any]

    @classmethod
    def create(
        cls,
        *,
        mission_id: str,
        name: str,
        trigger: MissionTrigger,
        priority: MissionPriority = MissionPriority.NORMAL,
        dependencies: (
            set[str]
            | frozenset[str]
            | tuple[str, ...]
            | list[str]
            | None
        ) = None,
        retry_policy: RetryPolicy | None = None,
        cooldown: timedelta = timedelta(0),
        enabled: bool = True,
        metadata: Mapping[str, Any] | None = None,
    ) -> "MissionDefinition":
        normalized_id = mission_id.strip().lower()

        if not normalized_id:
            raise ValueError(
                "mission_id cannot be empty."
            )

        if cooldown < timedelta(0):
            raise ValueError(
                "cooldown cannot be negative."
            )

        dependency_set = frozenset(
            dependency.strip().lower()
            for dependency in (dependencies or ())
        )

        if normalized_id in dependency_set:
            raise ValueError(
                "A mission cannot depend on itself."
            )

        return cls(
            mission_id=normalized_id,
            name=name.strip(),
            priority=priority,
            trigger=trigger,
            dependencies=dependency_set,
            retry_policy=(
                retry_policy or RetryPolicy()
            ),
            cooldown=cooldown,
            enabled=enabled,
            metadata=MappingProxyType(
                dict(metadata or {})
            ),
        )

    @property
    def priority_weight(self) -> int:
        return _PRIORITY_WEIGHT[self.priority]


@dataclass(frozen=True, slots=True)
class MissionRecord:
    """Scheduler projection for one registered mission."""

    definition: MissionDefinition
    state: MissionState
    attempt: int
    next_run_at: datetime | None
    last_started_at: datetime | None = None
    last_completed_at: datetime | None = None
    last_error: str | None = None

    def __post_init__(self) -> None:
        for attribute in (
            "next_run_at",
            "last_started_at",
            "last_completed_at",
        ):
            value = getattr(self, attribute)

            if value is not None:
                if value.tzinfo is None:
                    raise ValueError(
                        f"{attribute} must include timezone."
                    )

                object.__setattr__(
                    self,
                    attribute,
                    value.astimezone(UTC),
                )


@dataclass(frozen=True, slots=True)
class ScheduledMission:
    """Immutable ready-queue item."""

    execution_id: UUID
    mission_id: str
    name: str
    priority: MissionPriority
    scheduled_for: datetime
    attempt: int
    metadata: Mapping[str, Any]

    @classmethod
    def create(
        cls,
        *,
        record: MissionRecord,
        scheduled_for: datetime,
    ) -> "ScheduledMission":
        return cls(
            execution_id=uuid4(),
            mission_id=record.definition.mission_id,
            name=record.definition.name,
            priority=record.definition.priority,
            scheduled_for=scheduled_for.astimezone(UTC),
            attempt=record.attempt,
            metadata=record.definition.metadata,
        )


@dataclass(frozen=True, slots=True)
class MissionSchedulerStatistics:
    """Immutable scheduler statistics."""

    registered: int
    enabled: int
    ready: int
    queued: int
    succeeded: int
    failed: int
    cancelled: int
    exhausted: int
    queue_depth: int

    def to_dict(self) -> dict[str, int]:
        return {
            "registered": self.registered,
            "enabled": self.enabled,
            "ready": self.ready,
            "queued": self.queued,
            "succeeded": self.succeeded,
            "failed": self.failed,
            "cancelled": self.cancelled,
            "exhausted": self.exhausted,
            "queue_depth": self.queue_depth,
        }
