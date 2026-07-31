from __future__ import annotations

import pytest

from aletheus.constitutional_events import (
    ConstitutionalEvent,
    ConstitutionalEventFabric,
    ConstitutionalEventType,
    EventCollector,
    LedgerEventSubscriber,
    build_canonical_event_registry,
)
from aletheus.constitutional_ledger import ConstitutionalLedger


def test_canonical_event_vocabulary_is_registered():
    registry = build_canonical_event_registry()

    assert registry.get(ConstitutionalEventType.INTEGRITY_FINDING_CREATED) is not None
    assert registry.get(ConstitutionalEventType.COUNCIL_DECISION_RECORDED) is not None
    assert registry.statistics()["event_types"] >= 15


def test_publishes_typed_event_to_specific_subscriber():
    fabric = ConstitutionalEventFabric()
    collector = EventCollector()

    fabric.subscribe(
        ConstitutionalEventType.PLATFORM_ASSESSMENT_COMPLETED,
        collector,
    )

    event = ConstitutionalEvent.create(
        ConstitutionalEventType.PLATFORM_ASSESSMENT_COMPLETED,
        "aletheus.spa",
        payload={"score": 97.0},
    )

    deliveries = fabric.publish(event)

    assert len(deliveries) == 1
    assert deliveries[0].delivered is True
    assert collector.events == [event]
    assert fabric.health()["events"] == 1


def test_global_ledger_subscriber_records_event_for_time_travel():
    ledger = ConstitutionalLedger()
    fabric = ConstitutionalEventFabric()
    ledger_subscriber = LedgerEventSubscriber(ledger)

    fabric.subscribe_all(
        ledger_subscriber,
        subscriber_name="constitutional_ledger",
    )

    event = ConstitutionalEvent.create(
        ConstitutionalEventType.WATCH_TOWER_ASSESSMENT_COMPLETED,
        "aletheus.watch_tower",
        payload={
            "status": "healthy",
            "findings": 0,
        },
        correlation_id="BOOT-001",
    )

    fabric.publish(event)

    history = ledger.institutional_history("aletheus.watch_tower")

    assert len(history) == 1
    assert history[0].event_id == event.event_id

    snapshot = ledger.as_of(event.effective_at)

    assert any(item.event_id == event.event_id for item in snapshot.events)


def test_certified_event_type_rejects_uncertified_event():
    fabric = ConstitutionalEventFabric()

    event = ConstitutionalEvent.create(
        ConstitutionalEventType.COUNCIL_DECISION_RECORDED,
        "aletheus.council",
        payload={"approved": True},
        certified=False,
    )

    with pytest.raises(ValueError):
        fabric.publish(event)


def test_certified_council_decision_is_recorded():
    ledger = ConstitutionalLedger()
    fabric = ConstitutionalEventFabric()
    fabric.subscribe_all(LedgerEventSubscriber(ledger))

    event = ConstitutionalEvent.create(
        ConstitutionalEventType.COUNCIL_DECISION_RECORDED,
        "aletheus.council",
        payload={
            "approved": True,
            "decision": "Proceed with institutional wiring.",
        },
        certified=True,
    )

    deliveries = fabric.publish(event)

    assert all(delivery.delivered for delivery in deliveries)

    results = ledger.temporal_search(
        "institutional wiring",
        source_identity="aletheus.council",
    )

    assert len(results) == 1
    assert results[0].certified is True


def test_replays_correlated_constitutional_history():
    fabric = ConstitutionalEventFabric()
    collector = EventCollector()

    fabric.subscribe_all(collector)

    first = ConstitutionalEvent.create(
        ConstitutionalEventType.CIVILIZATION_BOOTSTRAP_STARTED,
        "aletheus.institutional_civilization",
        correlation_id="BOOT-REPLAY-001",
    )
    second = ConstitutionalEvent.create(
        ConstitutionalEventType.PLATFORM_ASSESSMENT_COMPLETED,
        "aletheus.spa",
        correlation_id="BOOT-REPLAY-001",
        causation_id=first.event_id,
    )
    third = ConstitutionalEvent.create(
        ConstitutionalEventType.CIVILIZATION_BOOTSTRAP_COMPLETED,
        "aletheus.institutional_civilization",
        correlation_id="BOOT-REPLAY-001",
        causation_id=second.event_id,
    )

    fabric.publish(first)
    fabric.publish(second)
    fabric.publish(third)

    original_count = len(collector.events)

    deliveries = fabric.replay(correlation_id="BOOT-REPLAY-001")

    assert original_count == 3
    assert len(deliveries) == 3
    assert len(collector.events) == 6


def test_subscriber_failure_is_visible_without_losing_event():
    fabric = ConstitutionalEventFabric()

    def broken_subscriber(event):
        raise RuntimeError("subscriber unavailable")

    fabric.subscribe(
        ConstitutionalEventType.HOMEOSTASIS_UPDATED,
        broken_subscriber,
        subscriber_name="broken_homeostasis_consumer",
    )

    event = ConstitutionalEvent.create(
        ConstitutionalEventType.HOMEOSTASIS_UPDATED,
        "aletheus.homeostasis",
    )

    deliveries = fabric.publish(event)

    assert len(fabric.events()) == 1
    assert deliveries[0].delivered is False
    assert deliveries[0].error == "subscriber unavailable"
    assert fabric.health()["status"] == "degraded"
