from __future__ import annotations

from aletheus.constitutional_ledger import (
    ConstitutionalLedger,
    TimeTravel,
    TranstemporalEngine,
)


def test_ledger_uses_canonical_transtemporal_engine():
    ledger = ConstitutionalLedger()

    assert isinstance(
        ledger.transtemporal,
        TranstemporalEngine,
    )
    assert ledger.time_travel is ledger.transtemporal
    assert ledger.transtemporal.health()["name"] == (
        "Transtemporal Engine™"
    )


def test_time_travel_remains_compatibility_alias():
    ledger = ConstitutionalLedger()

    compatibility_engine = TimeTravel(
        ledger.institutional_events
    )

    assert isinstance(
        compatibility_engine,
        TranstemporalEngine,
    )


def test_transtemporal_lineage_traces_causality():
    ledger = ConstitutionalLedger()

    first = ledger.record_event({
        "event_id": "EVENT-ROOT",
        "event_type": "InstitutionProjected",
        "source_identity": "aletheus.spa",
        "effective_at": "2026-07-14T08:00:00+00:00",
    })

    second = ledger.record_event({
        "event_id": "EVENT-ASSESSMENT",
        "event_type": "PlatformAssessmentCompleted",
        "source_identity": "aletheus.spa",
        "effective_at": "2026-07-14T08:01:00+00:00",
        "causation_id": first.event_id,
    })

    third = ledger.record_event({
        "event_id": "EVENT-DECISION",
        "event_type": "CouncilDecisionRecorded",
        "source_identity": "aletheus.council",
        "effective_at": "2026-07-14T08:02:00+00:00",
        "causation_id": second.event_id,
        "certified": True,
    })

    lineage = ledger.temporal_lineage(third.event_id)

    assert [
        event.event_id
        for event in lineage
    ] == [
        "EVENT-ROOT",
        "EVENT-ASSESSMENT",
        "EVENT-DECISION",
    ]


def test_transtemporal_provenance_is_inspectable():
    ledger = ConstitutionalLedger()

    event = ledger.record_event({
        "event_id": "EVENT-PROVENANCE",
        "event_type": "InstitutionHealthChanged",
        "source_identity": "aletheus.watch_tower",
        "effective_at": "2026-07-14T09:00:00+00:00",
        "payload": {
            "health": 98.0,
        },
        "correlation_id": "BOOT-001",
    })

    provenance = ledger.temporal_provenance(
        event.event_id
    )

    assert provenance["found"] is True
    assert provenance["source_identity"] == (
        "aletheus.watch_tower"
    )
    assert provenance["correlation_id"] == "BOOT-001"
    assert len(provenance["lineage"]) == 1


def test_unknown_provenance_is_explicit():
    ledger = ConstitutionalLedger()

    provenance = ledger.temporal_provenance(
        "EVENT-DOES-NOT-EXIST"
    )

    assert provenance == {
        "event_id": "EVENT-DOES-NOT-EXIST",
        "found": False,
        "lineage": [],
    }
