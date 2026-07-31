"""
Universal Collectible Intelligence Engine

Genesis 13.22
"""


class CollectibleIntelligenceEngine:
    def evaluate(self, asset):

        return {
            "asset": asset.title,
            "category": asset.category,
            "rarity": asset.rarity_score,
            "classification": self.classify(asset.rarity_score),
        }

    def classify(self, score):

        if score >= 90:
            return "apex"

        if score >= 70:
            return "premium"

        if score >= 50:
            return "core"

        return "speculative"
