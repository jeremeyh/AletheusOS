"""
Aletheus Cognitive Engine

PredictiveIntelligenceEngine
"""


from ..engines.base_engine import CognitiveEngine


class PredictiveIntelligenceEngine(
    CognitiveEngine
):


    def __init__(self):

        super().__init__(
            "PredictiveIntelligenceEngine",
            "Prediction"
        )



    def analyze(
        self,
        data=None
    ):

        return self.execute(
            data
        )

