from marketplace.providers.base_provider import MarketplaceProvider


class COMCProvider(MarketplaceProvider):

    def search(self, card):

        return [

            {
                "source": "COMC",
                "price": 121,
                "title": f"{card['player']} Comparable"
            }

        ]
