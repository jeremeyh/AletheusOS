"""
Aletheus Cognitive Engine

KnowledgeLineageEngine
"""


from ..engines.base_engine import CognitiveEngine


class KnowledgeLineageEngine(
    CognitiveEngine
):


    def __init__(self):

        super().__init__(
            "KnowledgeLineageEngine",
            "Knowledge"
        )



    def analyze(
        self,
        data=None
    ):

        return self.execute(
            data
        )

