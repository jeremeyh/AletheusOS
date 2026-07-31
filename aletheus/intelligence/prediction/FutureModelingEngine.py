"""
Aletheus Cognitive Engine

FutureModelingEngine
"""

from ..engines.base_engine import CognitiveEngine


class FutureModelingEngine(CognitiveEngine):
    def __init__(self):

        super().__init__("FutureModelingEngine", "Prediction")

    def analyze(self, data=None):

        return self.execute(data)
