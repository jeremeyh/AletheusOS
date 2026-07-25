from marketplace.providers.cardladder_provider import CardLadderProvider
from marketplace.providers.comc_provider import COMCProvider
from marketplace.providers.ebay_provider import EbayProvider


class MarketplaceManager:
    """
    Marketplace Intelligence Hub™

    Aggregates marketplace providers and returns
    normalized comparable sales.
    """

    PROVIDERS = [
        EbayProvider(),
        COMCProvider(),
        CardLadderProvider(),
    ]

    @classmethod
    def get_comps(cls, card):

        comps = []

        for provider in cls.PROVIDERS:

            try:

                provider_results = provider.search(card)

                if provider_results:
                    comps.extend(provider_results)

            except Exception as exc:

                print(
                    f"[Marketplace] {provider.__class__.__name__} failed: {exc}"
                )

        return comps
