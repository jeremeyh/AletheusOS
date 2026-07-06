from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class SearchProvider:

    provider_id: str
    display_name: str

    category: str = "foundation"

    description: str = ""

    enabled: bool = True

    metadata: dict = field(default_factory=dict)

    def to_dict(self):

        return {
            "provider_id": self.provider_id,
            "display_name": self.display_name,
            "category": self.category,
            "description": self.description,
            "enabled": self.enabled,
            "metadata": self.metadata,
        }


class ProviderRegistry:

    GENESIS = "21.8"
    VERSION = "1.0.0"

    def __init__(self):

        self._providers = {}

        self._bootstrap()

    def _bootstrap(self):

        foundation = [

            ("memory", "Memory"),

            ("knowledge", "Knowledge"),

            ("marketplace", "Marketplace"),

            ("internet", "Internet"),

            ("enterprise", "Enterprise"),

            ("visual", "Visual Intelligence"),

            ("forecast", "Forecast"),

            ("consensus", "Consensus"),

        ]

        for provider_id, name in foundation:

            self.register(

                SearchProvider(

                    provider_id=provider_id,

                    display_name=name,

                )

            )

    def register(

        self,

        provider: SearchProvider,

    ):

        self._providers[
            provider.provider_id
        ] = provider

    def get(

        self,

        provider_id: str,

    ):

        return self._providers.get(
            provider_id
        )

    def providers(self):

        return list(
            self._providers.values()
        )

    def enabled(self):

        return [

            provider

            for provider in self.providers()

            if provider.enabled

        ]

    def statistics(self):

        return {

            "providers": len(
                self._providers
            ),

            "enabled": len(
                self.enabled()
            ),

            "genesis": self.GENESIS,

            "version": self.VERSION,

        }


provider_registry = ProviderRegistry()
