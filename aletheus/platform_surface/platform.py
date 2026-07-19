"""Canonical public facade for the AletheusOS platform."""

from __future__ import annotations

from typing import Any

from aletheus.civilization import (
    build_civilization_orchestrator,
)
from aletheus.constitutional_cognition import (
    MultiplicitousIntelligenceMesh,
)
from aletheus.constitutional_instrumentation import (
    CognitionInstrumentBridge,
    ConstitutionalInstrumentBus,
    build_cognition_instrumentation,
)
from aletheus.constitutional_scenarios import (
    ConstitutionalScenarioEngine,
    ConstitutionalScenarioRegistry,
    ScenarioInstrumentPublisher,
)

from .cases import CaseSurface
from .cognition import CognitionSurface
from .instrumentation import (
    InstrumentationSurface,
)
from .ledger import LedgerSurface
from .missions import MissionSurface
from .models import (
    PlatformHealth,
    PlatformRuntimeSnapshot,
)
from .runtime import RuntimeSurface
from .scenarios import ScenarioSurface
from .security import SecuritySurface


class AletheusPlatform:
    """
    Stable constitutional application boundary.

    Applications consume this facade rather than importing internal engines.
    """

    VERSION = "0.2.0"

    def __init__(
        self,
        *,
        orchestrator,
        cognition_mesh: MultiplicitousIntelligenceMesh,
        instrument_bus: ConstitutionalInstrumentBus,
        scenario_engine: ConstitutionalScenarioEngine,
    ) -> None:
        self._orchestrator = orchestrator
        self._cognition_mesh = cognition_mesh
        self._instrument_bus = instrument_bus
        self._scenario_engine = scenario_engine

        self.runtime = RuntimeSurface(
            orchestrator=orchestrator
        )

        self.security = SecuritySurface(
            orchestrator=orchestrator
        )

        self.cases = CaseSurface(
            case_engine=orchestrator.case_engine
        )

        self.missions = MissionSurface(
            mission_engine=orchestrator.mission_engine,
            time=orchestrator.time,
        )

        self.ledger = LedgerSurface(
            ledger=orchestrator.ledger
        )

        self.cognition = CognitionSurface(
            mesh=cognition_mesh
        )

        self.instrumentation = (
            InstrumentationSurface(
                bus=instrument_bus
            )
        )

        self.scenarios = ScenarioSurface(
            engine=scenario_engine
        )

    def health(self) -> PlatformHealth:
        runtime_health = self.runtime.health()

        components = dict(
            runtime_health.components
        )

        components.update(
            {
                "cognition": (
                    self.cognition.health()
                ),
                "instrumentation": (
                    self.instrumentation.health()
                ),
                "scenarios": (
                    self.scenarios.health()
                ),
            }
        )

        degraded = any(
            isinstance(component, dict)
            and component.get("status")
            in {
                "degraded",
                "failed",
                "offline",
            }
            for component in components.values()
        )

        return PlatformHealth(
            status=(
                "degraded"
                if degraded
                else "healthy"
            ),
            healthy=not degraded,
            components=components,
        )

    def snapshot(
        self,
    ) -> PlatformRuntimeSnapshot:
        runtime_snapshot = (
            self.runtime.snapshot()
        )

        details = dict(
            runtime_snapshot.details
        )

        details.update(
            {
                "cognition": (
                    self.cognition.health()
                ),
                "instrumentation": {
                    instrument_id: (
                        state.to_dict()
                    )
                    for instrument_id, state
                    in (
                        self.instrumentation
                        .snapshot()
                        .items()
                    )
                },
                "scenarios": (
                    self.scenarios.health()
                ),
            }
        )

        return PlatformRuntimeSnapshot(
            status=runtime_snapshot.status,
            version=runtime_snapshot.version,
            cases=runtime_snapshot.cases,
            missions=runtime_snapshot.missions,
            time_missions=(
                runtime_snapshot.time_missions
            ),
            time_phases=(
                runtime_snapshot.time_phases
            ),
            mission_executions=(
                runtime_snapshot
                .mission_executions
            ),
            phase_executions=(
                runtime_snapshot
                .phase_executions
            ),
            domain_events_published=(
                runtime_snapshot
                .domain_events_published
            ),
            ledger_events=(
                runtime_snapshot.ledger_events
            ),
            failures=runtime_snapshot.failures,
            details=details,
        )

    def version(self) -> str:
        return self.VERSION


def build_aletheus_platform(
    *,
    watch_tower: Any | None = None,
    guardian: Any | None = None,
    conclave: Any | None = None,
    containment_vault: Any | None = None,
    sentinel: Any | None = None,
    fabric=None,
    ledger=None,
    cognition_mesh: (
        MultiplicitousIntelligenceMesh
        | None
    ) = None,
    instrument_bus: (
        ConstitutionalInstrumentBus
        | None
    ) = None,
    cognition_bridge: (
        CognitionInstrumentBridge
        | None
    ) = None,
    scenario_engine: (
        ConstitutionalScenarioEngine
        | None
    ) = None,
    scenario_registry: (
        ConstitutionalScenarioRegistry
        | None
    ) = None,
) -> AletheusPlatform:
    """
    Construct one connected AletheusOS Platform Surface.

    Cognition, instrumentation, and scenario capabilities are composed once
    here and exposed through stable public surfaces.
    """

    orchestrator = (
        build_civilization_orchestrator(
            watch_tower=watch_tower,
            guardian=guardian,
            conclave=conclave,
            containment_vault=(
                containment_vault
            ),
            sentinel=sentinel,
            fabric=fabric,
            ledger=ledger,
        )
    )

    resolved_bus = instrument_bus
    resolved_bridge = cognition_bridge

    if (
        resolved_bus is None
        and resolved_bridge is None
    ):
        (
            resolved_bus,
            resolved_bridge,
        ) = build_cognition_instrumentation()

    elif (
        resolved_bus is not None
        and resolved_bridge is None
    ):
        resolved_bridge = (
            CognitionInstrumentBridge(
                bus=resolved_bus
            )
        )

    elif (
        resolved_bus is None
        and resolved_bridge is not None
    ):
        resolved_bus = resolved_bridge.bus

    if resolved_bus is None:
        raise RuntimeError(
            "Instrument bus resolution failed."
        )

    if resolved_bridge is None:
        raise RuntimeError(
            "Cognition bridge resolution failed."
        )

    if cognition_mesh is None:
        resolved_mesh = (
            MultiplicitousIntelligenceMesh(
                observer=resolved_bridge
            )
        )
    else:
        resolved_mesh = cognition_mesh

    if scenario_engine is None:
        scenario_instruments = (
            ScenarioInstrumentPublisher(
                bus=resolved_bus
            )
        )

        resolved_scenario_engine = (
            ConstitutionalScenarioEngine(
                mesh=resolved_mesh,
                registry=(
                    scenario_registry
                    or ConstitutionalScenarioRegistry()
                ),
                instruments=(
                    scenario_instruments
                ),
            )
        )
    else:
        resolved_scenario_engine = (
            scenario_engine
        )

    return AletheusPlatform(
        orchestrator=orchestrator,
        cognition_mesh=resolved_mesh,
        instrument_bus=resolved_bus,
        scenario_engine=(
            resolved_scenario_engine
        ),
    )
