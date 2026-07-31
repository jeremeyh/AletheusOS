"""Public projection models for the AletheusOS Platform Surface™."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class PlatformRuntimeSnapshot:
    """Read-only summary of the connected constitutional runtime."""

    status: str
    version: str

    cases: int
    missions: int
    time_missions: int
    time_phases: int

    mission_executions: int
    phase_executions: int
    domain_events_published: int

    ledger_events: int
    failures: int

    details: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "version": self.version,
            "cases": self.cases,
            "missions": self.missions,
            "time_missions": self.time_missions,
            "time_phases": self.time_phases,
            "mission_executions": self.mission_executions,
            "phase_executions": self.phase_executions,
            "domain_events_published": (self.domain_events_published),
            "ledger_events": self.ledger_events,
            "failures": self.failures,
            "details": dict(self.details),
        }


@dataclass(frozen=True, slots=True)
class PlatformHealth:
    """Unified public platform health projection."""

    status: str
    healthy: bool
    components: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "healthy": self.healthy,
            "components": dict(self.components),
        }
