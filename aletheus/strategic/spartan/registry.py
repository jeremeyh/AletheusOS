"""Domain registry for SPARTAN™."""

from __future__ import annotations

from collections.abc import Iterable
from threading import RLock

from .domain import IntelligenceDomain


class DomainRegistry:
    def __init__(self) -> None:
        self._domains: dict[str, IntelligenceDomain] = {}
        self._lock = RLock()

    def register(
        self,
        domain: IntelligenceDomain,
        *,
        replace: bool = False,
    ) -> None:
        name = domain.name.strip().lower()
        if not name:
            raise ValueError("Domain name must not be empty")

        with self._lock:
            if name in self._domains and not replace:
                raise KeyError(f"SPARTAN domain already registered: {name}")
            self._domains[name] = domain

    def resolve(self, name: str) -> IntelligenceDomain:
        normalized = name.strip().lower()
        with self._lock:
            try:
                return self._domains[normalized]
            except KeyError as exc:
                raise KeyError(f"Unknown SPARTAN domain: {normalized}") from exc

    def list(self) -> Iterable[IntelligenceDomain]:
        with self._lock:
            return tuple(self._domains[name] for name in sorted(self._domains))

    def names(self) -> Iterable[str]:
        with self._lock:
            return tuple(sorted(self._domains))
