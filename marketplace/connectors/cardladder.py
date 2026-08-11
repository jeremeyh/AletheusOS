class CardLadderConnector:
    @staticmethod
    def search(card):

        if card.get("player") == "Caleb Williams":
            return [
                {
                    "marketplace": "Card Ladder",
                    "price": 126.00,
                    "shipping": 0,
                    "condition": "Raw",
                    "sold_date": "2026-06-19",
                },
                {
                    "marketplace": "Card Ladder",
                    "price": 129.00,
                    "shipping": 0,
                    "condition": "Raw",
                    "sold_date": "2026-06-18",
                },
            ]

        return []
