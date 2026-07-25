"""Minimal telemetry abstraction for SPAN™."""

from __future__ import annotations

from collections import Counter
from collections.abc import Mapping
from threading import RLock


class SPANTelemetry:
    def __init__(self) -> None:
        self._counters: Counter[str] = Counter()
        self._lock = RLock()

    def increment(self, metric: str, value: int = 1) -> None:
        if value < 0:
            raise ValueError("Telemetry increments must be non-negative")
        with self._lock:
            self._counters[metric] += value

    def snapshot(self) -> Mapping[str, int]:
        with self._lock:
            return dict(self._counters)
