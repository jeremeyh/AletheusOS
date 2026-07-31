"""
Aletheus Cognitive Engine

SkillAcquisitionEngine
"""

from ..engines.base_engine import CognitiveEngine


class SkillAcquisitionEngine(CognitiveEngine):
    def __init__(self):

        super().__init__("SkillAcquisitionEngine", "Learning")

    def analyze(self, data=None):

        return self.execute(data)
