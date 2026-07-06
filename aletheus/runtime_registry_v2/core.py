from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Optional

from .models import (
    ComponentHealth,
    RuntimeComponent,
    RuntimeLayer,
    RuntimeRegistryReport,
)


class RuntimeRegistry:
    """
    Canonical registry for all AletheusOS runtime components.

    The registry becomes the authoritative source for discovering
    every constitutional component, infrastructure service,
    engine, application, and capability.

    Genesis 6.1
    """

    def __init__(self):
        self._components: Dict[str, RuntimeComponent] = {}

    # ---------------------------------------------------------
    # Registration
    # ---------------------------------------------------------

    def register(self, component: RuntimeComponent):

        if component.component_id in self._components:
            raise ValueError(
                f"Component '{component.component_id}' already registered."
            )

        self._components[component.component_id] = component

    def unregister(self, component_id: str):

        self._components.pop(component_id, None)

    # ---------------------------------------------------------
    # Lookup
    # ---------------------------------------------------------

    def get(self, component_id: str) -> Optional[RuntimeComponent]:

        return self._components.get(component_id)

    def exists(self, component_id: str) -> bool:

        return component_id in self._components

    # ---------------------------------------------------------
    # Enumeration
    # ---------------------------------------------------------

    def all(self) -> List[RuntimeComponent]:

        return list(self._components.values())

    def by_layer(self, layer: RuntimeLayer) -> List[RuntimeComponent]:

        return [
            c
            for c in self._components.values()
            if c.layer == layer
        ]

    def grouped_by_layer(self):

        grouped = defaultdict(list)

        for component in self._components.values():
            grouped[component.layer.value].append(component)

        return dict(grouped)

    # ---------------------------------------------------------
    # Health
    # ---------------------------------------------------------

    def report(self) -> RuntimeRegistryReport:

        healthy = 0
        degraded = 0
        unavailable = 0
        unknown = 0

        for component in self._components.values():

            if component.health == ComponentHealth.HEALTHY:
                healthy += 1

            elif component.health == ComponentHealth.DEGRADED:
                degraded += 1

            elif component.health == ComponentHealth.UNAVAILABLE:
                unavailable += 1

            else:
                unknown += 1

        status = "healthy"

        if unavailable:
            status = "degraded"

        elif degraded:
            status = "warning"

        return RuntimeRegistryReport(
            status=status,
            component_count=len(self._components),
            healthy_count=healthy,
            degraded_count=degraded,
            unavailable_count=unavailable,
            unknown_count=unknown,
        )

    # ---------------------------------------------------------
    # Dependency Graph
    # ---------------------------------------------------------

    def dependency_graph(self):

        graph = {}

        for component in self._components.values():

            graph[component.component_id] = list(
                component.dependencies
            )

        return graph

    def dependents_of(self, component_id: str):

        dependents = []

        for component in self._components.values():

            if component_id in component.dependencies:
                dependents.append(component.component_id)

        return dependents

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def statistics(self):

        grouped = self.grouped_by_layer()

        return {
            "total_components": len(self._components),
            "layers": {
                layer: len(components)
                for layer, components in grouped.items()
            },
        }

    # ---------------------------------------------------------
    # Boot Summary
    # ---------------------------------------------------------

    def boot_summary(self):

        report = self.report()

        return {
            "status": report.status,
            "components": report.component_count,
            "health": {
                "healthy": report.healthy_count,
                "degraded": report.degraded_count,
                "unavailable": report.unavailable_count,
                "unknown": report.unknown_count,
            },
            "layers": self.statistics()["layers"],
        }
