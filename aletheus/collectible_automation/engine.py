"""
Collectible Automation Engine

Genesis 13.42
"""

from .notifications import NotificationEngine
from .reports import ReportGenerator
from .scheduler import AutomationScheduler
from .workflow import WorkflowRuntime


class CollectibleAutomationEngine:
    def __init__(self):

        self.scheduler = AutomationScheduler()

        self.runtime = WorkflowRuntime()

        self.notifications = NotificationEngine()

        self.reports = ReportGenerator()

    def run(self, workflow):

        return self.runtime.execute(workflow)
