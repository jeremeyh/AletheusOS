"""
Card Hawk Executive Dashboard

Version 2.1.0
"""

from cardhawk.dashboard import DashboardService


class ExecutiveDashboard:
    def __init__(self):

        self.dashboard = DashboardService()

    def build(self):

        snapshot = self.dashboard.snapshot()

        return {
            "title": "Card Hawk Executive Dashboard",
            "portfolio": snapshot["portfolio"],
            "analytics": snapshot["analytics"],
            "widgets": [
                "Portfolio Value",
                "Collection Allocation",
                "Player Exposure",
                "Team Exposure",
                "Recent Acquisitions",
                "Highest Value Assets",
                "Newest Assets",
                "Portfolio Performance",
            ],
        }
