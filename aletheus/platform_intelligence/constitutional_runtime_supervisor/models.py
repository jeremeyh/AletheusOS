"""Immutable models for the Constitutional Runtime Supervisor."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from typing import Any
from uuid import UUID, uuid4


class ConstitutionalRuntimeSupervisorState(StrEnum):
    """Canonical supervisor lifecycle states."""

    CREATED = "created"
    ACTIVE = "active"
    STOPPED = "stopped"
    FAILED = "failed"


class RuntimeSupervisionState(StrEnum):
    """Aggregated runtime supervision states."""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"
    STOPPED = "stopped"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class RestartPolicy:
    """Bounded restart and recovery policy."""

    maximum_attempts: int = 3
    cooldown: timedelta = timedelta(0)
    recoverable_health: frozenset[str] = frozenset(
        {
            "warning",
            "degraded",
            "critical",
            "offline",
        }
    )

    def __post_init__(self) -> None:
        if self.maximum_attempts < 0:
            raise ValueError("maximum_attempts cannot be negative.")

        if self.cooldown < timedelta(0):
            raise ValueError("cooldown cannot be negative.")


@dataclass(frozen=True, slots=True)
class ServiceSupervisionRecord:
    """Read-only supervision projection for one service."""

    address: str
    state: str
    health: str
    restart_attempts: int
    recoverable: bool
    last_recovery_at: datetime | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "address": self.address,
            "state": self.state,
            "health": self.health,
            "restart_attempts": self.restart_attempts,
            "recoverable": self.recoverable,
            "last_recovery_at": (
                self.last_recovery_at.isoformat() if self.last_recovery_at else None
            ),
        }


@dataclass(frozen=True, slots=True)
class RuntimeHealthReport:
    """Immutable aggregate runtime-health report."""

    report_id: UUID
    generated_at: datetime
    state: RuntimeSupervisionState
    service_count: int
    healthy: int
    warning: int
    degraded: int
    critical: int
    offline: int
    unknown: int
    running: int
    stopped: int
    recoverable_services: tuple[str, ...]
    services: tuple[ServiceSupervisionRecord, ...]

    @classmethod
    def create(
        cls,
        *,
        state: RuntimeSupervisionState,
        service_count: int,
        healthy: int,
        warning: int,
        degraded: int,
        critical: int,
        offline: int,
        unknown: int,
        running: int,
        stopped: int,
        recoverable_services: tuple[str, ...],
        services: tuple[ServiceSupervisionRecord, ...],
    ) -> RuntimeHealthReport:
        return cls(
            report_id=uuid4(),
            generated_at=datetime.now(UTC),
            state=state,
            service_count=service_count,
            healthy=healthy,
            warning=warning,
            degraded=degraded,
            critical=critical,
            offline=offline,
            unknown=unknown,
            running=running,
            stopped=stopped,
            recoverable_services=tuple(sorted(recoverable_services)),
            services=services,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_id": str(self.report_id),
            "generated_at": (self.generated_at.isoformat()),
            "state": self.state.value,
            "service_count": self.service_count,
            "healthy": self.healthy,
            "warning": self.warning,
            "degraded": self.degraded,
            "critical": self.critical,
            "offline": self.offline,
            "unknown": self.unknown,
            "running": self.running,
            "stopped": self.stopped,
            "recoverable_services": list(self.recoverable_services),
            "services": [service.to_dict() for service in self.services],
        }


@dataclass(frozen=True, slots=True)
class SupervisorHeartbeat:
    """Immutable CRS heartbeat."""

    sequence: int
    generated_at: datetime
    supervisor_state: ConstitutionalRuntimeSupervisorState
    runtime_state: RuntimeSupervisionState
    kernel_state: str
    service_count: int
    degraded_count: int
    recovery_count: int
    restart_count: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "sequence": self.sequence,
            "generated_at": (self.generated_at.isoformat()),
            "supervisor_state": (self.supervisor_state.value),
            "runtime_state": (self.runtime_state.value),
            "kernel_state": self.kernel_state,
            "service_count": self.service_count,
            "degraded_count": self.degraded_count,
            "recovery_count": self.recovery_count,
            "restart_count": self.restart_count,
        }


@dataclass(frozen=True, slots=True)
class SupervisorStatistics:
    """Immutable supervisor statistics."""

    supervision_cycles: int
    heartbeats: int
    recovery_attempts: int
    successful_recoveries: int
    failed_recoveries: int
    service_restarts: int
    monitored_services: int

    def to_dict(self) -> dict[str, int]:
        return {
            "supervision_cycles": (self.supervision_cycles),
            "heartbeats": self.heartbeats,
            "recovery_attempts": (self.recovery_attempts),
            "successful_recoveries": (self.successful_recoveries),
            "failed_recoveries": (self.failed_recoveries),
            "service_restarts": (self.service_restarts),
            "monitored_services": (self.monitored_services),
        }
