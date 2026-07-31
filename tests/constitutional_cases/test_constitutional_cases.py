from __future__ import annotations

import pytest

from aletheus.constitutional_cases import (
    CaseStatus,
    ConstitutionalCaseEngine,
    InvalidCaseTransitionError,
    create_security_incident_case,
)
from aletheus.constitutional_events import (
    ConstitutionalEventFabric,
    LedgerEventSubscriber,
)
from aletheus.constitutional_ledger import ConstitutionalLedger


def build_engine():
    ledger = ConstitutionalLedger()
    fabric = ConstitutionalEventFabric()

    fabric.subscribe_all(
        LedgerEventSubscriber(ledger),
        subscriber_name="constitutional_ledger",
    )

    engine = ConstitutionalCaseEngine(fabric=fabric)

    return engine, fabric, ledger


def attach_required_evidence(engine, case):
    for evidence_type in case.contract.required_evidence_types:
        engine.attach_evidence(
            case.case_id,
            evidence_type=evidence_type,
            evidence={
                "status": "verified",
                "evidence_type": evidence_type,
            },
            source_identity="aletheus.security_civilization",
        )


def test_detects_and_opens_security_case():
    engine, _, _ = build_engine()

    case = create_security_incident_case(
        entity_id="plugin.untrusted",
        severity="critical",
    )

    engine.detect(case)
    engine.open(case.case_id)

    assert case.status == CaseStatus.OPEN
    assert case.event_ids


def test_case_can_span_multiple_permitted_missions():
    engine, _, _ = build_engine()

    case = create_security_incident_case(
        entity_id="repository.module",
        severity="high",
    )

    engine.detect(case)
    engine.open(case.case_id)

    engine.attach_mission(
        case.case_id,
        mission_id="MISSION-001",
        mission_type="security_containment",
    )
    engine.attach_mission(
        case.case_id,
        mission_id="MISSION-002",
        mission_type="security_verification",
    )

    assert case.mission_ids == [
        "MISSION-001",
        "MISSION-002",
    ]


def test_rejects_unpermitted_mission_type():
    engine, _, _ = build_engine()

    case = create_security_incident_case(
        entity_id="runtime.module",
        severity="medium",
    )

    engine.detect(case)

    with pytest.raises(ValueError):
        engine.attach_mission(
            case.case_id,
            mission_id="MISSION-INVALID",
            mission_type="unrelated_mission",
        )


def test_complete_case_lifecycle():
    engine, _, ledger = build_engine()

    case = create_security_incident_case(
        entity_id="service.runtime",
        severity="critical",
    )

    engine.detect(case)
    engine.open(case.case_id)
    engine.investigate(case.case_id)

    engine.attach_mission(
        case.case_id,
        mission_id="MISSION-SECURITY-001",
        mission_type="security_containment",
    )

    attach_required_evidence(engine, case)

    engine.contain(case.case_id)
    engine.resolve(case.case_id)
    engine.verify(case.case_id)
    engine.close(case.case_id)

    assert case.status == CaseStatus.CLOSED
    assert case.closed_at is not None

    history = engine.history(case.case_id)

    assert history[0].event_type.value == "CaseDetected"
    assert history[-1].event_type.value == "CaseClosed"

    replay = ledger.replay_events(correlation_id=case.correlation_id)

    assert len(replay) == len(history)


def test_transtemporal_lineage_reconstructs_case():
    engine, _, ledger = build_engine()

    case = create_security_incident_case(
        entity_id="dependency.graph",
        severity="high",
    )

    engine.detect(case)
    engine.open(case.case_id)
    engine.investigate(case.case_id)
    attach_required_evidence(engine, case)
    engine.contain(case.case_id)
    engine.resolve(case.case_id)
    engine.verify(case.case_id)
    engine.close(case.case_id)

    lineage = ledger.temporal_lineage(case.event_ids[-1])

    assert lineage[0].event_type == "CaseDetected"
    assert lineage[-1].event_type == "CaseClosed"
    assert len(lineage) == len(case.event_ids)


def test_case_cannot_resolve_without_evidence():
    engine, _, _ = build_engine()

    case = create_security_incident_case(
        entity_id="runtime.service",
        severity="high",
    )

    engine.detect(case)
    engine.open(case.case_id)
    engine.investigate(case.case_id)
    engine.contain(case.case_id)

    with pytest.raises(ValueError):
        engine.resolve(case.case_id)


def test_case_cannot_close_before_verification():
    engine, _, _ = build_engine()

    case = create_security_incident_case(
        entity_id="runtime.service",
        severity="medium",
    )

    engine.detect(case)
    engine.open(case.case_id)

    with pytest.raises(InvalidCaseTransitionError):
        engine.close(case.case_id)
