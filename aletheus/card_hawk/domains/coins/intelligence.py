"""
Coin Intelligence

Genesis 13.22
"""


class CoinIntelligenceEngine:
    def evaluate(self, coin):

        return {"grade": coin.metadata.get("grade"), "mint": coin.metadata.get("mint")}
