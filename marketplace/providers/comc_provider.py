from marketplace.providers.base_provider import MarketplaceProvider


class COMCProvider(MarketplaceProvider):
    @property
    def name(self):
        return "COMC"

    def search(self, query):
        return [
            {
                "source": "COMC",
                "price": 121,
                "title": "Caleb Williams Comparable",
            }
        ]

    def get_comps(self, card):
        return self.search(card)

    def get_listings(self, card):
        return []

    def get_sales(self, card):
        return self.search(card)

    def health_check(self):
        return {"status": "ONLINE"}
