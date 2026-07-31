"""Live Platform Digital Twin façade."""

from __future__ import annotations

from collections import Counter, deque
from threading import RLock
from typing import Any
from uuid import UUID

from aletheus.platform_intelligence.constitutional import (
    ConstitutionalAddress,
    ConstitutionalObject,
)
from aletheus.platform_intelligence.constitutional_graph import (
    ConstitutionalGraph,
)
from aletheus.platform_intelligence.event_bus import (
    ConstitutionalEventBus,
)
from aletheus.platform_intelligence.events import (
    ConstitutionalEvent,
)
from aletheus.platform_intelligence.service_registry import (
    PlatformServiceRegistry,
)

from .diff import TwinSnapshotDiff
from .exceptions import (
    TwinObjectNotFoundError,
    TwinSnapshotNotFoundError,
)
from .snapshot import TwinSnapshot
from .statistics import (
    PlatformDigitalTwinStatistics,
)


class PlatformDigitalTwin:
    """
    Live constitutional projection of AletheusOS.

    The Twin composes authoritative registry and graph state. It does not
    replace either source and does not execute runtime behavior.
    """

    def __init__(
        self,
        *,
        service_registry: PlatformServiceRegistry,
        graph: ConstitutionalGraph,
        event_bus: ConstitutionalEventBus | None = None,
        snapshot_limit: int = 100,
    ) -> None:
        if snapshot_limit < 0:
            raise ValueError("snapshot_limit cannot be negative.")

        self._service_registry = service_registry
        self._graph = graph
        self._event_bus = event_bus
        self._snapshot_limit = snapshot_limit

        self._revision = 0
        self._events_observed = 0
        self._last_event: ConstitutionalEvent | None = None

        self._snapshots: deque[TwinSnapshot] = deque(
            maxlen=(snapshot_limit if snapshot_limit > 0 else None)
        )

        self._subscription_id: UUID | None = None
        self._lock = RLock()

        if event_bus is not None:
            self._subscription_id = event_bus.subscribe(self.handle)

    @property
    def revision(self) -> int:
        with self._lock:
            return self._revision

    @property
    def subscription_id(self) -> UUID | None:
        return self._subscription_id

    def handle(
        self,
        event: ConstitutionalEvent,
    ) -> None:
        """Observe one constitutional event."""

        with self._lock:
            self._events_observed += 1
            self._revision += 1
            self._last_event = event

    def object(
        self,
        address: str | ConstitutionalAddress,
    ) -> ConstitutionalObject:
        resolved = self._address(address)

        if self._graph.contains(resolved):
            return self._graph.get_node(resolved)

        if self._service_registry.contains(resolved):
            return self._service_registry.get(resolved)

        raise TwinObjectNotFoundError(f"Twin object not found: {resolved}")

    def service(
        self,
        address: str | ConstitutionalAddress,
    ) -> ConstitutionalObject:
        try:
            return self._service_registry.get(address)
        except Exception as error:
            raise TwinObjectNotFoundError(
                f"Twin service not found: {address}"
            ) from error

    def dependencies(
        self,
        address: str | ConstitutionalAddress,
    ) -> tuple[ConstitutionalObject, ...]:
        if self._graph.contains(address):
            return self._graph.dependencies(address)

        dependency_addresses = self._service_registry.dependencies_of(address)

        return tuple(self.object(item) for item in dependency_addresses)

    def dependents(
        self,
        address: str | ConstitutionalAddress,
    ) -> tuple[ConstitutionalObject, ...]:
        if self._graph.contains(address):
            return self._graph.dependents(address)

        dependent_addresses = self._service_registry.dependents_of(address)

        return tuple(self.object(item) for item in dependent_addresses)

    def impact(
        self,
        address: str | ConstitutionalAddress,
    ) -> tuple[ConstitutionalObject, ...]:
        """Return all upstream dependents affected by a node."""

        if self._graph.contains(address):
            return self._graph.upstream(address)

        return self.dependents(address)

    def health(self) -> dict[str, object]:
        """Return the current platform health projection."""

        services = self._service_registry.all()

        health_counts = Counter(service.health.value for service in services)

        unhealthy = tuple(
            service.address
            for service in services
            if service.health.value
            in {
                "warning",
                "degraded",
                "critical",
                "offline",
            }
        )

        if health_counts["critical"] > 0:
            state = "critical"
        elif health_counts["offline"] > 0 or (
            health_counts["degraded"] > 0 or health_counts["warning"] > 0
        ):
            state = "degraded"
        elif services and all(
            service.health.value == "healthy" for service in services
        ):
            state = "healthy"
        else:
            state = "unknown"

        return {
            "state": state,
            "total_services": len(services),
            "counts": dict(health_counts),
            "unhealthy_services": sorted(unhealthy),
        }

    def snapshot(
        self,
        *,
        retain: bool = True,
    ) -> TwinSnapshot:
        registry_snapshot = self._service_registry.snapshot()
        graph_snapshot = self._graph.snapshot()

        with self._lock:
            revision = self._revision
            last_event = self._last_event

        statistics = self.statistics().to_dict()

        snapshot = TwinSnapshot.create(
            revision=revision,
            services=tuple(registry_snapshot["services"]),
            nodes=tuple(graph_snapshot["nodes"]),
            relationships=tuple(graph_snapshot["relationships"]),
            health=self.health(),
            topology=graph_snapshot["topology"],
            statistics=statistics,
            last_event=(last_event.to_envelope() if last_event is not None else None),
        )

        if retain and self._snapshot_limit > 0:
            with self._lock:
                self._snapshots.append(snapshot)

        return snapshot

    def retained_snapshots(
        self,
    ) -> tuple[TwinSnapshot, ...]:
        with self._lock:
            return tuple(self._snapshots)

    def get_snapshot(
        self,
        snapshot_id: UUID,
    ) -> TwinSnapshot:
        with self._lock:
            for snapshot in self._snapshots:
                if snapshot.snapshot_id == snapshot_id:
                    return snapshot

        raise TwinSnapshotNotFoundError(f"Twin snapshot not found: {snapshot_id}")

    def diff(
        self,
        previous: TwinSnapshot,
        current: TwinSnapshot,
    ) -> TwinSnapshotDiff:
        return TwinSnapshotDiff.between(
            previous,
            current,
        )

    def statistics(
        self,
    ) -> PlatformDigitalTwinStatistics:
        registry_stats = self._service_registry.statistics()
        graph_stats = self._graph.statistics()

        health_counts = Counter(
            service.health.value for service in self._service_registry.all()
        )

        with self._lock:
            revision = self._revision
            events_observed = self._events_observed
            snapshots_retained = len(self._snapshots)

        return PlatformDigitalTwinStatistics(
            revision=revision,
            snapshots_retained=(snapshots_retained),
            events_observed=events_observed,
            services=registry_stats.registered,
            nodes=graph_stats.nodes,
            relationships=graph_stats.relationships,
            healthy=health_counts["healthy"],
            warning=health_counts["warning"],
            degraded=health_counts["degraded"],
            critical=health_counts["critical"],
            offline=health_counts["offline"],
            unknown=health_counts["unknown"],
        )

    def current_state(self) -> dict[str, Any]:
        """Return the current live Twin projection."""

        return {
            "revision": self.revision,
            "health": self.health(),
            "services": [
                service.to_snapshot() for service in self._service_registry.all()
            ],
            "graph": self._graph.snapshot(),
            "statistics": (self.statistics().to_dict()),
            "last_event": (
                self._last_event.to_envelope() if self._last_event is not None else None
            ),
        }

    def close(self) -> None:
        """Detach the Twin from its Event Bus."""

        if self._event_bus is not None and self._subscription_id is not None:
            self._event_bus.unsubscribe(self._subscription_id)
            self._subscription_id = None

    @staticmethod
    def _address(
        value: str | ConstitutionalAddress,
    ) -> ConstitutionalAddress:
        return (
            value
            if isinstance(
                value,
                ConstitutionalAddress,
            )
            else ConstitutionalAddress(value)
        )
