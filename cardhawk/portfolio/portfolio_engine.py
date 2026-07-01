"""
Card Hawk Portfolio Engine

Version 1.4.0
"""

from __future__ import annotations

from collections import defaultdict


class PortfolioEngine:

    def __init__(self, assets):

        self.assets = list(assets)

    def total_purchase_price(self):

        return sum(
            asset.purchase_price
            for asset in self.assets
        )

    def total_market_value(self):

        return sum(
            asset.estimated_value
            for asset in self.assets
        )

    def unrealized_gain(self):

        return (
            self.total_market_value()
            - self.total_purchase_price()
        )

    def allocation_by_sport(self):

        allocation = defaultdict(float)

        for asset in self.assets:

            allocation[asset.sport] += asset.estimated_value

        return dict(allocation)

    def allocation_by_team(self):

        allocation = defaultdict(float)

        for asset in self.assets:

            allocation[asset.team] += asset.estimated_value

        return dict(allocation)

    def summary(self):

        return {

            "asset_count": len(self.assets),

            "purchase_total":
                self.total_purchase_price(),

            "market_total":
                self.total_market_value(),

            "unrealized_gain":
                self.unrealized_gain(),

        }
