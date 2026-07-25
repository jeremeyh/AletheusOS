"""
Card Hawk Portfolio Intelligence Engine

Genesis 13.5
"""


from .allocation import AllocationEngine
from .risk import PortfolioRiskEngine
from .valuation import PortfolioValuationEngine


class CardHawkPortfolioEngine:


    def __init__(self):

        self.valuation = (
            PortfolioValuationEngine()
        )

        self.allocation = (
            AllocationEngine()
        )

        self.risk = (
            PortfolioRiskEngine()
        )



    def analyze(
        self,
        assets
    ):

        return {

            "valuation":
                self.valuation.calculate(
                    assets
                ),

            "allocation":
                self.allocation.calculate(
                    assets
                ),

            "risk":
                self.risk.analyze(
                    assets
                )

        }

