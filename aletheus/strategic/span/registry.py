"""Local registry for SPAN™ components and adapters."""

from __future__ import annotations

from collections.abc import Iterable
from threading import RLock
from typing import Any


class SPANRegistry:
    def __init__(self) -> None:
        self._items: dict[str, Any] = {}
        self._lock = RLock()

    def register(self, name: str, component: Any, *, replace: bool = False) -> None:
        normalized = name.strip().lower()
        if not normalized:
            raise ValueError("Registry name must not be empty")

        with self._lock:
            if normalized in self._items and not replace:
                raise KeyError(f"Component already registered: {normalized}")
            self._items[normalized] = component

    def resolve(self, name: str) -> Any:
        normalized = name.strip().lower()
        with self._lock:
            try:
                return self._items[normalized]
            except KeyError as exc:
                raise KeyError(f"Unknown SPAN component: {normalized}") from exc

    def names(self) -> Iterable[str]:
        with self._lock:
            return tuple(sorted(self._items))
