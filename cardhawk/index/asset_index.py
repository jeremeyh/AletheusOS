"""
Asset Index Engine

Version 1.3.0
"""

from collections import defaultdict


class AssetIndex:

    def __init__(self):

        self.clear()

    def clear(self):

        self.players = defaultdict(list)
        self.teams = defaultdict(list)
        self.sports = defaultdict(list)
        self.years = defaultdict(list)
        self.sets = defaultdict(list)
        self.categories = defaultdict(list)

    def build(self, assets):

        self.clear()

        for asset in assets:

            if asset.player:
                self.players[asset.player].append(asset)

            if asset.team:
                self.teams[asset.team].append(asset)

            if asset.sport:
                self.sports[asset.sport].append(asset)

            if asset.year:
                self.years[str(asset.year)].append(asset)

            if asset.set_name:
                self.sets[asset.set_name].append(asset)

            if asset.category:
                self.categories[asset.category].append(asset)

    def statistics(self):

        return {

            "players": len(self.players),
            "teams": len(self.teams),
            "sports": len(self.sports),
            "years": len(self.years),
            "sets": len(self.sets),
            "categories": len(self.categories),

        }
