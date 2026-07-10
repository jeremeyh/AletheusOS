"""
Card Hawk Analytics Engine

Genesis 13.17
"""


from .performance import PerformanceAnalyticsEngine
from .allocation import AllocationAnalyticsEngine
from .exposure import ExposureAnalyticsEngine



class CardHawkAnalyticsEngine:


    def __init__(self):

        self.performance = (
            PerformanceAnalyticsEngine()
        )

        self.allocation = (
            AllocationAnalyticsEngine()
        )

        self.exposure = (
            ExposureAnalyticsEngine()
        )



    def analyze(
        self,
        assets
    ):

        return {

            "performance":

                self.performance.analyze(
                    assets
                ),


            "allocation":

                self.allocation.analyze(
                    assets
                ),


            "exposure":

                self.exposure.analyze(
                    assets
                )

        }

