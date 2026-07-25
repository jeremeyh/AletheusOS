"""
Aletheus Cognitive Engine

MetaReasoningEngine
"""


from ..engines.base_engine import CognitiveEngine


class MetaReasoningEngine(
    CognitiveEngine
):


    def __init__(self):

        super().__init__(
            "MetaReasoningEngine",
            "Evolution"
        )



    def analyze(
        self,
        data=None
    ):

        return self.execute(
            data
        )

