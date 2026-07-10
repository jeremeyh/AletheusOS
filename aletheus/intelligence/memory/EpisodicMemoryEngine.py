"""
Aletheus Cognitive Engine

EpisodicMemoryEngine
"""


from ..engines.base_engine import CognitiveEngine



class EpisodicMemoryEngine(
    CognitiveEngine
):


    def __init__(self):

        super().__init__(
            "EpisodicMemoryEngine",
            "Memory"
        )



    def analyze(
        self,
        data=None
    ):

        return self.execute(
            data
        )

