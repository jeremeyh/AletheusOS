"""
Aletheus Cognitive Engine

SignalDetectionEngine
"""


from ..engines.base_engine import CognitiveEngine



class SignalDetectionEngine(
    CognitiveEngine
):


    def __init__(self):

        super().__init__(
            "SignalDetectionEngine",
            "Perception"
        )



    def analyze(
        self,
        data=None
    ):

        return self.execute(
            data
        )

