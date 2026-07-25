"""Immutable Runtime Intelligence Orchestrator views."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from types import MappingProxyType
from typing import Any
from uuid import UUID, uuid4


def _freeze(
    value: Mapping[str, Any],
) -> Mapping[str, Any]:
    return MappingProxyType(dict(value))


@dataclass(frozen=True, slots=True)
class RuntimeHealthSummary:
    """Aggregated constitutional health view."""

    state: str
    total_services: int
    healthy: int
    warning: int
    degraded: int
    critical: int
    offline: int
    unknown: int
    unhealthy_services: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "state": self.state,
            "total_services": self.total_services,
            "healthy": self.healthy,
            "warning": self.warning,
            "degraded": self.degraded,
            "critical": self.critical,
            "offline": self.offline,
            "unknown": self.unknown,
            "unhealthy_services": list(
                self.unhealthy_services
            ),
        }


@dataclass(frozen=True, slots=True)
class RuntimeConstitutionalState:
    """Structural constitutional compliance projection."""

    satisfied: bool
    cycles: int
    orphans: int
    connected_components: int
    broken_dependencies: int
    checks: Mapping[str, bool]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "checks",
            _freeze(self.checks),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "satisfied": self.satisfied,
            "cycles": self.cycles,
            "orphans": self.orphans,
            "connected_components": (
                self.connected_components
            ),
            "broken_dependencies": (
                self.broken_dependencies
            ),
            "checks": dict(self.checks),
        }


@dataclass(frozen=True, slots=True)
class RuntimeIntelligenceOverview:
    """Complete read-only overview of Platform Intelligence."""

    overview_id: UUID
    generated_at: datetime
    twin_revision: int
    runtime: Mapping[str, Any]
    services: Mapping[str, Any]
    graph: Mapping[str, Any]
    events: Mapping[str, Any]
    health: RuntimeHealthSummary
    constitution: RuntimeConstitutionalState
    intelligence: Mapping[str, Any]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "runtime",
            _freeze(self.runtime),
        )
        object.__setattr__(
            self,
            "services",
            _freeze(self.services),
        )
        object.__setattr__(
            self,
            "graph",
            _freeze(self.graph),
        )
        object.__setattr__(
            self,
            "events",
            _freeze(self.events),
        )
        object.__setattr__(
            self,
            "intelligence",
            _freeze(self.intelligence),
        )

    @classmethod
    def create(
        cls,
        *,
        twin_revision: int,
        runtime: Mapping[str, Any],
        services: Mapping[str, Any],
        graph: Mapping[str, Any],
        events: Mapping[str, Any],
        health: RuntimeHealthSummary,
        constitution: RuntimeConstitutionalState,
        intelligence: Mapping[str, Any],
    ) -> RuntimeIntelligenceOverview:
        return cls(
            overview_id=uuid4(),
            generated_at=datetime.now(UTC),
            twin_revision=twin_revision,
            runtime=runtime,
            services=services,
            graph=graph,
            events=events,
            health=health,
            constitution=constitution,
            intelligence=intelligence,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "overview_id": str(self.overview_id),
            "generated_at": (
                self.generated_at.isoformat()
            ),
            "twin_revision": self.twin_revision,
            "runtime": dict(self.runtime),
            "services": dict(self.services),
            "graph": dict(self.graph),
            "events": dict(self.events),
            "health": self.health.to_dict(),
            "constitution": (
                self.constitution.to_dict()
            ),
            "intelligence": dict(
                self.intelligence
            ),
        }
