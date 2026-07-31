"""
SPA Autonomous Architecture Council

Genesis 155
"""

from .constitution_validator import ConstitutionValidator
from .decision_engine import DecisionEngine
from .proposal_engine import ProposalEngine
from .review_engine import ReviewEngine
from .risk_engine import RiskEngine


class ArchitectureCouncil:
    def __init__(self):

        self.proposals = ProposalEngine()

        self.review = ReviewEngine()

        self.risk = RiskEngine()

        self.constitution = ConstitutionValidator()

        self.decision = DecisionEngine()

    def initialize(self):

        return {
            "system": "spa_architecture_council",
            "genesis": "155",
            "status": "operational",
        }

    def evaluate(self, proposal):

        review = self.review.review(proposal)

        risk = self.risk.evaluate(proposal)

        constitution = self.constitution.validate(proposal)

        decision = self.decision.decide(review, risk, constitution)

        return {
            "proposal": proposal,
            "review": review,
            "risk": risk,
            "constitution": constitution,
            "decision": decision,
        }
