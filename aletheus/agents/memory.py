"""
Agent Memory Layer

Genesis 13.27
"""


class AgentMemory:
    def __init__(self):

        self.history = []

    def store(self, event):

        self.history.append(event)

    def recall(self):

        return self.history
