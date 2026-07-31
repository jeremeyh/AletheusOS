"""
Outcome Learning

Genesis 13.48
"""


class OutcomeTracker:
    def __init__(self):

        self.events = []

    def record(self, event):

        self.events.append(event)
