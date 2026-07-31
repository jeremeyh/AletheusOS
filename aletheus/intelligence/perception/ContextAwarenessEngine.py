"""
Aletheus Cognitive Engine

ContextAwarenessEngine
"""

from ..engines.base_engine import CognitiveEngine


class ContextAwarenessEngine(CognitiveEngine):
    def __init__(self):

        super().__init__("ContextAwarenessEngine", "Perception")

    def analyze(self, data=None):

        return self.execute(data)
