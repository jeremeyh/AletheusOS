"""
Aletheus Cognitive Engine

StrategicPlanningEngine
"""

from ..engines.base_engine import CognitiveEngine


class StrategicPlanningEngine(CognitiveEngine):
    def __init__(self):

        super().__init__("StrategicPlanningEngine", "Strategy")

    def analyze(self, data=None):

        return self.execute(data)
