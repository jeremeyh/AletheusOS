class GenomeEngine:
    """
    CardHawk Genome™

    Learns portfolio tendencies and
    collectible characteristics over time.
    """

    @staticmethod
    def learn(asset):

        return {
            "player": asset.get("player"),
            "brand": asset.get("brand"),
            "parallel": asset.get("parallel"),
            "score": asset.get("thorx_score"),
            "market_value": asset.get("market_value"),
            "status": "Learned",
        }

    @staticmethod
    def recommend(asset):

        score = asset.get(
            "thorx_score",
            0,
        )

        if score >= 95:
            return "GRAIL"

        if score >= 90:
            return "ELITE"

        if score >= 80:
            return "BUY"

        if score >= 70:
            return "WATCH"

        return "PASS"
