"""
Aletheus Cognitive Engine

AdaptationEngine
"""


from ..engines.base_engine import CognitiveEngine



class AdaptationEngine(
    CognitiveEngine
):


    def __init__(self):

        super().__init__(
            "AdaptationEngine",
            "Learning"
        )



    def analyze(
        self,
        data=None
    ):

        return self.execute(
            data
        )

