"""
Usage Metering Engine

Genesis 13.45
"""


class UsageMeter:
    def __init__(self):

        self.events = []

    def record(self, event):

        self.events.append(event)
