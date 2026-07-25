"""
Aletheus Cognitive Engine

OpportunityDetectionEngine
"""


from ..engines.base_engine import CognitiveEngine


class OpportunityDetectionEngine(
    CognitiveEngine
):


    def __init__(self):

        super().__init__(
            "OpportunityDetectionEngine",
            "Strategy"
        )



    def analyze(
        self,
        data=None
    ):

        return self.execute(
            data
        )

