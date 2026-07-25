"""
Aletheus Cognitive Engine

PerceptionIntelligenceEngine
"""


from ..engines.base_engine import CognitiveEngine


class PerceptionIntelligenceEngine(
    CognitiveEngine
):


    def __init__(self):

        super().__init__(
            "PerceptionIntelligenceEngine",
            "Perception"
        )



    def analyze(
        self,
        data=None
    ):

        return self.execute(
            data
        )

