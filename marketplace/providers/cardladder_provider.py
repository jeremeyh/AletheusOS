from marketplace.providers.base_provider import MarketplaceProvider


class CardLadderProvider(MarketplaceProvider):

    @property
    def name(self):
        return "Card Ladder"

    def search(self, query):
        return [
            {
                "source": "Card Ladder",
                "price": 126,
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
        return {
            "status": "ONLINE"
        }
