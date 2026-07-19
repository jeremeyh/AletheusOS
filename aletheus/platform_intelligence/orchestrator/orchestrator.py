"""Runtime Intelligence Orchestrator façade."""

from __future__ import annotations

from typing import Any

from aletheus.platform_intelligence.constitutional_graph import (
    ConstitutionalGraph,
)
from aletheus.platform_intelligence.digital_twin import (
    PlatformDigitalTwin,
    TwinSnapshot,
)
from aletheus.platform_intelligence.event_bus import (
    ConstitutionalEventBus,
)
from aletheus.platform_intelligence.intelligence_engine import (
    PlatformIntelligenceAnalysis,
    PlatformIntelligenceEngine,
)
from aletheus.platform_intelligence.runtime_explorer import (
    RuntimeExplorer,
)
from aletheus.platform_intelligence.service_registry import (
    PlatformServiceRegistry,
)

from .models import (
    RuntimeConstitutionalState,
    RuntimeHealthSummary,
    RuntimeIntelligenceOverview,
)


class RuntimeIntelligenceOrchestrator:
    """
    Single read-only composition façade for Platform Intelligence.

    The orchestrator owns no platform state and performs no mutation. It
    coordinates existing bounded components into stable constitutional views.
    """

    def __init__(
        self,
        *,
        service_registry: PlatformServiceRegistry,
        graph: ConstitutionalGraph,
        event_bus: ConstitutionalEventBus,
        digital_twin: PlatformDigitalTwin,
        explorer: RuntimeExplorer,
        intelligence_engine: PlatformIntelligenceEngine,
    ) -> None:
        self._service_registry = service_registry
        self._graph = graph
        self._event_bus = event_bus
        self._digital_twin = digital_twin
        self._explorer = explorer
        self._intelligence_engine = (
            intelligence_engine
        )

    @property
    def revision(self) -> int:
        return self._digital_twin.revision

    def overview(
        self,
    ) -> RuntimeIntelligenceOverview:
        analysis = self.intelligence_summary()

        return RuntimeIntelligenceOverview.create(
            twin_revision=self.revision,
            runtime=self.runtime_summary(),
            services=self.service_inventory(),
            graph=self.dependency_summary(),
            events=self.event_summary(),
            health=self.health_summary(),
            constitution=(
                self.constitutional_state()
            ),
            intelligence=analysis.to_dict(),
        )

    def snapshot(
        self,
        *,
        retain: bool = True,
    ) -> TwinSnapshot:
        return self._digital_twin.snapshot(
            retain=retain
        )

    def runtime_summary(
        self,
    ) -> dict[str, Any]:
        state = self._digital_twin.current_state()

        return {
            "revision": state["revision"],
            "health": state["health"],
            "statistics": state["statistics"],
            "last_event": state["last_event"],
        }

    def service_inventory(
        self,
    ) -> dict[str, Any]:
        snapshot = self._service_registry.snapshot()

        return {
            "services": snapshot["services"],
            "statistics": snapshot["statistics"],
        }

    def dependency_summary(
        self,
    ) -> dict[str, Any]:
        snapshot = self._graph.snapshot()

        return {
            "nodes": snapshot["nodes"],
            "relationships": (
                snapshot["relationships"]
            ),
            "topology": snapshot["topology"],
            "statistics": snapshot["statistics"],
        }

    def event_summary(
        self,
    ) -> dict[str, Any]:
        statistics = (
            self._event_bus.statistics().to_dict()
        )
        history = self._event_bus.history()

        return {
            "statistics": statistics,
            "latest": (
                history[-1].to_envelope()
                if history
                else None
            ),
            "history_size": len(history),
        }

    def health_summary(
        self,
    ) -> RuntimeHealthSummary:
        projection = self._digital_twin.health()
        counts = projection.get("counts", {})

        return RuntimeHealthSummary(
            state=str(projection["state"]),
            total_services=int(
                projection["total_services"]
            ),
            healthy=int(counts.get("healthy", 0)),
            warning=int(counts.get("warning", 0)),
            degraded=int(
                counts.get("degraded", 0)
            ),
            critical=int(
                counts.get("critical", 0)
            ),
            offline=int(counts.get("offline", 0)),
            unknown=int(counts.get("unknown", 0)),
            unhealthy_services=tuple(
                projection.get(
                    "unhealthy_services",
                    (),
                )
            ),
        )

    def constitutional_state(
        self,
    ) -> RuntimeConstitutionalState:
        graph_stats = self._graph.statistics()

        broken_dependencies = 0

        for service in self._service_registry.all():
            for dependency in (
                self._service_registry.dependencies_of(
                    service.address
                )
            ):
                if not self._service_registry.contains(
                    dependency
                ):
                    broken_dependencies += 1

        checks = {
            "no_cycles": graph_stats.cycles == 0,
            "no_broken_dependencies": (
                broken_dependencies == 0
            ),
            "single_connected_component": (
                graph_stats.connected_components
                <= 1
                if graph_stats.nodes
                else True
            ),
            "no_orphans": graph_stats.orphans == 0,
        }

        return RuntimeConstitutionalState(
            satisfied=all(checks.values()),
            cycles=graph_stats.cycles,
            orphans=graph_stats.orphans,
            connected_components=(
                graph_stats.connected_components
            ),
            broken_dependencies=(
                broken_dependencies
            ),
            checks=checks,
        )

    def intelligence_summary(
        self,
    ) -> PlatformIntelligenceAnalysis:
        return self._intelligence_engine.analyze()

    def explorer_statistics(
        self,
    ) -> dict[str, Any]:
        return (
            self._explorer.statistics().to_dict()
        )

    def retained_snapshots(
        self,
    ) -> tuple[TwinSnapshot, ...]:
        return (
            self._digital_twin.retained_snapshots()
        )
