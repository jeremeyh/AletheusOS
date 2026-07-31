"""
Provenance Engine

Genesis 13.35
"""


class ProvenanceEngine:
    def __init__(self):

        self.history = []

    def add_event(self, asset, event):

        self.history.append({"asset": asset, "event": event})

        return self.history
