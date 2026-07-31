"""
Collector Experience Engine

Genesis 14.9
"""

from .assistant import CollectorAssistant
from .dashboard import DashboardEngine
from .discovery import DiscoveryEngine


class CollectorExperienceEngine:
    def __init__(self):

        self.dashboard = DashboardEngine()

        self.discovery = DiscoveryEngine()

        self.assistant = CollectorAssistant()

    def launch(self):

        return {"application": "ready"}
