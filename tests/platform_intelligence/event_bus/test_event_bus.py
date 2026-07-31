from __future__ import annotations

from uuid import UUID

import pytest

from aletheus.platform_intelligence import (
    ConstitutionalEvent,
    ConstitutionalEventBus,
    ConstitutionalEventKind,
    DuplicateSubscriptionError,
    EventPublicationError,
    SubscriptionNotFoundError,
)


def make_event(
    kind: ConstitutionalEventKind = (ConstitutionalEventKind.PLATFORM_STARTED),
    *,
    source: str = "runtime.core",
    subject: str = "runtime.core",
) -> ConstitutionalEvent:
    return ConstitutionalEvent.create(
        kind=kind,
        source=source,
        subject=subject,
    )


def test_publish_assigns_monotonic_sequence() -> None:
    bus = ConstitutionalEventBus()

    first = bus.publish(make_event())
    second = bus.publish(make_event())

    assert first.sequence == 0
    assert second.sequence == 1


def test_publish_does_not_mutate_original_event() -> None:
    bus = ConstitutionalEventBus()
    original = make_event()

    published = bus.publish(original)

    assert original.sequence is None
    assert published.sequence == 0
    assert published.event_id == original.event_id


def test_subscriber_receives_event() -> None:
    bus = ConstitutionalEventBus()
    received: list[ConstitutionalEvent] = []

    subscription_id = bus.subscribe(received.append)

    assert isinstance(subscription_id, UUID)

    published = bus.publish(make_event())

    assert received == [published]


def test_subscription_filters_by_kind() -> None:
    bus = ConstitutionalEventBus()
    received: list[ConstitutionalEvent] = []

    bus.subscribe(
        received.append,
        kinds={
            ConstitutionalEventKind.HEALTH_CHANGED,
        },
    )

    bus.publish(make_event())
    health = bus.publish(make_event(ConstitutionalEventKind.HEALTH_CHANGED))

    assert received == [health]


def test_subscription_filters_by_source_prefix() -> None:
    bus = ConstitutionalEventBus()
    received: list[ConstitutionalEvent] = []

    bus.subscribe(
        received.append,
        source_prefix="service.",
    )

    bus.publish(make_event(source="runtime.core"))
    service_event = bus.publish(make_event(source="service.registry"))

    assert received == [service_event]


def test_subscription_filters_by_subject_prefix() -> None:
    bus = ConstitutionalEventBus()
    received: list[ConstitutionalEvent] = []

    bus.subscribe(
        received.append,
        subject_prefix="workspace.",
    )

    bus.publish(make_event(subject="runtime.core"))
    workspace_event = bus.publish(make_event(subject="workspace.founder"))

    assert received == [workspace_event]


def test_object_subscriber_is_supported() -> None:
    bus = ConstitutionalEventBus()

    class Subscriber:
        def __init__(self) -> None:
            self.received: list[ConstitutionalEvent] = []

        def handle(
            self,
            event: ConstitutionalEvent,
        ) -> None:
            self.received.append(event)

    subscriber = Subscriber()
    bus.subscribe(subscriber)

    event = bus.publish(make_event())

    assert subscriber.received == [event]


def test_duplicate_subscription_is_rejected() -> None:
    bus = ConstitutionalEventBus()
    received: list[ConstitutionalEvent] = []

    bus.subscribe(received.append)

    with pytest.raises(DuplicateSubscriptionError):
        bus.subscribe(received.append)


def test_unsubscribe_stops_delivery() -> None:
    bus = ConstitutionalEventBus()
    received: list[ConstitutionalEvent] = []

    subscription_id = bus.subscribe(received.append)

    bus.unsubscribe(subscription_id)
    bus.publish(make_event())

    assert received == []


def test_unknown_subscription_cannot_be_removed() -> None:
    bus = ConstitutionalEventBus()

    with pytest.raises(SubscriptionNotFoundError):
        bus.unsubscribe(UUID(int=0))


