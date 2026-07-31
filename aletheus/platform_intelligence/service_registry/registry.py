"""Constitutional Platform Service Registry."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable
from threading import RLock
from types import MappingProxyType

from aletheus.platform_intelligence.constitutional import (
    ConstitutionalAddress,
    ConstitutionalHealth,
    ConstitutionalObject,
    ConstitutionalState,
)
from aletheus.platform_intelligence.event_bus import (
    ConstitutionalEventBus,
)
from aletheus.platform_intelligence.events import (
    ConstitutionalEvent,
    ConstitutionalEventKind,
    ConstitutionalEventSeverity,
    health_changed_event,
    object_registered_event,
    state_changed_event,
)

from .exceptions import (
    ServiceAlreadyRegisteredError,
    ServiceDependencyError,
    ServiceInUseError,
    ServiceNotFoundError,
)
from .models import (
    PlatformServiceDefinition,
    PlatformServiceRegistryStatistics,
)


class PlatformServiceRegistry:
    """
    Authoritative constitutional catalog of platform services.

    The registry owns service representations and dependency declarations.
    It does not instantiate service implementations or execute service logic.
    """

    def __init__(
        self,
        *,
        event_bus: ConstitutionalEventBus | None = None,
        require_registered_dependencies: bool = True,
    ) -> None:
        self._event_bus = event_bus
        self._require_registered_dependencies = require_registered_dependencies

        self._services: dict[
            ConstitutionalAddress,
            ConstitutionalObject,
        ] = {}

        self._dependencies: dict[
            ConstitutionalAddress,
            frozenset[ConstitutionalAddress],
        ] = {}

        self._lock = RLock()

    @property
    def event_bus(
        self,
    ) -> ConstitutionalEventBus | None:
        return self._event_bus

    def register(
        self,
        definition: PlatformServiceDefinition,
    ) -> ConstitutionalObject:
        """Register one service and publish constitutional facts."""

        address = definition.address

        with self._lock:
            if address in self._services:
                raise ServiceAlreadyRegisteredError(
                    f"Service already registered: {address}"
                )

            missing = sorted(
                (
                    dependency
                    for dependency in definition.dependencies
                    if dependency not in self._services
                ),
                key=str,
            )

            if missing and self._require_registered_dependencies:
                raise ServiceDependencyError(
                    "Service dependencies are not registered: "
                    + ", ".join(str(item) for item in missing)
                )

            service = definition.to_constitutional_object()

            self._services[address] = service
            self._dependencies[address] = definition.dependencies

        self._publish(
            object_registered_event(
                service,
                source="service.platform-registry",
            )
        )

        self._publish(
            ConstitutionalEvent.create(
                kind=(ConstitutionalEventKind.SERVICE_REGISTERED),
                source="service.platform-registry",
                subject=address,
                payload={
                    "service": service.to_snapshot(),
                    "dependencies": sorted(
                        str(dependency) for dependency in definition.dependencies
                    ),
                },
            )
        )

        for dependency in definition.dependencies:
            self._publish(
                ConstitutionalEvent.create(
                    kind=(ConstitutionalEventKind.DEPENDENCY_RESOLVED),
                    source="service.platform-registry",
                    subject=address,
                    payload={
                        "dependency": str(dependency),
                    },
                )
            )

        return service

    def register_many(
        self,
        definitions: Iterable[PlatformServiceDefinition],
    ) -> tuple[ConstitutionalObject, ...]:
        """
        Register service definitions in dependency-resolvable order.

        The operation stops if no remaining definition can be resolved.
        Already completed registrations remain registered.
        """

        pending = list(definitions)
        registered: list[ConstitutionalObject] = []

        while pending:
            progressed = False

            for definition in tuple(pending):
                if all(dependency in self for dependency in definition.dependencies):
                    registered.append(self.register(definition))
                    pending.remove(definition)
                    progressed = True

            if progressed:
                continue

            unresolved = {
                str(definition.address): sorted(
                    str(dependency)
                    for dependency in definition.dependencies
                    if dependency not in self
                )
                for definition in pending
            }

            raise ServiceDependencyError(
                f"Unable to resolve service dependency order: {unresolved}"
            )

        return tuple(registered)

    def get(
        self,
        address: str | ConstitutionalAddress,
    ) -> ConstitutionalObject:
        resolved = self._address(address)

        with self._lock:
            service = self._services.get(resolved)

        if service is None:
            raise ServiceNotFoundError(f"Service not found: {resolved}")

        return service

    def contains(
        self,
        address: str | ConstitutionalAddress,
    ) -> bool:
        resolved = self._address(address)

        with self._lock:
            return resolved in self._services

    def __contains__(
        self,
        address: object,
    ) -> bool:
        if isinstance(address, ConstitutionalAddress):
            return self.contains(address)

        if isinstance(address, str):
            try:
                return self.contains(address)
            except ValueError:
                return False

        return False

    def all(
        self,
    ) -> tuple[ConstitutionalObject, ...]:
        with self._lock:
            return tuple(
                sorted(
                    self._services.values(),
                    key=lambda service: service.address,
                )
            )

    def dependencies_of(
        self,
        address: str | ConstitutionalAddress,
    ) -> tuple[ConstitutionalAddress, ...]:
        resolved = self._address(address)
        self.get(resolved)

        with self._lock:
            dependencies = self._dependencies[resolved]

        return tuple(sorted(dependencies, key=str))

    def dependents_of(
        self,
        address: str | ConstitutionalAddress,
    ) -> tuple[ConstitutionalAddress, ...]:
        resolved = self._address(address)
        self.get(resolved)

        with self._lock:
            dependents = tuple(
                service_address
                for service_address, dependencies in self._dependencies.items()
                if resolved in dependencies
            )

        return tuple(sorted(dependents, key=str))

    def transition(
        self,
        address: str | ConstitutionalAddress,
        state: ConstitutionalState,
        *,
        health: ConstitutionalHealth | None = None,
    ) -> ConstitutionalObject:
        resolved = self._address(address)

        with self._lock:
            current = self.get(resolved)
            updated = current.transition_to(
                state,
                health=health,
            )
            self._services[resolved] = updated

        self._publish(
            state_changed_event(
                updated,
                previous_state=current.state,
                source="service.platform-registry",
            )
        )

        event_kind = self._service_event_kind(state)

        if event_kind is not None:
            self._publish(
                ConstitutionalEvent.create(
                    kind=event_kind,
                    source="service.platform-registry",
                    subject=resolved,
                    severity=(
                        ConstitutionalEventSeverity.ERROR
                        if state is ConstitutionalState.DEGRADED
                        else ConstitutionalEventSeverity.INFO
                    ),
                    payload={
                        "previous_state": (current.state.value),
                        "current_state": state.value,
                    },
                )
            )

        return updated

    def report_health(
        self,
        address: str | ConstitutionalAddress,
        health: ConstitutionalHealth,
        *,
        metrics: dict[str, object] | None = None,
    ) -> ConstitutionalObject:
        resolved = self._address(address)

        with self._lock:
            current = self.get(resolved)
            updated = current.report_health(
                health,
                metrics=metrics,
            )
            self._services[resolved] = updated

        self._publish(
            health_changed_event(
                updated,
                previous_health=current.health,
                source="service.platform-registry",
            )
        )

        return updated

    def remove(
        self,
        address: str | ConstitutionalAddress,
        *,
        force: bool = False,
    ) -> ConstitutionalObject:
        resolved = self._address(address)
        service = self.get(resolved)
        dependents = self.dependents_of(resolved)

        if dependents and not force:
            raise ServiceInUseError(
                f"Service {resolved} has dependents: "
                + ", ".join(str(item) for item in dependents)
            )

        with self._lock:
            del self._services[resolved]
            del self._dependencies[resolved]

            if force:
                for dependent, dependencies in tuple(self._dependencies.items()):
                    if resolved in dependencies:
                        self._dependencies[dependent] = frozenset(
                            item for item in dependencies if item != resolved
                        )

        self._publish(
            ConstitutionalEvent.create(
                kind=ConstitutionalEventKind.OBJECT_RETIRED,
                source="service.platform-registry",
                subject=resolved,
                severity=(
                    ConstitutionalEventSeverity.WARNING
                    if force
                    else ConstitutionalEventSeverity.NOTICE
                ),
                payload={
                    "service": service.to_snapshot(),
                    "forced": force,
                },
            )
        )

        return service

    def statistics(
        self,
    ) -> PlatformServiceRegistryStatistics:
        with self._lock:
            services = tuple(self._services.values())
            dependency_edges = sum(
                len(dependencies) for dependencies in self._dependencies.values()
            )

        state_counts = Counter(service.state.value for service in services)
        health_counts = Counter(service.health.value for service in services)

        unhealthy_states = {
            ConstitutionalHealth.WARNING,
            ConstitutionalHealth.DEGRADED,
            ConstitutionalHealth.CRITICAL,
            ConstitutionalHealth.OFFLINE,
        }

        return PlatformServiceRegistryStatistics(
            registered=len(services),
            running=state_counts[ConstitutionalState.RUNNING.value],
            degraded=state_counts[ConstitutionalState.DEGRADED.value],
            unhealthy=sum(service.health in unhealthy_states for service in services),
            dependency_edges=dependency_edges,
            services_by_state=MappingProxyType(dict(state_counts)),
            services_by_health=MappingProxyType(dict(health_counts)),
        )

    def snapshot(
        self,
    ) -> dict[str, object]:
        """Return a Digital Twin-ready registry snapshot."""

        return {
            "services": [
                {
                    **service.to_snapshot(),
                    "dependencies": [
                        str(dependency)
                        for dependency in self.dependencies_of(service.identity.address)
                    ],
                    "dependents": [
                        str(dependent)
                        for dependent in self.dependents_of(service.identity.address)
                    ],
                }
                for service in self.all()
            ],
            "statistics": self.statistics().to_dict(),
        }

    def _publish(
        self,
        event: ConstitutionalEvent,
    ) -> None:
        if self._event_bus is not None:
            self._event_bus.publish(event)

    @staticmethod
    def _address(
        value: str | ConstitutionalAddress,
    ) -> ConstitutionalAddress:
        return (
            value
            if isinstance(value, ConstitutionalAddress)
            else ConstitutionalAddress(value)
        )

    @staticmethod
    def _service_event_kind(
        state: ConstitutionalState,
    ) -> ConstitutionalEventKind | None:
        if state is ConstitutionalState.RUNNING:
            return ConstitutionalEventKind.SERVICE_STARTED

        if state is ConstitutionalState.STOPPED:
            return ConstitutionalEventKind.SERVICE_STOPPED

        if state is ConstitutionalState.DEGRADED:
            return ConstitutionalEventKind.SERVICE_FAILED

        return None
