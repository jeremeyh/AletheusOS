"""
Founder Console Engine

Genesis 14.8
"""

from .dashboard import DashboardEngine
from .decision_queue import DecisionQueue
from .timeline import IntelligenceTimeline


class FounderConsoleEngine:
    def __init__(self):

        self.dashboard = DashboardEngine()

        self.queue = DecisionQueue()

        self.timeline = IntelligenceTimeline()

    def load(self):

        return {"console": "ready"}
