from __future__ import annotations

from collections.abc import Callable
from typing import Any


class DependencyContainer:
    def __init__(self) -> None:
        self._providers: dict[str, Callable[[DependencyContainer], Any]] = {}
        self._singletons: dict[str, Any] = {}
        self._resolving: list[str] = []

    def register(
        self,
        name: str,
        provider: Callable[[DependencyContainer], Any],
        *,
        singleton: bool = True,
    ) -> None:
        if name in self._providers:
            raise KeyError(f"Dependency already registered: {name}")
        self._providers[name] = provider
        if not singleton:
            self._singletons.pop(name, None)

    def resolve(self, name: str) -> Any:
        if name in self._singletons:
            return self._singletons[name]
        if name in self._resolving:
            cycle = " -> ".join([*self._resolving, name])
            raise RuntimeError(f"Dependency cycle detected: {cycle}")
        provider = self._providers.get(name)
        if provider is None:
            raise KeyError(f"Dependency not registered: {name}")
        self._resolving.append(name)
        try:
            value = provider(self)
        finally:
            self._resolving.pop()
        self._singletons[name] = value
        return value
