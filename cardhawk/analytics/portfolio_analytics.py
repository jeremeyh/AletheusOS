"""
Portfolio Analytics

Version 1.5.0
"""

from collections import Counter


class PortfolioAnalytics:

    def __init__(self, assets):

        self.assets = list(assets)

    def asset_count(self):

        return len(self.assets)

    def category_breakdown(self):

        return dict(
            Counter(
                asset.category
                for asset in self.assets
            )
        )

    def player_breakdown(self):

        return dict(
            Counter(
                asset.player
                for asset in self.assets
                if asset.player
            )
        )

    def team_breakdown(self):

        return dict(
            Counter(
                asset.team
                for asset in self.assets
                if asset.team
            )
        )

    def sport_breakdown(self):

        return dict(
            Counter(
                asset.sport
                for asset in self.assets
                if asset.sport
            )
        )

    def grade_breakdown(self):

        return dict(
            Counter(
                asset.grade
                for asset in self.assets
                if asset.grade
            )
        )

    def summary(self):

        return {

            "assets": self.asset_count(),

            "players":
                len(self.player_breakdown()),

            "teams":
                len(self.team_breakdown()),

            "sports":
                len(self.sport_breakdown()),

            "categories":
                len(self.category_breakdown()),

        }
