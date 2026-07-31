"""
Aletheus Cognitive Engine

ScenarioSimulationEngine
"""

from ..engines.base_engine import CognitiveEngine


class ScenarioSimulationEngine(CognitiveEngine):
    def __init__(self):

        super().__init__("ScenarioSimulationEngine", "Prediction")

    def analyze(self, data=None):

        return self.execute(data)
