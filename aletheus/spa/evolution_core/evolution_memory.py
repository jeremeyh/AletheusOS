"""
SPA Evolution Memory

Genesis 160
"""


class EvolutionMemory:
    def __init__(self):

        self.records = []

    def remember(self, decision):

        self.records.append(decision)

    def history(self):

        return self.records
