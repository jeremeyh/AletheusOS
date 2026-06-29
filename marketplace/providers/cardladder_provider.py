from marketplace.providers.base_provider import MarketplaceProvider


class CardLadderProvider(MarketplaceProvider):

    def search(self, card):

        return [

            {
                "source": "Card Ladder",
                "price": 126,
                "title": f"{card['player']} Comparable"
            }

        ]
