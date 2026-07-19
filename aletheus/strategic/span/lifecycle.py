"""Lifecycle management for SPAN™."""

from __future__ import annotations

from threading import RLock


class SPANLifecycle:
    def __init__(self) -> None:
        self._started = False
        self._lock = RLock()

    @property
    def is_started(self) -> bool:
        with self._lock:
            return self._started

    def start(self) -> None:
        with self._lock:
            self._started = True

    def stop(self) -> None:
        with self._lock:
            self._started = False
