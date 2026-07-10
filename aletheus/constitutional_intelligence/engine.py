"""
Constitutional Intelligence Engine

Genesis 13.54
"""


from .principles import PrincipleRegistry
from .policies import PolicyEngine
from .audit import GovernanceAudit
from .change_control import ChangeControlEngine



class ConstitutionalIntelligenceEngine:


    def __init__(self):

        self.principles = PrincipleRegistry()

        self.policies = PolicyEngine()

        self.audit = GovernanceAudit()

        self.change_control = ChangeControlEngine()



    def evaluate(
        self,
        action
    ):


        return self.policies.evaluate(
            action
        )

