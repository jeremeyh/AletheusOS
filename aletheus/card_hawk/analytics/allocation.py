"""
Portfolio Allocation Analytics

Genesis 13.17
"""


class AllocationAnalyticsEngine:
    def analyze(self, assets):

        result = {}

        for asset in assets:
            category = asset.category

            result[category] = result.get(category, 0) + asset.estimated_value

        return result
