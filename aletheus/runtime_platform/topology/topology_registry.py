from __future__ import annotations

from types import MappingProxyType
from typing import Any

from .capability import RuntimeCapability
from .component import RuntimeComponent
from .dependency_graph import DependencyGraph
from .domain import RuntimeDomain
from .service import RuntimeService
from .topology_snapshot import TopologySnapshot


class TopologyRegistrationError(RuntimeError):
    pass


class RuntimeTopologyRegistry:
    """
    Canonical runtime topology source.

    This registry owns structural truth only. It does not execute runtime
    workloads, perform health checks, or manage command dispatch.
    """

    VERSION = "1.0.0"

    def __init__(self) -> None:
        self._domains: dict[str, RuntimeDomain] = {}
        self._services: dict[str, RuntimeService] = {}
        self._components: dict[str, RuntimeComponent] = {}
        self._providers: dict[str, Any] = {}
        self._capabilities: dict[str, RuntimeCapability] = {}
        self._graph = DependencyGraph()
        self._sealed = False

    @property
    def sealed(self) -> bool:
        return self._sealed

    def _ensure_mutable(self) -> None:
        if self._sealed:
            raise TopologyRegistrationError("Runtime topology is sealed.")

    def register_domain(
        self,
        domain: RuntimeDomain,
        *,
        replace: bool = False,
    ) -> RuntimeDomain:
        self._ensure_mutable()
        self._register_named(
            self._domains,
            domain.name,
            domain,
            replace=replace,
        )
        self._graph.add(domain.name, domain.dependencies)

        for capability in domain.capabilities:
            self.register_capability(
                RuntimeCapability(
                    name=capability,
                    provider=domain.name,
                    version=domain.version,
                ),
                replace=replace,
            )

        return domain

    def register_service(
        self,
        service: RuntimeService,
        *,
        replace: bool = False,
    ) -> RuntimeService:
        self._ensure_mutable()
        self._register_named(
            self._services,
            service.name,
            service,
            replace=replace,
        )
        self._graph.add(service.name, service.dependencies)

        for capability in service.capabilities:
            self.register_capability(
                RuntimeCapability(
                    name=capability,
                    provider=service.name,
                    version=service.version,
                ),
                replace=replace,
            )

        return service

    def register_component(
        self,
        component: RuntimeComponent,
        *,
        replace: bool = False,
    ) -> RuntimeComponent:
        self._ensure_mutable()
        self._register_named(
            self._components,
            component.name,
            component,
            replace=replace,
        )
        self._graph.add(
            component.name,
            component.dependencies,
        )

        for capability in component.capabilities:
            self.register_capability(
                RuntimeCapability(
                    name=capability,
                    provider=component.name,
                    version=component.version,
                ),
                replace=replace,
            )

        return component

    def register_provider(
        self,
        name: str,
        provider: Any,
        *,
        dependencies: tuple[str, ...] = (),
        replace: bool = False,
    ) -> Any:
        self._ensure_mutable()
        normalized = name.strip()

        if not normalized:
            raise ValueError("Provider name cannot be empty.")

        self._register_named(
            self._providers,
            normalized,
            provider,
            replace=replace,
        )
        self._graph.add(normalized, dependencies)
        return provider

    def register_capability(
        self,
        capability: RuntimeCapability,
        *,
        replace: bool = False,
    ) -> RuntimeCapability:
        self._ensure_mutable()
        self._register_named(
            self._capabilities,
            capability.name,
            capability,
            replace=replace,
        )
        return capability

    @staticmethod
    def _register_named(
        target: dict[str, Any],
        name: str,
        value: Any,
        *,
        replace: bool,
    ) -> None:
        normalized = name.strip()

        if not normalized:
            raise ValueError("Registration name cannot be empty.")

        if normalized in target and not replace:
            raise TopologyRegistrationError(f"Already registered: {normalized}")

        target[normalized] = value

    def resolve(self, name: str) -> Any | None:
        for collection in (
            self._domains,
            self._services,
            self._components,
            self._providers,
            self._capabilities,
        ):
            if name in collection:
                return collection[name]

        return None

    def validate(self) -> None:
        self._graph.validate()

    def seal(self) -> TopologySnapshot:
        self.validate()
        self._sealed = True
        return self.snapshot()

    def snapshot(self) -> TopologySnapshot:
        dependency_map = {node.name: node.dependencies for node in self._graph.nodes()}

        return TopologySnapshot(
            version=self.VERSION,
            domains=tuple(sorted(self._domains)),
            services=tuple(sorted(self._services)),
            components=tuple(sorted(self._components)),
            providers=tuple(sorted(self._providers)),
            capabilities=tuple(sorted(self._capabilities)),
            dependencies=MappingProxyType(dependency_map),
            metadata=MappingProxyType(
                {
                    "sealed": self._sealed,
                    "boot_order": self._graph.boot_order(),
                    "shutdown_order": (self._graph.shutdown_order()),
                }
            ),
        )

    def boot_order(self) -> tuple[str, ...]:
        return self._graph.boot_order()

    def shutdown_order(self) -> tuple[str, ...]:
        return self._graph.shutdown_order()
