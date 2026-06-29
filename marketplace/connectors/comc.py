class COMCConnector:

    @staticmethod
    def search(card):

        if card.get("player") == "Caleb Williams":

            return [
                {
                    "marketplace": "COMC",
                    "price": 124.00,
                    "shipping": 0,
                    "condition": "Raw",
                    "sold_date": "2026-06-22",
                },
                {
                    "marketplace": "COMC",
                    "price": 130.00,
                    "shipping": 0,
                    "condition": "Raw",
                    "sold_date": "2026-06-21",
                },
            ]

        return []
