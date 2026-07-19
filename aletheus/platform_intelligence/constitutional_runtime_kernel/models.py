"""Immutable models for the Constitutional Runtime Kernel."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from types import MappingProxyType
from typing import Any, Mapping


class ConstitutionalRuntimeKernelState(StrEnum):
    """Canonical CRK lifecycle states."""

    CREATED = "created"
    COMPOSED = "composed"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class ConstitutionalRuntimeKernelStatus:
    """Immutable CRK status projection."""

    state: ConstitutionalRuntimeKernelState
    version: str
    created_at: datetime
    modified_at: datetime
    composed: bool
    running: bool
    registered_services: int
    graph_nodes: int
    graph_relationships: int
    twin_revision: int
    event_subscribers: int
    mission_count: int
    scheduled_missions: int
    failure_reason: str | None = None

    def __post_init__(self) -> None:
        for name in (
            "created_at",
            "modified_at",
        ):
            value = getattr(self, name)

            if value.tzinfo is None:
                raise ValueError(
                    f"{name} must include timezone."
                )

            object.__setattr__(
                self,
                name,
                value.astimezone(UTC),
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "state": self.state.value,
            "version": self.version,
            "created_at": self.created_at.isoformat(),
            "modified_at": self.modified_at.isoformat(),
            "composed": self.composed,
            "running": self.running,
            "registered_services": (
                self.registered_services
            ),
            "graph_nodes": self.graph_nodes,
            "graph_relationships": (
                self.graph_relationships
            ),
            "twin_revision": self.twin_revision,
            "event_subscribers": (
                self.event_subscribers
            ),
            "mission_count": self.mission_count,
            "scheduled_missions": (
                self.scheduled_missions
            ),
            "failure_reason": self.failure_reason,
        }


@dataclass(frozen=True, slots=True)
class ConstitutionalRuntimeKernelSnapshot:
    """Immutable aggregate CRK snapshot."""

    generated_at: datetime
    kernel: Mapping[str, Any]
    runtime: Mapping[str, Any]
    services: Mapping[str, Any]
    graph: Mapping[str, Any]
    events: Mapping[str, Any]
    twin: Mapping[str, Any]
    intelligence: Mapping[str, Any]
    missions: Mapping[str, Any]
    scheduler: Mapping[str, Any]

    def __post_init__(self) -> None:
        if self.generated_at.tzinfo is None:
            raise ValueError(
                "generated_at must include timezone."
            )

        object.__setattr__(
            self,
            "generated_at",
            self.generated_at.astimezone(UTC),
        )

        for name in (
            "kernel",
            "runtime",
            "services",
            "graph",
            "events",
            "twin",
            "intelligence",
            "missions",
            "scheduler",
        ):
            object.__setattr__(
                self,
                name,
                MappingProxyType(
                    dict(getattr(self, name))
                ),
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "generated_at": (
                self.generated_at.isoformat()
            ),
            "kernel": dict(self.kernel),
            "runtime": dict(self.runtime),
            "services": dict(self.services),
            "graph": dict(self.graph),
            "events": dict(self.events),
            "twin": dict(self.twin),
            "intelligence": dict(
                self.intelligence
            ),
            "missions": dict(self.missions),
            "scheduler": dict(self.scheduler),
        }
