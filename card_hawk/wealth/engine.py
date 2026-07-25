"""
Card Hawk Wealth Engine

Genesis 14.27
"""


from .portfolio import PortfolioEngine
from .risk import RiskEngine


class WealthEngine:


    def __init__(self):

        self.portfolio = PortfolioEngine()

        self.risk = RiskEngine()



    def analyze(
        self,
        data
    ):


        return {

            "status":

                "complete"

        }

