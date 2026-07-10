"""
Portfolio Allocation Intelligence

Genesis 13.5
"""


class AllocationEngine:


    def calculate(
        self,
        assets
    ):

        allocation = {}


        for asset in assets:

            category = (
                asset.category
            )


            allocation[category] = (
                allocation.get(
                    category,
                    0
                )
                +
                asset.estimated_value
            )


        return allocation

