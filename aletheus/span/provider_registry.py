from __future__ import annotations

from typing import Dict, Iterable, Optional

from .pipeline import SPANPipeline
from .providers.base import Provider


class ProviderRegistry:
    """Canonical registry for SPAN providers."""

    def __init__(self) -> None:
        self._providers: Dict[str, Provider] = {}
        self._enabled: Dict[str, bool] = {}

    def register(self, provider: Provider, *, name: Optional[str] = None) -> None:
        key = name or provider.__class__.__name__
        if key in self._providers:
            raise ValueError(f"Provider already registered: {key}")
        self._providers[key] = provider
        self._enabled[key] = True

    def unregister(self, name: str) -> None:
        self._providers.pop(name, None)
        self._enabled.pop(name, None)

    def enable(self, name: str) -> None:
        if name not in self._providers:
            raise KeyError(name)
        self._enabled[name] = True

    def disable(self, name: str) -> None:
        if name not in self._providers:
            raise KeyError(name)
        self._enabled[name] = False

    def get(self, name: str) -> Provider:
        return self._providers[name]

    def list(self) -> Iterable[str]:
        return tuple(self._providers.keys())

    def enabled(self) -> Iterable[Provider]:
        return tuple(
            provider
            for name, provider in self._providers.items()
            if self._enabled.get(name, False)
        )

    def build_pipeline(self, analyzers=None) -> SPANPipeline:
        return SPANPipeline(
            providers=list(self.enabled()),
            analyzers=[] if analyzers is None else list(analyzers),
        )
