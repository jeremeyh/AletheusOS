"""
Aletheus Cognitive Engine

ContinuousLearningEngine
"""


from ..engines.base_engine import CognitiveEngine


class ContinuousLearningEngine(
    CognitiveEngine
):


    def __init__(self):

        super().__init__(
            "ContinuousLearningEngine",
            "Learning"
        )



    def analyze(
        self,
        data=None
    ):

        return self.execute(
            data
        )

