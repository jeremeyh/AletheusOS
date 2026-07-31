"""
Aletheus Cognitive Engine

ReflectionEngine
"""

from ..engines.base_engine import CognitiveEngine


class ReflectionEngine(CognitiveEngine):
    def __init__(self):

        super().__init__("ReflectionEngine", "Evolution")

    def analyze(self, data=None):

        return self.execute(data)
