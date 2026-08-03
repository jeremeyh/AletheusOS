"""Transtemporal Engine™ for Constitutional Ledger."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from .institutional_event_store import InstitutionalEventStore
from .institutional_events import InstitutionalLedgerEvent


def _parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value)


@dataclass(frozen=True, slots=True)
class TemporalSnapshot:
    """
    Reconstructed institutional state at a specific effective time.

    The latest event for each source-identity/event-type pair at or before
    `as_of` represents the effective institutional state.
    """

    as_of: str
    events: tuple[InstitutionalLedgerEvent, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "as_of": self.as_of,
            "event_count": len(self.events),
            "events": [event.to_dict() for event in self.events],
        }


@dataclass(frozen=True, slots=True)
class TemporalDifference:
    """Difference between two reconstructed institutional states."""

    before: TemporalSnapshot
    after: TemporalSnapshot
    added: tuple[InstitutionalLedgerEvent, ...]
    removed: tuple[InstitutionalLedgerEvent, ...]
    changed: tuple[dict[str, Any], ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "before": self.before.to_dict(),
            "after": self.after.to_dict(),
            "added": [event.to_dict() for event in self.added],
            "removed": [event.to_dict() for event in self.removed],
            "changed": list(self.changed),
        }


class TranstemporalEngine:
    """
    Transtemporal Engine™

    Constitutional historical and cross-temporal reasoning capability.

    Responsibilities:
    - empirical historical search
    - point-in-time reconstruction
    - temporal state comparison
    - correlated event replay
    - institutional lineage inquiry
    - provenance and causality traversal

    Non-responsibilities:
    - wall-clock scheduling, owned by Hour Glass™
    - relative mission progression, owned by TIME™
    """

    VERSION = "0.1.0"

    def __init__(
        self,
        store: InstitutionalEventStore,
    ) -> None:
        self.store = store
        self._queries = 0

    def search(
        self,
        query: str,
        *,
        source_identity: str | None = None,
        event_type: str | None = None,
    ) -> tuple[InstitutionalLedgerEvent, ...]:
        """Search empirical institutional history."""

        self._queries += 1
        normalized = query.strip().casefold()
        results = []

        for event in self.store.all():
            if source_identity is not None and event.source_identity != source_identity:
                continue

            if event_type is not None and event.event_type != event_type:
                continue

            searchable = " ".join(
                [
                    event.event_id,
                    event.event_type,
                    event.source_identity,
                    repr(event.payload),
                    repr(event.evidence),
                    " ".join(event.tags),
                ]
            ).casefold()

            if not normalized or normalized in searchable:
                results.append(event)

        return tuple(results)

    def snapshot(
        self,
        as_of: str,
        *,
        source_identity: str | None = None,
    ) -> TemporalSnapshot:
        """Reconstruct effective institutional state at a point in time."""

        self._queries += 1
        boundary = _parse_timestamp(as_of)

        candidates = [
            event
            for event in self.store.all()
            if _parse_timestamp(event.effective_at) <= boundary
            and (source_identity is None or event.source_identity == source_identity)
        ]

        latest: dict[
            tuple[str, str],
            InstitutionalLedgerEvent,
        ] = {}

        for event in candidates:
            key = (
                event.source_identity,
                event.event_type,
            )
            current = latest.get(key)

            if current is None or _parse_timestamp(
                event.effective_at
            ) > _parse_timestamp(current.effective_at):
                latest[key] = event

        events = tuple(
            sorted(
                latest.values(),
                key=lambda event: (
                    event.source_identity,
                    event.event_type,
                ),
            )
        )

        return TemporalSnapshot(
            as_of=as_of,
            events=events,
        )

    def compare(
        self,
        before_at: str,
        after_at: str,
        *,
        source_identity: str | None = None,
    ) -> TemporalDifference:
        """Compare two effective institutional states."""

        self._queries += 1

        before = self.snapshot(
            before_at,
            source_identity=source_identity,
        )
        after = self.snapshot(
            after_at,
            source_identity=source_identity,
        )

        before_map = {
            (event.source_identity, event.event_type): event for event in before.events
        }
        after_map = {
            (event.source_identity, event.event_type): event for event in after.events
        }

        added = tuple(
            after_map[key] for key in sorted(after_map.keys() - before_map.keys())
        )

        removed = tuple(
            before_map[key] for key in sorted(before_map.keys() - after_map.keys())
        )

        changed = []

        for key in sorted(before_map.keys() & after_map.keys()):
            earlier = before_map[key]
            later = after_map[key]

            if earlier.event_id != later.event_id:
                changed.append(
                    {
                        "source_identity": key[0],
                        "event_type": key[1],
                        "before": earlier.to_dict(),
                        "after": later.to_dict(),
                    }
                )

        return TemporalDifference(
            before=before,
            after=after,
            added=added,
            removed=removed,
            changed=tuple(changed),
        )

    def replay(
        self,
        *,
        correlation_id: str | None = None,
        source_identity: str | None = None,
    ) -> tuple[InstitutionalLedgerEvent, ...]:
        """Replay institutional history in effective temporal order."""

        self._queries += 1
        events = self.store.all()

        if correlation_id is not None:
            events = tuple(
                event for event in events if event.correlation_id == correlation_id
            )

        if source_identity is not None:
            events = tuple(
                event for event in events if event.source_identity == source_identity
            )

        return tuple(
            sorted(
                events,
                key=lambda event: (
                    _parse_timestamp(event.effective_at),
                    _parse_timestamp(event.recorded_at),
                ),
            )
        )

    def lineage(
        self,
        event_id: str,
    ) -> tuple[InstitutionalLedgerEvent, ...]:
        """
        Trace causal ancestry ending at `event_id`.

        The result is returned from earliest known cause to the requested
        terminal event.
        """

        self._queries += 1
        terminal = self.store.get(event_id)

        if terminal is None:
            return ()

        lineage = [terminal]
        visited = {terminal.event_id}
        current = terminal

        while current.causation_id:
            parent = self.store.get(current.causation_id)

            if parent is None or parent.event_id in visited:
                break

            lineage.append(parent)
            visited.add(parent.event_id)
            current = parent

        lineage.reverse()
        return tuple(lineage)

    def provenance(
        self,
        event_id: str,
    ) -> dict[str, Any]:
        """Return inspectable provenance for one institutional event."""

        self._queries += 1
        event = self.store.get(event_id)

        if event is None:
            return {
                "event_id": event_id,
                "found": False,
                "lineage": [],
            }

        lineage = self.lineage(event_id)

        return {
            "event_id": event_id,
            "found": True,
            "source_identity": event.source_identity,
            "event_type": event.event_type,
            "effective_at": event.effective_at,
            "recorded_at": event.recorded_at,
            "correlation_id": event.correlation_id,
            "causation_id": event.causation_id,
            "certified": event.certified,
            "lineage": [item.to_dict() for item in lineage],
        }

    def health(self) -> dict[str, Any]:
        return {
            "name": "Transtemporal Engine™",
            "version": self.VERSION,
            "status": "online",
            "queries": self._queries,
            **self.store.statistics(),
        }
