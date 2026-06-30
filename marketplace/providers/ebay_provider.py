from marketplace.providers.base_provider import MarketplaceProvider


class EbayProvider(MarketplaceProvider):

    @property
    def name(self):
        return "eBay"

    def search(self, query):
        return []

    def get_comps(self, card):
        return []

    def get_listings(self, card):
        return []

    def get_sales(self, card):
        return []

    def health_check(self):
        return {
            "status": "ONLINE"
        }
