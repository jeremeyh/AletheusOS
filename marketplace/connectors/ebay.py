class EbayConnector:
    """
    Placeholder eBay Sold Listings connector.
    """

    @staticmethod
    def search(card):

        player = card.get("player", "")

        if player == "Caleb Williams":

            return [
                {
                    "marketplace": "eBay",
                    "price": 120.00,
                    "shipping": 5.95,
                    "condition": "Raw",
                    "sold_date": "2026-06-25",
                },
                {
                    "marketplace": "eBay",
                    "price": 128.00,
                    "shipping": 4.99,
                    "condition": "Raw",
                    "sold_date": "2026-06-23",
                },
                {
                    "marketplace": "eBay",
                    "price": 127.00,
                    "shipping": 6.00,
                    "condition": "Raw",
                    "sold_date": "2026-06-20",
                },
            ]

        return []
