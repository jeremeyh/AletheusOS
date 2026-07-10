"""
Card Hawk Performance Analytics

Genesis 13.17
"""


class PerformanceAnalyticsEngine:


    def analyze(
        self,
        assets
    ):

        cost = sum(
            a.purchase_price
            for a in assets
        )


        value = sum(
            a.estimated_value
            for a in assets
        )


        return {

            "cost_basis":
                cost,

            "current_value":
                value,

            "gain":
                value - cost,

            "roi":

                (
                    ((value-cost)/cost)*100
                    if cost
                    else 0
                )

        }

