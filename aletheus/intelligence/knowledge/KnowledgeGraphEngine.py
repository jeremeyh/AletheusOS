"""
Aletheus Cognitive Engine

KnowledgeGraphEngine
"""


from ..engines.base_engine import CognitiveEngine


class KnowledgeGraphEngine(
    CognitiveEngine
):


    def __init__(self):

        super().__init__(
            "KnowledgeGraphEngine",
            "Knowledge"
        )



    def analyze(
        self,
        data=None
    ):

        return self.execute(
            data
        )

