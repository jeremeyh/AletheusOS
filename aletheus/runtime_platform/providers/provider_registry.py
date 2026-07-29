from __future__ import annotations

from .contracts import RuntimeProvider


class ProviderRegistry:

    def __init__(self) -> None:
        self._providers: dict[str, RuntimeProvider] = {}

    def register(
        self,
        provider: RuntimeProvider,
        *,
        replace: bool=False,
    ) -> RuntimeProvider:

        if provider.name in self._providers and not replace:
            raise ValueError(
                f"Provider already registered: {provider.name}"
            )

        self._providers[provider.name] = provider
        return provider

    def resolve(
        self,
        name: str,
    ) -> RuntimeProvider | None:

        return self._providers.get(name)

    def providers(self):

        return tuple(
            sorted(self._providers.values(),
                   key=lambda p: p.name)
        )

    def snapshot(self):

        return {
            provider.name: provider.snapshot()
            for provider in self.providers()
        }
