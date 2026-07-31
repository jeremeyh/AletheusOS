"""In-memory institutional event store owned by Constitutional Ledger."""

from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime

from .institutional_events import InstitutionalLedgerEvent


def _parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


class DuplicateInstitutionalEventError(ValueError):
    """Raised when an institutional event identity already exists."""


class InstitutionalEventStore:
    """Append-only institutional history maintained by Ledger."""

    def __init__(self) -> None:
        self._events: dict[str, InstitutionalLedgerEvent] = {}
        self._order: list[str] = []

    def append(
        self,
        event: InstitutionalLedgerEvent,
    ) -> InstitutionalLedgerEvent:
        if event.event_id in self._events:
            raise DuplicateInstitutionalEventError(
                f"Institutional event {event.event_id!r} already exists."
            )

        self._events[event.event_id] = event
        self._order.append(event.event_id)
        return event

    def append_many(
        self,
        events: Iterable[InstitutionalLedgerEvent],
    ) -> tuple[InstitutionalLedgerEvent, ...]:
        return tuple(self.append(event) for event in events)

    def get(
        self,
        event_id: str,
    ) -> InstitutionalLedgerEvent | None:
        return self._events.get(event_id)

    def all(self) -> tuple[InstitutionalLedgerEvent, ...]:
        return tuple(self._events[event_id] for event_id in self._order)

    def by_source(
        self,
        source_identity: str,
    ) -> tuple[InstitutionalLedgerEvent, ...]:
        return tuple(
            event for event in self.all() if event.source_identity == source_identity
        )

    def by_type(
        self,
        event_type: str,
    ) -> tuple[InstitutionalLedgerEvent, ...]:
        return tuple(event for event in self.all() if event.event_type == event_type)

    def by_correlation(
        self,
        correlation_id: str,
    ) -> tuple[InstitutionalLedgerEvent, ...]:
        return tuple(
            event for event in self.all() if event.correlation_id == correlation_id
        )

    def effective_between(
        self,
        start_at: str,
        end_at: str,
    ) -> tuple[InstitutionalLedgerEvent, ...]:
        start = _parse_timestamp(start_at)
        end = _parse_timestamp(end_at)

        return tuple(
            event
            for event in self.all()
            if start <= _parse_timestamp(event.effective_at) <= end
        )

    def recorded_between(
        self,
        start_at: str,
        end_at: str,
    ) -> tuple[InstitutionalLedgerEvent, ...]:
        start = _parse_timestamp(start_at)
        end = _parse_timestamp(end_at)

        return tuple(
            event
            for event in self.all()
            if start <= _parse_timestamp(event.recorded_at) <= end
        )

    def statistics(self) -> dict:
        return {
            "institutional_events": len(self._events),
            "event_types": sorted(
                {event.event_type for event in self._events.values()}
            ),
            "source_identities": sorted(
                {event.source_identity for event in self._events.values()}
            ),
            "certified": sum(event.certified for event in self._events.values()),
        }
