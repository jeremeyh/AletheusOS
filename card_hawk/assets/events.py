"""
Asset Events

Genesis 14.1
"""


class AssetEventLog:
    def __init__(self):

        self.events = []

    def record(self, event):

        self.events.append(event)
