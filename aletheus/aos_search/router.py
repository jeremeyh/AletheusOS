from __future__ import annotations

from collections.abc import Callable


class SearchRouter:

    GENESIS = "21.8"
    VERSION = "1.0.0"

    def __init__(self):
        self._providers: dict[str, Callable] = {}

    def register(
        self,
        name: str,
        provider: Callable,
    ):

        self._providers[name] = provider

    def has(
        self,
        name: str,
    ) -> bool:

        return name in self._providers

    def execute(
        self,
        execution_plan,
        query: str,
    ):

        results = {}

        for provider in execution_plan.providers:

            if provider not in self._providers:
                continue

            results[
                provider
            ] = self._providers[
                provider
            ](query)

        return results

    def providers(self):

        return sorted(
            self._providers.keys()
        )

    def statistics(self):

        return {
            "providers": len(
                self._providers
            ),
            "genesis": self.GENESIS,
            "version": self.VERSION,
        }


search_router = SearchRouter()
