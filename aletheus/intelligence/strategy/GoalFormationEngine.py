"""
Aletheus Cognitive Engine

GoalFormationEngine
"""

from ..engines.base_engine import CognitiveEngine


class GoalFormationEngine(CognitiveEngine):
    def __init__(self):

        super().__init__("GoalFormationEngine", "Strategy")

    def analyze(self, data=None):

        return self.execute(data)
