from __future__ import annotations

import pytest

from aletheus.constitutional_events import (
    ConstitutionalEventFabric,
    LedgerEventSubscriber,
)
from aletheus.constitutional_ledger import ConstitutionalLedger
from aletheus.constitutional_missions import (
    ConstitutionalMissionEngine,
    InvalidMissionTransitionError,
    MissionStatus,
    create_security_containment_mission,
)


def build_engine():
    ledger = ConstitutionalLedger()
    fabric = ConstitutionalEventFabric()

    fabric.subscribe_all(
        LedgerEventSubscriber(ledger),
        subscriber_name="constitutional_ledger",
    )

    engine = ConstitutionalMissionEngine(fabric=fabric)

    return engine, fabric, ledger


def join_required_institutions(engine, mission):
    for institution_id in mission.contract.required_institutions:
        engine.join(
            mission.mission_id,
            institution_id,
        )


def attach_required_evidence(engine, mission):
    for evidence_type in mission.contract.required_evidence_types:
        engine.attach_evidence(
            mission.mission_id,
            evidence_type=evidence_type,
            evidence={
                "status": "verified",
                "evidence_type": evidence_type,
            },
            source_identity="aletheus.security_civilization",
        )


def test_creates_canonical_security_mission():
    engine, _, _ = build_engine()

    mission = create_security_containment_mission(
        entity_id="plugin.untrusted",
        severity="critical",
    )

    engine.create(mission)

    assert mission.status == MissionStatus.PLANNED
    assert engine.registry.get(mission.mission_id) is mission
    assert mission.event_ids


def test_mission_requires_authorization_before_start():
    engine, _, _ = build_engine()

    mission = create_security_containment_mission(
        entity_id="runtime.module",
        severity="high",
    )
    engine.create(mission)
    join_required_institutions(engine, mission)

    with pytest.raises(InvalidMissionTransitionError):
        engine.start(mission.mission_id)


def test_mission_requires_all_participants():
    engine, _, _ = build_engine()

    mission = create_security_containment_mission(
        entity_id="repository.module",
        severity="critical",
    )
    engine.create(mission)
    engine.authorize(mission.mission_id)

    with pytest.raises(ValueError):
        engine.start(mission.mission_id)


def test_complete_security_mission_lifecycle():
    engine, _, ledger = build_engine()

    mission = create_security_containment_mission(
        entity_id="plugin.untrusted",
        severity="critical",
    )

    engine.create(mission)
    engine.authorize(mission.mission_id)
    join_required_institutions(engine, mission)
    engine.start(mission.mission_id)
    attach_required_evidence(engine, mission)
    engine.complete(mission.mission_id)

    assert mission.status == MissionStatus.COMPLETED
    assert mission.completed_at is not None

    history = engine.history(mission.mission_id)

    event_types = [event.event_type.value for event in history]

    assert event_types[0] == "MissionCreated"
    assert "MissionAuthorized" in event_types
    assert "MissionStarted" in event_types
    assert event_types[-1] == "MissionCompleted"

    replay = ledger.replay_events(correlation_id=mission.correlation_id)

    assert len(replay) == len(history)


def test_transtemporal_lineage_reconstructs_mission():
    engine, _, ledger = build_engine()

    mission = create_security_containment_mission(
        entity_id="dependency.graph",
        severity="high",
    )

    engine.create(mission)
    engine.authorize(mission.mission_id)
    join_required_institutions(engine, mission)
    engine.start(mission.mission_id)
    attach_required_evidence(engine, mission)
    engine.complete(mission.mission_id)

    lineage = ledger.temporal_lineage(mission.event_ids[-1])

    assert lineage[0].event_type == "MissionCreated"
    assert lineage[-1].event_type == "MissionCompleted"
    assert len(lineage) == len(mission.event_ids)


def test_mission_cannot_complete_without_evidence():
    engine, _, _ = build_engine()

    mission = create_security_containment_mission(
        entity_id="service.runtime",
        severity="medium",
    )

    engine.create(mission)
    engine.authorize(mission.mission_id)
    join_required_institutions(engine, mission)
    engine.start(mission.mission_id)

    with pytest.raises(ValueError):
        engine.complete(mission.mission_id)


def test_unauthorized_institution_cannot_join():
    engine, _, _ = build_engine()

    mission = create_security_containment_mission(
        entity_id="service.runtime",
        severity="medium",
    )
    engine.create(mission)

    with pytest.raises(ValueError):
        engine.join(
            mission.mission_id,
            "aletheus.unauthorized",
        )
