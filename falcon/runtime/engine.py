from falcon.runtime.dna import FalconDNA
from falcon.runtime.forecasting import FalconForecasting
from falcon.runtime.health import FalconHealth
from falcon.runtime.opportunity_queue import FalconOpportunityQueue
from falcon.runtime.snapshots import FalconSnapshots


class FalconEngine:
    """
    FALCON™

    Forecasting, Analytics, Learning & Collection Optimization Network.
    """

    @staticmethod
    def snapshot():
        return {
            "health": FalconHealth.analyze(),
            "opportunity_queue": FalconOpportunityQueue.build(),
            "forecast": FalconForecasting.forecast_portfolio(),
            "dna": FalconDNA.analyze(),
            "history": FalconSnapshots.history(),
        }

    @staticmethod
    def record_snapshot():
        return FalconSnapshots.create()
