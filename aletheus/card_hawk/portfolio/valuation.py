"""
Portfolio Valuation Engine

Genesis 13.5
"""


class PortfolioValuationEngine:


    def calculate(
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


        gain = value - cost


        roi = (
            (gain / cost) * 100
            if cost
            else 0
        )


        return {

            "cost_basis":
                cost,

            "estimated_value":
                value,

            "unrealized_gain":
                gain,

            "roi_percent":
                roi

        }

