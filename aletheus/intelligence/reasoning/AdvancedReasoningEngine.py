"""
Aletheus Cognitive Engine

AdvancedReasoningEngine
"""


from ..engines.base_engine import CognitiveEngine



class AdvancedReasoningEngine(
    CognitiveEngine
):


    def __init__(self):

        super().__init__(
            "AdvancedReasoningEngine",
            "Reasoning"
        )



    def analyze(
        self,
        data=None
    ):

        return self.execute(
            data
        )

