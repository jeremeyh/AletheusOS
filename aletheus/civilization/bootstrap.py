"""Bootstrap for the TIME-driven Civilization Orchestrator™."""

from __future__ import annotations

from typing import Any

from aletheus.constitutional_cases import (
    ConstitutionalCaseEngine,
)
from aletheus.constitutional_events import (
    ConstitutionalEventFabric,
    LedgerEventSubscriber,
)
from aletheus.constitutional_events.security import (
    register_security_event_types,
)
from aletheus.constitutional_ledger import ConstitutionalLedger
from aletheus.constitutional_missions import (
    ConstitutionalMissionEngine,
)
from aletheus.constitutional_time import (
    TetraInstitutionalMissionEngine,
)
from aletheus.mission_runtime import (
    ConstitutionalMissionRuntime,
    InstitutionExecutorRegistry,
    register_security_executors,
)

from .orchestrator import CivilizationOrchestrator


def build_civilization_orchestrator(
    *,
    watch_tower: Any | None = None,
    guardian: Any | None = None,
    conclave: Any | None = None,
    containment_vault: Any | None = None,
    sentinel: Any | None = None,
    fabric: ConstitutionalEventFabric | None = None,
    ledger: ConstitutionalLedger | None = None,
) -> CivilizationOrchestrator:
    resolved_ledger = ledger or ConstitutionalLedger()
    resolved_fabric = fabric or ConstitutionalEventFabric()

    resolved_fabric.subscribe_all(
        LedgerEventSubscriber(resolved_ledger),
        subscriber_name="constitutional_ledger",
    )

    register_security_event_types(resolved_fabric.registry)

    case_engine = ConstitutionalCaseEngine(fabric=resolved_fabric)

    mission_engine = ConstitutionalMissionEngine(fabric=resolved_fabric)

    time = TetraInstitutionalMissionEngine(fabric=resolved_fabric)

    executors = InstitutionExecutorRegistry()

    register_security_executors(
        executors,
        watch_tower=watch_tower,
        guardian=guardian,
        conclave=conclave,
        containment_vault=containment_vault,
        sentinel=sentinel,
    )

    mission_runtime = ConstitutionalMissionRuntime(
        time=time,
        executors=executors,
    )

    return CivilizationOrchestrator(
        ledger=resolved_ledger,
        case_engine=case_engine,
        mission_engine=mission_engine,
        time=time,
        mission_runtime=mission_runtime,
    )
