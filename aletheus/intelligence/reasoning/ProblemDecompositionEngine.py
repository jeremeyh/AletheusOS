"""
Aletheus Cognitive Engine

ProblemDecompositionEngine
"""


from ..engines.base_engine import CognitiveEngine



class ProblemDecompositionEngine(
    CognitiveEngine
):


    def __init__(self):

        super().__init__(
            "ProblemDecompositionEngine",
            "Reasoning"
        )



    def analyze(
        self,
        data=None
    ):

        return self.execute(
            data
        )

