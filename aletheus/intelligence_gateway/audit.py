"""
API Audit Layer

Genesis 13.43
"""


class AuditEngine:


    def __init__(self):

        self.events = []



    def record(
        self,
        event
    ):

        self.events.append(
            event
        )

