"""
Aletheus Cognitive Engine

KnowledgeEvolutionEngine
"""


from ..engines.base_engine import CognitiveEngine



class KnowledgeEvolutionEngine(
    CognitiveEngine
):


    def __init__(self):

        super().__init__(
            "KnowledgeEvolutionEngine",
            "Knowledge"
        )



    def analyze(
        self,
        data=None
    ):

        return self.execute(
            data
        )

