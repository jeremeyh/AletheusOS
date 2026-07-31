"""
Card Hawk Alert Engine

Genesis 13.10
"""


class AlertEngine:
    def __init__(self):

        self.alerts = []

    def create(self, event):

        self.alerts.append(event)

        return event

    def list(self):

        return self.alerts
