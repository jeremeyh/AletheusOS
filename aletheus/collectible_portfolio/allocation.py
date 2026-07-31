"""
Allocation Intelligence

Genesis 13.33
"""


class AllocationEngine:
    def analyze(self, assets):

        allocation = {}

        for asset in assets:
            category = asset.get("category", "unknown")

            allocation[category] = allocation.get(category, 0) + 1

        return allocation
