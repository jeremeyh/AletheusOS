"""
Market Memory Store

Genesis 13.47
"""


class MarketMemory:


    def __init__(self):

        self.events = []



    def record(
        self,
        event
    ):

        self.events.append(
            event
        )

