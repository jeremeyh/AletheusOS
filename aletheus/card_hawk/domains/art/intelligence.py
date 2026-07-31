"""
Artwork Intelligence

Genesis 13.22
"""


class ArtIntelligenceEngine:
    def evaluate(self, item):

        return {
            "artist": item.metadata.get("artist"),
            "medium": item.metadata.get("medium"),
        }
