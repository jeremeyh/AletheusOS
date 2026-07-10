"""
Aletheus Cognitive Engine

ShortTermMemoryEngine
"""


from ..engines.base_engine import CognitiveEngine



class ShortTermMemoryEngine(
    CognitiveEngine
):


    def __init__(self):

        super().__init__(
            "ShortTermMemoryEngine",
            "Memory"
        )



    def analyze(
        self,
        data=None
    ):

        return self.execute(
            data
        )

