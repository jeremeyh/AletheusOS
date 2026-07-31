"""
Constitutional Intelligence Engine

Genesis 13.54
"""

from .audit import GovernanceAudit
from .change_control import ChangeControlEngine
from .policies import PolicyEngine
from .principles import PrincipleRegistry


class ConstitutionalIntelligenceEngine:
    def __init__(self):

        self.principles = PrincipleRegistry()

        self.policies = PolicyEngine()

        self.audit = GovernanceAudit()

        self.change_control = ChangeControlEngine()

    def evaluate(self, action):

        return self.policies.evaluate(action)
