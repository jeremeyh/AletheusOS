"""
Aletheus Cognitive Engine

DecisionIntelligenceEngine
"""


from ..engines.base_engine import CognitiveEngine



class DecisionIntelligenceEngine(
    CognitiveEngine
):


    def __init__(self):

        super().__init__(
            "DecisionIntelligenceEngine",
            "Strategy"
        )



    def analyze(
        self,
        data=None
    ):

        return self.execute(
            data
        )

