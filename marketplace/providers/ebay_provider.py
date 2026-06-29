from marketplace.providers.base_provider import MarketplaceProvider


class EbayProvider(MarketplaceProvider):

    def search(self, card):

        #
        # Placeholder
        #

        return [

            {
                "source": "eBay",
                "price": 122,
                "title": f"{card['player']} Comparable"
            },

            {
                "source": "eBay",
                "price": 129,
                "title": f"{card['player']} Comparable"
            }

        ]
