"""
Aletheus Cognitive Engine

SemanticMemoryEngine
"""

from ..engines.base_engine import CognitiveEngine


class SemanticMemoryEngine(CognitiveEngine):
    def __init__(self):

        super().__init__("SemanticMemoryEngine", "Memory")

    def analyze(self, data=None):

        return self.execute(data)
