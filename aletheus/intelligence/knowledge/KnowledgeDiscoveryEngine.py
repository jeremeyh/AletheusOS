"""
Aletheus Cognitive Engine

KnowledgeDiscoveryEngine
"""


from ..engines.base_engine import CognitiveEngine



class KnowledgeDiscoveryEngine(
    CognitiveEngine
):


    def __init__(self):

        super().__init__(
            "KnowledgeDiscoveryEngine",
            "Knowledge"
        )



    def analyze(
        self,
        data=None
    ):

        return self.execute(
            data
        )

