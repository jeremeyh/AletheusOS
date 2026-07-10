"""
Aletheus Cognitive Engine

HypothesisEngine
"""


from ..engines.base_engine import CognitiveEngine



class HypothesisEngine(
    CognitiveEngine
):


    def __init__(self):

        super().__init__(
            "HypothesisEngine",
            "Reasoning"
        )



    def analyze(
        self,
        data=None
    ):

        return self.execute(
            data
        )

