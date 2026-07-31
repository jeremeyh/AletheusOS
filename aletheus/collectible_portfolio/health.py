"""
Collection Health Engine

Genesis 13.33
"""


class CollectionHealthEngine:
    def calculate(self, metrics):

        scores = [
            metrics.get("scarcity", 0),
            metrics.get("liquidity", 0),
            metrics.get("growth", 0),
        ]

        return int(sum(scores) / len(scores))
