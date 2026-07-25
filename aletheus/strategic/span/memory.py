"""Strategic memory for SPAN™ recommendation lineage."""

from __future__ import annotations

from collections.abc import Iterable
from threading import RLock
from uuid import UUID

from .models import Recommendation


class InMemoryStrategicMemory:
    """Thread-safe reference memory for development and tests.

    Replace with Mammoth™ persistence through an adapter in a later drop.
    """

    def __init__(self) -> None:
        self._items: dict[UUID, Recommendation] = {}
        self._lock = RLock()

    def record(self, recommendation: Recommendation) -> None:
        with self._lock:
            self._items[recommendation.recommendation_id] = recommendation

    def get(self, recommendation_id: UUID) -> Recommendation | None:
        with self._lock:
            return self._items.get(recommendation_id)

    def list(self) -> Iterable[Recommendation]:
        with self._lock:
            return tuple(self._items.values())
