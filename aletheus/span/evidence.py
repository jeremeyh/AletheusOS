"""Evidence collection and indexing for SPAN™."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable, Iterator
from threading import RLock
from typing import Any

from .models import Evidence, SourceLocation


class EvidenceStore:
    """Thread-safe in-memory store for architectural evidence."""

    def __init__(self) -> None:
        self._items: dict[str, Evidence] = {}
        self._by_kind: dict[str, set[str]] = defaultdict(set)
        self._by_source: dict[str, set[str]] = defaultdict(set)
        self._lock = RLock()

    def add(self, evidence: Evidence) -> Evidence:
        with self._lock:
            self._items[evidence.id] = evidence
            self._by_kind[evidence.kind].add(evidence.id)
            self._by_source[evidence.source].add(evidence.id)
        return evidence

    def extend(self, evidence: Iterable[Evidence]) -> None:
        for item in evidence:
            self.add(item)

    def create(
        self,
        *,
        kind: str,
        source: str,
        target: str | None = None,
        confidence: float = 1.0,
        location: SourceLocation | None = None,
        attributes: dict[str, Any] | None = None,
    ) -> Evidence:
        return self.add(
            Evidence(
                kind=kind,
                source=source,
                target=target,
                confidence=confidence,
                location=location,
                attributes=attributes or {},
            )
        )

    def get(self, evidence_id: str) -> Evidence | None:
        return self._items.get(evidence_id)

    def by_kind(self, kind: str) -> tuple[Evidence, ...]:
        return tuple(self._items[item_id] for item_id in sorted(self._by_kind.get(kind, ())))

    def by_source(self, source: str) -> tuple[Evidence, ...]:
        return tuple(self._items[item_id] for item_id in sorted(self._by_source.get(source, ())))

    def query(
        self,
        *,
        kind: str | None = None,
        source: str | None = None,
        target: str | None = None,
    ) -> tuple[Evidence, ...]:
        items: Iterable[Evidence] = self._items.values()
        if kind is not None:
            items = (item for item in items if item.kind == kind)
        if source is not None:
            items = (item for item in items if item.source == source)
        if target is not None:
            items = (item for item in items if item.target == target)
        return tuple(items)

    def clear(self) -> None:
        with self._lock:
            self._items.clear()
            self._by_kind.clear()
            self._by_source.clear()

    def to_list(self) -> list[dict[str, Any]]:
        return [item.to_dict() for item in self]

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self) -> Iterator[Evidence]:
        return iter(tuple(self._items.values()))
