from datetime import datetime
from uuid import UUID

import pytest

from aletheus.platform_intelligence import (
    ConstitutionalEvent,
    ConstitutionalEventKind,
    ConstitutionalEventSeverity,
    ConstitutionalEventValidationError,
)


def test_event_creation() -> None:
    event = ConstitutionalEvent.create(
        kind=ConstitutionalEventKind.PLATFORM_STARTED,
        source="runtime.core",
        subject="runtime.core",
    )

    assert isinstance(event.event_id, UUID)
    assert event.kind is ConstitutionalEventKind.PLATFORM_STARTED
    assert event.severity is ConstitutionalEventSeverity.INFO
    assert event.occurred_at.tzinfo is not None


def test_event_payload_is_immutable() -> None:
    event = ConstitutionalEvent.create(
        kind=ConstitutionalEventKind.OBJECT_UPDATED,
        source="service.registry",
        subject="service.workspace",
        payload={"state": "running"},
    )

    with pytest.raises(TypeError):
        event.payload["state"] = "stopped"  # type: ignore[index]


def test_naive_timestamp_is_rejected() -> None:
    with pytest.raises(
        ConstitutionalEventValidationError,
        match="timezone",
    ):
        ConstitutionalEvent.create(
            kind=ConstitutionalEventKind.PLATFORM_STARTED,
            source="runtime.core",
            subject="runtime.core",
            occurred_at=datetime.now(),
        )


def test_negative_sequence_is_rejected() -> None:
    event = ConstitutionalEvent.create(
        kind=ConstitutionalEventKind.PLATFORM_STARTED,
        source="runtime.core",
        subject="runtime.core",
    )

    with pytest.raises(
        ConstitutionalEventValidationError,
        match="negative",
    ):
        event.with_sequence(-1)


def test_event_can_be_sequenced_immutably() -> None:
    event = ConstitutionalEvent.create(
        kind=ConstitutionalEventKind.PLATFORM_STARTED,
        source="runtime.core",
        subject="runtime.core",
    )

    sequenced = event.with_sequence(7)

    assert event.sequence is None
    assert sequenced.sequence == 7
    assert sequenced.event_id == event.event_id


def test_causation_preserves_correlation() -> None:
    cause = ConstitutionalEvent.create(
        kind=ConstitutionalEventKind.SERVICE_REGISTERED,
        source="service.registry",
        subject="service.workspace",
    )

    effect = ConstitutionalEvent.create(
        kind=ConstitutionalEventKind.SERVICE_STARTED,
        source="service.lifecycle",
        subject="service.workspace",
    ).caused_by(cause)

    assert effect.causation_id == cause.event_id
    assert effect.correlation_id == cause.correlation_id


def test_integrity_hash_is_deterministic() -> None:
    event = ConstitutionalEvent.create(
        kind=ConstitutionalEventKind.PLATFORM_STARTED,
        source="runtime.core",
        subject="runtime.core",
        payload={"version": "9.2.0"},
    )

    assert event.integrity_hash() == event.integrity_hash()


def test_envelope_contains_integrity_hash() -> None:
    event = ConstitutionalEvent.create(
        kind=ConstitutionalEventKind.PLATFORM_STARTED,
        source="runtime.core",
        subject="runtime.core",
    )

    envelope = event.to_envelope()

    assert envelope["kind"] == "platform.started"
    assert len(envelope["integrity_hash"]) == 64
