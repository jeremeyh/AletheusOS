from __future__ import annotations

import pytest

from aletheus.constitutional_events import (
    ConstitutionalEventFabric,
    LedgerEventSubscriber,
)
from aletheus.constitutional_ledger import ConstitutionalLedger
from aletheus.constitutional_time import (
    InvalidPhaseTransitionError,
    MissionPhaseContract,
    MissionPhaseGraph,
    PhaseCycleError,
    PhaseStatus,
    TetraInstitutionalMissionEngine,
    security_containment_phase_graph,
)


def build_time():
    ledger = ConstitutionalLedger()
    fabric = ConstitutionalEventFabric()

    fabric.subscribe_all(
        LedgerEventSubscriber(ledger),
        subscriber_name="constitutional_ledger",
    )

    time = TetraInstitutionalMissionEngine(
        fabric=fabric
    )

    return time, fabric, ledger


def join_phase(time, mission_id, phase_id):
    contract = time.graph(mission_id).require(
        phase_id
    )

    for institution_id in (
        contract.participating_institutions
    ):
        time.join(
            mission_id,
            phase_id=phase_id,
            institution_id=institution_id,
        )


def complete_phase(
    time,
    mission_id,
    phase_id,
):
    contract = time.graph(mission_id).require(
        phase_id
    )

    join_phase(time, mission_id, phase_id)

    time.start_phase(
        mission_id,
        phase_id,
    )

    for evidence_type in (
        contract.required_evidence_types
    ):
        time.attach_evidence(
            mission_id,
            phase_id=phase_id,
            evidence_type=evidence_type,
            evidence={
                "status": "verified",
                "phase_id": phase_id,
            },
            source_identity=(
                contract.participating_institutions[0]
            ),
        )

    time.complete_phase(
        mission_id,
        phase_id,
    )


def test_attaches_security_phase_graph():
    time, _, _ = build_time()

    state = time.attach_graph(
        mission_id="MISSION-TIME-001",
        correlation_id="CASE-TIME-001",
        graph=security_containment_phase_graph(),
    )

    assert len(state.phases) == 5
    assert time.eligible_phases(
        "MISSION-TIME-001"
    ) == ("detect",)


def test_phase_cannot_start_before_dependency():
    time, _, _ = build_time()

    time.attach_graph(
        mission_id="MISSION-TIME-002",
        correlation_id="CASE-TIME-002",
        graph=security_containment_phase_graph(),
    )

    join_phase(
        time,
        "MISSION-TIME-002",
        "classify",
    )

    with pytest.raises(
        InvalidPhaseTransitionError
    ):
        time.start_phase(
            "MISSION-TIME-002",
            "classify",
        )


def test_completing_phase_unlocks_next_phase():
    time, _, _ = build_time()

    time.attach_graph(
        mission_id="MISSION-TIME-003",
        correlation_id="CASE-TIME-003",
        graph=security_containment_phase_graph(),
    )

    complete_phase(
        time,
        "MISSION-TIME-003",
        "detect",
    )

    assert time.eligible_phases(
        "MISSION-TIME-003"
    ) == ("classify",)


def test_executes_complete_relative_sequence():
    time, _, ledger = build_time()

    mission_id = "MISSION-TIME-004"
    correlation_id = "CASE-TIME-004"

    time.attach_graph(
        mission_id=mission_id,
        correlation_id=correlation_id,
        graph=security_containment_phase_graph(),
    )

    for phase_id in (
        "detect",
        "classify",
        "contain",
        "preserve",
        "stabilize",
    ):
        complete_phase(
            time,
            mission_id,
            phase_id,
        )

    state = time.state(mission_id)

    assert time.sequence_completed(
        mission_id
    )
    assert state.completed_order == [
        "detect",
        "classify",
        "contain",
        "preserve",
        "stabilize",
    ]

    replay = ledger.replay_events(
        correlation_id=correlation_id
    )

    assert any(
        event.event_type
        == "MissionTemporalSequenceCompleted"
        for event in replay
    )


def test_phase_requires_evidence_before_completion():
    time, _, _ = build_time()

    mission_id = "MISSION-TIME-005"

    time.attach_graph(
        mission_id=mission_id,
        correlation_id="CASE-TIME-005",
        graph=security_containment_phase_graph(),
    )

    join_phase(
        time,
        mission_id,
        "detect",
    )
    time.start_phase(
        mission_id,
        "detect",
    )

    with pytest.raises(ValueError):
        time.complete_phase(
            mission_id,
            "detect",
        )


def test_failed_dependency_blocks_downstream_phase():
    time, _, _ = build_time()

    mission_id = "MISSION-TIME-006"

    time.attach_graph(
        mission_id=mission_id,
        correlation_id="CASE-TIME-006",
        graph=security_containment_phase_graph(),
    )

    join_phase(
        time,
        mission_id,
        "detect",
    )

    time.start_phase(
        mission_id,
        "detect",
    )

    time.fail_phase(
        mission_id,
        "detect",
        reason="Integrity finding invalid.",
    )

    state = time.state(mission_id)

    assert state.phases["detect"].status == (
        PhaseStatus.FAILED
    )
    assert state.phases["classify"].status == (
        PhaseStatus.BLOCKED
    )


def test_graph_rejects_cycles():
    graph = MissionPhaseGraph()

    graph.add(
        MissionPhaseContract(
            phase_id="one",
            canonical_name="One",
            purpose="One",
            dependencies=("two",),
        )
    )
    graph.add(
        MissionPhaseContract(
            phase_id="two",
            canonical_name="Two",
            purpose="Two",
            dependencies=("one",),
        )
    )

    with pytest.raises(PhaseCycleError):
        graph.validate()
