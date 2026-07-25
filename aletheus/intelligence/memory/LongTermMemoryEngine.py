"""
Aletheus Cognitive Engine

LongTermMemoryEngine
"""


from ..engines.base_engine import CognitiveEngine


class LongTermMemoryEngine(
    CognitiveEngine
):


    def __init__(self):

        super().__init__(
            "LongTermMemoryEngine",
            "Memory"
        )



    def analyze(
        self,
        data=None
    ):

        return self.execute(
            data
        )