def test_batch_preserves_order() -> None:
    bus = ConstitutionalEventBus()

    published = bus.publish_batch(
        [
            make_event(ConstitutionalEventKind.PLATFORM_STARTED),
            make_event(ConstitutionalEventKind.SERVICE_REGISTERED),
            make_event(ConstitutionalEventKind.SERVICE_STARTED),
        ]
    )

    assert [event.sequence for event in published] == [0, 1, 2]


def test_history_is_bounded() -> None:
    bus = ConstitutionalEventBus(history_limit=2)

    bus.publish(make_event())
    second = bus.publish(make_event())
    third = bus.publish(make_event())

    assert bus.history() == (
        second,
        third,
    )


def test_zero_history_disables_retention() -> None:
    bus = ConstitutionalEventBus(history_limit=0)

    bus.publish(make_event())

    assert bus.history() == ()


def test_history_can_filter_by_kind() -> None:
    bus = ConstitutionalEventBus()

    bus.publish(make_event())
    health = bus.publish(make_event(ConstitutionalEventKind.HEALTH_CHANGED))

    assert bus.history(kinds={ConstitutionalEventKind.HEALTH_CHANGED}) == (health,)


def test_history_can_filter_after_sequence() -> None:
    bus = ConstitutionalEventBus()

    bus.publish(make_event())
    second = bus.publish(make_event())
    third = bus.publish(make_event())

    assert bus.history(after_sequence=0) == (
        second,
        third,
    )


def test_replay_delivers_retained_history() -> None:
    bus = ConstitutionalEventBus()
    bus.publish(make_event())
    bus.publish(make_event())

    replayed: list[ConstitutionalEvent] = []

    count = bus.replay(replayed.append)

    assert count == 2
    assert replayed == list(bus.history())


def test_replay_supports_filters() -> None:
    bus = ConstitutionalEventBus()

    bus.publish(make_event())
    health = bus.publish(make_event(ConstitutionalEventKind.HEALTH_CHANGED))

    replayed: list[ConstitutionalEvent] = []

    count = bus.replay(
        replayed.append,
        kinds={ConstitutionalEventKind.HEALTH_CHANGED},
    )

    assert count == 1
    assert replayed == [health]


def test_non_strict_dispatch_records_failure() -> None:
    bus = ConstitutionalEventBus(strict_dispatch=False)

    def fail(
        event: ConstitutionalEvent,
    ) -> None:
        raise RuntimeError("subscriber failed")

    bus.subscribe(fail)

    published = bus.publish(make_event())
    stats = bus.statistics()

    assert published.sequence == 0
    assert stats.failed_deliveries == 1


def test_strict_dispatch_raises() -> None:
    bus = ConstitutionalEventBus(strict_dispatch=True)

    def fail(
        event: ConstitutionalEvent,
    ) -> None:
        raise RuntimeError("subscriber failed")

    bus.subscribe(fail)

    with pytest.raises(EventPublicationError):
        bus.publish(make_event())


def test_statistics_are_consistent() -> None:
    bus = ConstitutionalEventBus()
    received: list[ConstitutionalEvent] = []

    bus.subscribe(received.append)

    first = bus.publish(make_event())
    bus.publish(make_event(ConstitutionalEventKind.HEALTH_CHANGED))

    stats = bus.statistics()

    assert stats.published == 2
    assert stats.delivered == 2
    assert stats.failed_deliveries == 0
    assert stats.subscriber_count == 1
    assert stats.history_size == 2
    assert stats.next_sequence == 2
    assert stats.events_by_kind["platform.started"] == 1
    assert stats.events_by_kind["health.changed"] == 1
    assert stats.last_event_id != str(first.event_id)


def test_clear_history_preserves_counters() -> None:
    bus = ConstitutionalEventBus()
    bus.publish(make_event())

    bus.clear_history()

    stats = bus.statistics()

    assert stats.history_size == 0
    assert stats.published == 1


def test_reset_clears_bus_state() -> None:
    bus = ConstitutionalEventBus()
    received: list[ConstitutionalEvent] = []

    bus.subscribe(received.append)
    bus.publish(make_event())

    bus.reset()

    stats = bus.statistics()

    assert stats.published == 0
    assert stats.delivered == 0
    assert stats.subscriber_count == 0
    assert stats.history_size == 0
    assert stats.next_sequence == 0
