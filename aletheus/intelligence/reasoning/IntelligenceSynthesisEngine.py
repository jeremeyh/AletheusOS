"""
Aletheus Cognitive Engine

IntelligenceSynthesisEngine
"""

from ..engines.base_engine import CognitiveEngine


class IntelligenceSynthesisEngine(CognitiveEngine):
    def __init__(self):

        super().__init__("IntelligenceSynthesisEngine", "Reasoning")

    def analyze(self, data=None):

        return self.execute(data)
