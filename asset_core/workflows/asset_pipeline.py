"""
Canonical Asset Pipeline
"""

class AssetPipeline:

    STAGES = [
        "asset.created",
        "hawk_aeye.process",
        "dna.completed",
        "thorx.score",
        "portfolio.update",
        "timeline.update",
        "founder.brief",
        "market.sync",
    ]

    def run(self, asset):

        print()

        print("=" * 60)
        print("CardHawk OS™ Asset Pipeline")
        print("=" * 60)

        for stage in self.STAGES:
            print("->", stage)

        print("=" * 60)
