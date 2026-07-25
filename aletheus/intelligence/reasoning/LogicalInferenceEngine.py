"""
Aletheus Cognitive Engine

LogicalInferenceEngine
"""


from ..engines.base_engine import CognitiveEngine


class LogicalInferenceEngine(
    CognitiveEngine
):


    def __init__(self):

        super().__init__(
            "LogicalInferenceEngine",
            "Reasoning"
        )



    def analyze(
        self,
        data=None
    ):

        return self.execute(
            data
        )

