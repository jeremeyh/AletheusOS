"""Constitutional Runtime Kernel composition root."""

from __future__ import annotations

from datetime import UTC, datetime
from threading import RLock
from typing import Any

from aletheus.platform_intelligence.constitutional import (
    ConstitutionalHealth,
    ConstitutionalState,
)
from aletheus.platform_intelligence.constitutional_dependency_manager import (
    ConstitutionalDependencyManager,
    ConstitutionalDependencyPlan,
)
from aletheus.platform_intelligence.constitutional_graph import (
    ConstitutionalGraph,
)
from aletheus.platform_intelligence.digital_twin import (
    PlatformDigitalTwin,
)
from aletheus.platform_intelligence.event_bus import (
    ConstitutionalEventBus,
)
from aletheus.platform_intelligence.events import (
    ConstitutionalEvent,
    ConstitutionalEventKind,
)
from aletheus.platform_intelligence.intelligence_engine import (
    PlatformIntelligenceEngine,
)
from aletheus.platform_intelligence.mission_engine import (
    ConstitutionalMissionEngine,
)
from aletheus.platform_intelligence.mission_scheduler import (
    ConstitutionalMissionScheduler,
)
from aletheus.platform_intelligence.orchestrator import (
    RuntimeIntelligenceOrchestrator,
)
from aletheus.platform_intelligence.runtime_explorer import (
    RuntimeExplorer,
)
from aletheus.platform_intelligence.service_registry import (
    PlatformServiceDefinition,
    PlatformServiceRegistry,
)

from .exceptions import (
    KernelCompositionError,
    KernelLifecycleError,
    KernelServiceRegistrationError,
)
from .models import (
    ConstitutionalRuntimeKernelSnapshot,
    ConstitutionalRuntimeKernelState,
    ConstitutionalRuntimeKernelStatus,
)


