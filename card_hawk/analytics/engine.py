"""
Card Hawk Analytics Engine

Genesis 14.19
"""


from .dashboards import DashboardEngine
from .metrics import MetricsEngine
from .reports import ReportingEngine


class AnalyticsEngine:


    def __init__(self):

        self.metrics = MetricsEngine()

        self.dashboard = DashboardEngine()

        self.reports = ReportingEngine()



    def analyze(
        self,
        data
    ):


        return {

            "status":

                "complete"

        }

