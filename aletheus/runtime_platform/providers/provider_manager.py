from __future__ import annotations

from typing import Any

from .provider_registry import ProviderRegistry


class ProviderManager:

    def __init__(
        self,
        registry: ProviderRegistry,
    ) -> None:

        self.registry = registry

    def initialize(
        self,
        runtime: Any,
    ):

        for provider in self.registry.providers():
            provider.initialize(runtime)

    def activate(self):

        for provider in self.registry.providers():
            provider.activate()

    def shutdown(self):

        for provider in reversed(
            self.registry.providers()
        ):
            provider.shutdown()

    def snapshot(self):

        return self.registry.snapshot()

    def health(self):

        return {
            provider.name: provider.health()
            for provider in self.registry.providers()
        }