class ConstitutionalRuntimeKernel:
    """
    Composition root for the Platform Intelligence Fabric.

    CRK instantiates, wires, starts, stops, and exposes bounded subsystems.
    It does not absorb registry, graph, Twin, Explorer, intelligence,
    mission, scheduler, event, or orchestration behavior.
    """

    VERSION = "9.11.0"

    _CANONICAL_SERVICES = (
        (
            "service.platform-intelligence.event-bus",
            "Constitutional Event Bus",
            (),
        ),
        (
            "service.platform-intelligence.service-registry",
            "Platform Service Registry",
            (
                "service.platform-intelligence.event-bus",
            ),
        ),
        (
            "service.platform-intelligence.constitutional-graph",
            "Constitutional Graph",
            (
                "service.platform-intelligence.service-registry",
            ),
        ),
        (
            "service.platform-intelligence.digital-twin",
            "Platform Digital Twin",
            (
                "service.platform-intelligence.event-bus",
                "service.platform-intelligence.service-registry",
                "service.platform-intelligence.constitutional-graph",
            ),
        ),
        (
            "service.platform-intelligence.runtime-explorer",
            "Runtime Explorer",
            (
                "service.platform-intelligence.digital-twin",
                "service.platform-intelligence.constitutional-graph",
            ),
        ),
        (
            "service.platform-intelligence.intelligence-engine",
            "Platform Intelligence Engine",
            (
                "service.platform-intelligence.runtime-explorer",
            ),
        ),
        (
            "service.platform-intelligence.mission-engine",
            "Constitutional Mission Engine",
            (
                "service.platform-intelligence.event-bus",
            ),
        ),
        (
            "service.platform-intelligence.mission-scheduler",
            "Constitutional Mission Scheduler",
            (
                "service.platform-intelligence.mission-engine",
            ),
        ),
        (
            "service.platform-intelligence.orchestrator",
            "Runtime Intelligence Orchestrator",
            (
                "service.platform-intelligence.digital-twin",
                "service.platform-intelligence.runtime-explorer",
                "service.platform-intelligence.intelligence-engine",
            ),
        ),
        (
            "service.platform-intelligence.crk",
            "Constitutional Runtime Kernel",
            (
                "service.platform-intelligence.event-bus",
                "service.platform-intelligence.service-registry",
                "service.platform-intelligence.constitutional-graph",
                "service.platform-intelligence.digital-twin",
                "service.platform-intelligence.runtime-explorer",
                "service.platform-intelligence.intelligence-engine",
                "service.platform-intelligence.mission-engine",
                "service.platform-intelligence.mission-scheduler",
                "service.platform-intelligence.orchestrator",
            ),
        ),
    )

    def __init__(
        self,
        *,
        auto_compose: bool = True,
    ) -> None:
        now = datetime.now(UTC)

        self._state = (
            ConstitutionalRuntimeKernelState.CREATED
        )
        self._created_at = now
        self._modified_at = now
        self._failure_reason: str | None = None
        self._lock = RLock()

        self._event_bus: (
            ConstitutionalEventBus | None
        ) = None
        self._service_registry: (
            PlatformServiceRegistry | None
        ) = None
        self._graph: ConstitutionalGraph | None = None
        self._dependency_manager: (
            ConstitutionalDependencyManager | None
        ) = None
        self._digital_twin: (
            PlatformDigitalTwin | None
        ) = None
        self._runtime_explorer: (
            RuntimeExplorer | None
        ) = None
        self._intelligence_engine: (
            PlatformIntelligenceEngine | None
        ) = None
        self._mission_engine: (
            ConstitutionalMissionEngine | None
        ) = None
        self._mission_scheduler: (
            ConstitutionalMissionScheduler | None
        ) = None
        self._orchestrator: (
            RuntimeIntelligenceOrchestrator | None
        ) = None

        if auto_compose:
            self.compose()

    @property
    def state(
        self,
    ) -> ConstitutionalRuntimeKernelState:
        return self._state

    @property
    def composed(self) -> bool:
        return self._state not in {
            ConstitutionalRuntimeKernelState.CREATED,
            ConstitutionalRuntimeKernelState.FAILED,
        }

    @property
    def running(self) -> bool:
        return (
            self._state
            is ConstitutionalRuntimeKernelState.RUNNING
        )

    @property
    def event_bus(self) -> ConstitutionalEventBus:
        return self._require(
            self._event_bus,
            "event_bus",
        )

    @property
    def service_registry(
        self,
    ) -> PlatformServiceRegistry:
        return self._require(
            self._service_registry,
            "service_registry",
        )

    @property
    def graph(self) -> ConstitutionalGraph:
        return self._require(
            self._graph,
            "graph",
        )

    @property
    def dependency_manager(
        self,
    ) -> ConstitutionalDependencyManager:
        return self._require(
            self._dependency_manager,
            "dependency_manager",
        )

    @property
    def digital_twin(self) -> PlatformDigitalTwin:
        return self._require(
            self._digital_twin,
            "digital_twin",
        )

    @property
    def runtime_explorer(self) -> RuntimeExplorer:
        return self._require(
            self._runtime_explorer,
            "runtime_explorer",
        )

    @property
    def intelligence_engine(
        self,
    ) -> PlatformIntelligenceEngine:
        return self._require(
            self._intelligence_engine,
            "intelligence_engine",
        )

    @property
    def mission_engine(
        self,
    ) -> ConstitutionalMissionEngine:
        return self._require(
            self._mission_engine,
            "mission_engine",
        )

    @property
    def mission_scheduler(
        self,
    ) -> ConstitutionalMissionScheduler:
        return self._require(
            self._mission_scheduler,
            "mission_scheduler",
        )

    @property
    def orchestrator(
        self,
    ) -> RuntimeIntelligenceOrchestrator:
        return self._require(
            self._orchestrator,
            "orchestrator",
        )

    def compose(
        self,
    ) -> ConstitutionalRuntimeKernel:
        with self._lock:
            if self._state is not (
                ConstitutionalRuntimeKernelState.CREATED
            ):
                raise KernelLifecycleError(
                    "CRK can only be composed from "
                    "the created state."
                )

            try:
                event_bus = ConstitutionalEventBus()

                service_registry = (
                    PlatformServiceRegistry(
                        event_bus=event_bus
                    )
                )

                graph = ConstitutionalGraph()

                digital_twin = PlatformDigitalTwin(
                    service_registry=service_registry,
                    graph=graph,
                    event_bus=event_bus,
                )

                runtime_explorer = RuntimeExplorer(
                    twin=digital_twin,
                    graph=graph,
                    service_registry=(
                        service_registry
                    ),
                )

                intelligence_engine = (
                    PlatformIntelligenceEngine(
                        explorer=runtime_explorer,
                        graph=graph,
                    )
                )

                mission_engine = (
                    ConstitutionalMissionEngine(
                        event_bus=event_bus
                    )
                )

                mission_scheduler = (
                    ConstitutionalMissionScheduler()
                )

                orchestrator = (
                    RuntimeIntelligenceOrchestrator(
                        service_registry=(
                            service_registry
                        ),
                        graph=graph,
                        event_bus=event_bus,
                        digital_twin=digital_twin,
                        explorer=runtime_explorer,
                        intelligence_engine=(
                            intelligence_engine
                        ),
                    )
                )

                self._event_bus = event_bus
                self._service_registry = (
                    service_registry
                )
                self._graph = graph
                self._digital_twin = digital_twin
                self._runtime_explorer = (
                    runtime_explorer
                )
                self._intelligence_engine = (
                    intelligence_engine
                )
                self._mission_engine = (
                    mission_engine
                )
                self._mission_scheduler = (
                    mission_scheduler
                )
                self._orchestrator = orchestrator

                self._register_canonical_services()

                self._dependency_manager = (
                    ConstitutionalDependencyManager(
                        service_registry=service_registry
                    )
                )

                validation = (
                    self._dependency_manager.validate()
                )

                if not validation.valid:
                    raise KernelCompositionError(
                        "CRK dependency topology is invalid."
                    )

                self._state = (
                    ConstitutionalRuntimeKernelState.COMPOSED
                )
                self._touch()

            except Exception as error:
                self._state = (
                    ConstitutionalRuntimeKernelState.FAILED
                )
                self._failure_reason = str(error)
                self._touch()

                raise KernelCompositionError(
                    "CRK composition failed."
                ) from error

        return self

    def start(
        self,
    ) -> ConstitutionalRuntimeKernelStatus:
        with self._lock:
            if self._state not in {
                ConstitutionalRuntimeKernelState.COMPOSED,
                ConstitutionalRuntimeKernelState.STOPPED,
            }:
                raise KernelLifecycleError(
                    "CRK can only start from composed "
                    "or stopped state."
                )

            self._state = (
                ConstitutionalRuntimeKernelState.STARTING
            )
            self._touch()

            try:
                boot_plan = (
                    self.dependency_manager
                    .build_boot_plan()
                )

                for level in boot_plan.levels:
                    for address in level.services:
                        service = (
                            self.service_registry.get(
                                address
                            )
                        )

                        states = (
                            (
                                ConstitutionalState.INITIALIZING,
                                ConstitutionalState.STARTING,
                                ConstitutionalState.RUNNING,
                            )
                            if service.state
                            is ConstitutionalState.REGISTERED
                            else (
                                ConstitutionalState.STARTING,
                                ConstitutionalState.RUNNING,
                            )
                        )

                        transitioned = (
                            self._transition_service(
                                address,
                                *states,
                            )
                        )

                        transitioned = (
                            self.service_registry
                            .report_health(
                                transitioned.address,
                                ConstitutionalHealth.HEALTHY,
                            )
                        )

                        self.graph.update_node(
                            transitioned
                        )

                self._state = (
                    ConstitutionalRuntimeKernelState.RUNNING
                )
                self._failure_reason = None
                self._touch()

                self.event_bus.publish(
                    ConstitutionalEvent.create(
                        kind=(
                            ConstitutionalEventKind.PLATFORM_STARTED
                        ),
                        source=(
                            "service.platform-intelligence.crk"
                        ),
                        subject=(
                            "service.platform-intelligence.crk"
                        ),
                        payload={
                            "version": self.VERSION,
                            "state": self._state.value,
                        },
                    )
                )

            except Exception as error:
                self._state = (
                    ConstitutionalRuntimeKernelState.FAILED
                )
                self._failure_reason = str(error)
                self._touch()
                raise

        return self.status()

    def stop(
        self,
    ) -> ConstitutionalRuntimeKernelStatus:
        with self._lock:
            if self._state is not (
                ConstitutionalRuntimeKernelState.RUNNING
            ):
                raise KernelLifecycleError(
                    "CRK can only stop from running state."
                )

            self._state = (
                ConstitutionalRuntimeKernelState.STOPPING
            )
            self._touch()

            shutdown_plan = (
                self.dependency_manager
                .build_shutdown_plan()
            )

            for level in shutdown_plan.levels:
                for address in level.services:
                    transitioned = (
                        self._transition_service(
                            address,
                            ConstitutionalState.STOPPING,
                            ConstitutionalState.STOPPED,
                        )
                    )

                    self.graph.update_node(
                        transitioned
                    )

            self._state = (
                ConstitutionalRuntimeKernelState.STOPPED
            )
            self._touch()

            self.event_bus.publish(
                ConstitutionalEvent.create(
                    kind=(
                        ConstitutionalEventKind.PLATFORM_STOPPED
                    ),
                    source=(
                        "service.platform-intelligence.crk"
                    ),
                    subject=(
                        "service.platform-intelligence.crk"
                    ),
                    payload={
                        "version": self.VERSION,
                        "state": self._state.value,
                    },
                )
            )

        return self.status()

    def status(
        self,
    ) -> ConstitutionalRuntimeKernelStatus:
        registry_stats = (
            self.service_registry.statistics()
            if self._service_registry is not None
            else None
        )
        graph_stats = (
            self.graph.statistics()
            if self._graph is not None
            else None
        )
        bus_stats = (
            self.event_bus.statistics()
            if self._event_bus is not None
            else None
        )

        return ConstitutionalRuntimeKernelStatus(
            state=self._state,
            version=self.VERSION,
            created_at=self._created_at,
            modified_at=self._modified_at,
            composed=self.composed,
            running=self.running,
            registered_services=(
                registry_stats.registered
                if registry_stats is not None
                else 0
            ),
            graph_nodes=(
                graph_stats.nodes
                if graph_stats is not None
                else 0
            ),
            graph_relationships=(
                graph_stats.relationships
                if graph_stats is not None
                else 0
            ),
            twin_revision=(
                self.digital_twin.revision
                if self._digital_twin is not None
                else 0
            ),
            event_subscribers=(
                bus_stats.subscriber_count
                if bus_stats is not None
                else 0
            ),
            mission_count=(
                self.mission_engine.statistics().total
                if self._mission_engine is not None
                else 0
            ),
            scheduled_missions=(
                self.mission_scheduler.statistics().registered
                if self._mission_scheduler
                is not None
                else 0
            ),
            failure_reason=self._failure_reason,
        )

    def boot_plan(
        self,
    ) -> ConstitutionalDependencyPlan:
        return (
            self.dependency_manager
            .build_boot_plan()
        )

    def shutdown_plan(
        self,
    ) -> ConstitutionalDependencyPlan:
        return (
            self.dependency_manager
            .build_shutdown_plan()
        )

    def restart_plan(
        self,
        address: str,
    ) -> ConstitutionalDependencyPlan:
        return (
            self.dependency_manager
            .build_restart_plan(address)
        )

    def overview(self) -> dict[str, Any]:
        return self.orchestrator.overview().to_dict()

    def snapshot(
        self,
    ) -> ConstitutionalRuntimeKernelSnapshot:
        return ConstitutionalRuntimeKernelSnapshot(
            generated_at=datetime.now(UTC),
            kernel=self.status().to_dict(),
            runtime=self.orchestrator.runtime_summary(),
            services=(
                self.orchestrator.service_inventory()
            ),
            graph=(
                self.orchestrator.dependency_summary()
            ),
            events=self.orchestrator.event_summary(),
            twin=self.digital_twin.current_state(),
            intelligence=(
                self.orchestrator
                .intelligence_summary()
                .to_dict()
            ),
            missions=self.mission_engine.snapshot(),
            scheduler=(
                self.mission_scheduler
                .statistics()
                .to_dict()
            ),
        )

    def close(self) -> None:
        """Release subscriptions owned by composed subsystems."""

        if self._digital_twin is not None:
            self._digital_twin.close()

    def _register_canonical_services(
        self,
    ) -> None:
        try:
            definitions = [
                PlatformServiceDefinition.create(
                    address=address,
                    canonical_name=name,
                    version=self.VERSION,
                    authority=(
                        "AletheusOS Constitution"
                    ),
                    owner=(
                        "Platform Intelligence Fabric"
                    ),
                    dependencies=dependencies,
                )
                for (
                    address,
                    name,
                    dependencies,
                ) in self._CANONICAL_SERVICES
            ]

            registered = (
                self.service_registry.register_many(
                    definitions
                )
            )

            self.graph.add_nodes(registered)

            for definition in definitions:
                for dependency in (
                    definition.dependencies
                ):
                    self.graph.connect(
                        source=definition.address,
                        target=dependency,
                        kind=(
                            self._dependency_kind()
                        ),
                    )

        except Exception as error:
            raise KernelServiceRegistrationError(
                "Unable to register canonical "
                "Platform Intelligence services."
            ) from error

    @staticmethod
    def _dependency_kind():
        from aletheus.platform_intelligence.constitutional import (
            RelationshipKind,
        )

        return RelationshipKind.DEPENDS_ON

    def _transition_service(
        self,
        address: str,
        *states: ConstitutionalState,
    ):
        service = self.service_registry.get(
            address
        )

        for state in states:
            service = (
                self.service_registry.transition(
                    service.address,
                    state,
                )
            )

        return service

    def _touch(self) -> None:
        self._modified_at = datetime.now(UTC)

    @staticmethod
    def _require(
        value: Any,
        name: str,
    ) -> Any:
        if value is None:
            raise KernelCompositionError(
                f"CRK component is unavailable: {name}"
            )

        return value
