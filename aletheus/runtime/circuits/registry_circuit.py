from __future__ import annotations

from typing import Any

from aletheus.runtime.circuits.anchor_circuit import (
    CircuitHealth,
    CircuitManifest,
    CircuitStatus,
    RuntimeAnchorCircuit,
)
from aletheus.runtime.managers import RegistryManager


class RegistryCircuit(RuntimeAnchorCircuit):
    """
    Registry Circuit

    Stable runtime attachment point for component discovery,
    component manifests, and shared health monitoring.

    The circuit receives its manager from the Runtime Composition Root.
    """

    CIRCUIT_ID = "registry"

    def __init__(
        self,
        manager: RegistryManager,
    ) -> None:
        self.manager = manager
        self._ready = False

    def manifest(self) -> CircuitManifest:
        return CircuitManifest(
            circuit_id=self.CIRCUIT_ID,
            name="Registry Circuit",
            purpose=(
                "Provides runtime component discovery, component "
                "manifests, registry summaries, and shared health monitoring."
            ),
            dependencies=[],
            provides=[
                "runtime_registry",
                "health_monitor",
                "component_discovery",
                "boot_summary",
            ],
        )

    def boot(self, runtime: Any) -> None:
        runtime.registry_manager = self.manager
        runtime.registry = self.manager.registry
        runtime.health_monitor = self.manager.health_monitor
        runtime.health = self.manager.health_monitor
        self._ready = True

    def shutdown(self) -> None:
        self._ready = False

    def health(self) -> CircuitHealth:
        if not self._ready:
            return CircuitHealth(
                circuit_id=self.CIRCUIT_ID,
                status=CircuitStatus.INITIALIZING,
                score=50,
                message="Registry Circuit has not completed boot.",
            )

        summary = self.manager.health_summary()

        return CircuitHealth(
            circuit_id=self.CIRCUIT_ID,
            status=CircuitStatus.READY,
            score=int(summary.get("score", 100)),
            message="Registry Circuit ready.",
            metrics={
                "registered_components": len(self.manager.list_components()),
                "health_checks": len(self.manager.health_checks()),
                "health_summary": summary,
            },
        )

    def register_component(self, component) -> None:
        self.manager.register_component(component)

    def publish_health(self, check) -> None:
        self.manager.publish_health(check)

    def registry_summary(self) -> dict:
        return self.manager.boot_summary()

    def list_components(self):
        return self.manager.list_components()

    def component(self, component_id: str):
        return self.manager.component(component_id)
