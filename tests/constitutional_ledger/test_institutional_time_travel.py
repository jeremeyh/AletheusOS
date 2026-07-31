from __future__ import annotations

from aletheus.constitutional_ledger import ConstitutionalLedger


def test_records_generic_institutional_event():
    ledger = ConstitutionalLedger()

    event = ledger.record_event(
        {
            "event_type": "InstitutionEstablished",
            "source_identity": "aletheus.spa",
            "effective_at": "2026-07-01T10:00:00+00:00",
            "payload": {
                "status": "implemented",
            },
            "certified": True,
        }
    )

    assert event.event_type == "InstitutionEstablished"
    assert event.source_identity == "aletheus.spa"
    assert ledger.institutional_event(event.event_id) == event
    assert ledger.health()["institutional_events"] == 1


def test_accepts_civilization_bootstrap_event_shape():
    ledger = ConstitutionalLedger()

    event = ledger.record_event(
        {
            "event_id": "CIV-BOOT-001",
            "event_type": "CivilizationBootstrapCompleted",
            "source": "aletheus.institutional_civilization",
            "timestamp": "2026-07-14T08:30:00+00:00",
            "payload": {
                "status": "ready",
                "synthetic_harmony": 100.0,
            },
        }
    )

    assert event.event_id == "CIV-BOOT-001"
    assert event.source_identity == ("aletheus.institutional_civilization")


def test_temporal_search_finds_empirical_history():
    ledger = ConstitutionalLedger()

    ledger.record_event(
        {
            "event_type": "PlatformAssessmentCompleted",
            "source_identity": "aletheus.spa",
            "effective_at": "2026-07-01T10:00:00+00:00",
            "payload": {
                "score": 91.0,
                "finding": "runtime coupling",
            },
        }
    )

    results = ledger.temporal_search(
        "runtime coupling",
        source_identity="aletheus.spa",
    )

    assert len(results) == 1
    assert results[0].payload["score"] == 91.0


def test_snapshot_reconstructs_latest_state_as_of_time():
    ledger = ConstitutionalLedger()

    ledger.record_event(
        {
            "event_type": "InstitutionHealthChanged",
            "source_identity": "aletheus.watch_tower",
            "effective_at": "2026-07-01T10:00:00+00:00",
            "payload": {"health": 70.0},
        }
    )
    ledger.record_event(
        {
            "event_type": "InstitutionHealthChanged",
            "source_identity": "aletheus.watch_tower",
            "effective_at": "2026-07-02T10:00:00+00:00",
            "payload": {"health": 95.0},
        }
    )

    snapshot = ledger.as_of(
        "2026-07-01T23:59:59+00:00",
        source_identity="aletheus.watch_tower",
    )

    assert len(snapshot.events) == 1
    assert snapshot.events[0].payload["health"] == 70.0


def test_temporal_comparison_exposes_changed_state():
    ledger = ConstitutionalLedger()

    ledger.record_event(
        {
            "event_type": "InstitutionHealthChanged",
            "source_identity": "aletheus.spa",
            "effective_at": "2026-07-01T10:00:00+00:00",
            "payload": {"health": 82.0},
        }
    )
    ledger.record_event(
        {
            "event_type": "InstitutionHealthChanged",
            "source_identity": "aletheus.spa",
            "effective_at": "2026-07-03T10:00:00+00:00",
            "payload": {"health": 98.0},
        }
    )

    difference = ledger.compare_time(
        "2026-07-01T23:59:59+00:00",
        "2026-07-03T23:59:59+00:00",
        source_identity="aletheus.spa",
    )

    assert len(difference.changed) == 1
    assert difference.changed[0]["before"]["payload"]["health"] == 82.0
    assert difference.changed[0]["after"]["payload"]["health"] == 98.0


def test_replay_orders_correlated_events():
    ledger = ConstitutionalLedger()

    ledger.record_event(
        {
            "event_type": "WatchTowerAssessmentCompleted",
            "source_identity": "aletheus.watch_tower",
            "effective_at": "2026-07-14T08:00:00+00:00",
            "correlation_id": "BOOT-001",
        }
    )
    ledger.record_event(
        {
            "event_type": "CivilizationBootstrapCompleted",
            "source_identity": "aletheus.institutional_civilization",
            "effective_at": "2026-07-14T08:01:00+00:00",
            "correlation_id": "BOOT-001",
        }
    )

    replay = ledger.replay_events(correlation_id="BOOT-001")

    assert len(replay) == 2
    assert replay[0].event_type == "WatchTowerAssessmentCompleted"
    assert replay[1].event_type == "CivilizationBootstrapCompleted"
