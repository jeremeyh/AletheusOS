"""
Card Hawk Notification Engine

Genesis 13.19
"""

from .priority import NotificationPriorityEngine
from .routing import NotificationRouter


class CardHawkNotificationEngine:
    def __init__(self):

        self.priority = NotificationPriorityEngine()

        self.router = NotificationRouter()

        self.history = []

    def process(self, event):

        priority = self.priority.classify(event)

        event.priority = priority

        event.channels = self.router.route(priority)

        self.history.append(event)

        return event

    def snapshot(self):

        return {"notifications": len(self.history)}
