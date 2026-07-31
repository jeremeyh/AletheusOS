"""
SPA Evolution History Memory

Genesis 154
"""


class EvolutionHistory:
    def __init__(self):

        self.events = []

    def record(self, event):

        self.events.append(event)

    def list(self):

        return self.events
