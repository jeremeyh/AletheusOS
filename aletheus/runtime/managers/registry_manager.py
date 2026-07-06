from __future__ import annotations

from typing import Any, Optional

from aletheus.runtime_registry_v2.core import RuntimeRegistry
from aletheus.runtime_registry_v2.health import HealthMonitor
from aletheus.runtime_registry_v2.models import RuntimeComponent


class RegistryManager:
    """
    Registry Manager

    Coordinates runtime component registration, component discovery,
    manifest lookup, and shared health monitoring.

    Managers coordinate services.
    They do not own service lifecycles.
    """

    def __init__(
        self,
        registry: RuntimeRegistry,
        health_monitor: HealthMonitor,
    ) -> None:
        self.registry = registry
        self.health_monitor = health_monitor

    def register_component(
        self,
        component: RuntimeComponent,
    ) -> None:
        self.registry.register(component)

    def component(
        self,
        component_id: str,
    ) -> Optional[RuntimeComponent]:
        return self.registry.get(component_id)

    def list_components(self) -> list[RuntimeComponent]:
        return self.registry.all()

    def boot_summary(self) -> dict:
        return self.registry.boot_summary()

    def registry_statistics(self) -> dict:
        return self.registry.statistics()

    def publish_health(
        self,
        check: Any,
    ) -> None:
        self.health_monitor.publish(check)

    def health_summary(self) -> dict:
        return self.health_monitor.summary()

    def health_checks(self) -> list:
        return self.health_monitor.all()
