"""
Card Hawk Market Intelligence Engine

Genesis 13.9
"""


from .pricing import PricingIntelligenceEngine
from .demand import DemandIntelligenceEngine
from .saturation import MarketSaturationIndex



class CardHawkMarketEngine:


    def __init__(self):

        self.pricing = (
            PricingIntelligenceEngine()
        )

        self.demand = (
            DemandIntelligenceEngine()
        )

        self.saturation = (
            MarketSaturationIndex()
        )



    def analyze(
        self,
        asset_id,
        sales=None,
        supply=0,
        demand=0
    ):

        return {

            "asset_id":
                asset_id,

            "pricing":
                self.pricing.analyze(
                    sales or []
                ),

            "demand":
                self.demand.evaluate(
                    []
                ),

            "saturation":
                self.saturation.calculate(
                    supply,
                    demand
                )

        }

