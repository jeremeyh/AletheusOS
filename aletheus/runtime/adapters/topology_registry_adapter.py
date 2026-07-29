from __future__ import annotations

from aletheus.runtime_platform.topology.topology_registry import (
    RuntimeTopologyRegistry,
)


class TopologyRegistryAdapter:
    """
    Compatibility facade exposing the legacy RuntimeRegistry API while
    delegating all state to RuntimeTopologyRegistry.
    """

    def __init__(self) -> None:
        self._topology = RuntimeTopologyRegistry()

    @property
    def topology(self) -> RuntimeTopologyRegistry:
        return self._topology

    def register_domain(self, name: str, instance) -> None:
        self._topology.register_domain(name, instance)

    def register_service(self, name: str, instance) -> None:
        self._topology.register_service(name, instance)

    def register_component(self, name: str, metadata) -> None:
        self._topology.register_component(name, metadata)

    def snapshot(self):
        return self._topology.snapshot()
