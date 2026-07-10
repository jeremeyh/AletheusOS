"""
Agent Council Runtime

Genesis 13.29
"""


from .registry import CouncilRegistry
from .deliberation import DeliberationEngine
from .consensus import ConsensusEngine
from .governance import CouncilGovernance



class AgentCouncil:


    def __init__(self):

        self.registry = CouncilRegistry()

        self.deliberation = DeliberationEngine()

        self.consensus = ConsensusEngine()

        self.governance = CouncilGovernance()



    def evaluate(
        self,
        opinions
    ):


        self.deliberation.review(
            opinions
        )


        decision = self.consensus.decide(
            opinions
        )


        return self.governance.authorize(
            decision
        )

