"""
Opportunity Intelligence Models

Genesis 13.26
"""

from dataclasses import dataclass, field



@dataclass
class OpportunityAssessment:


    opportunity_id: str

    asset_name: str

    score: int = 0

    decision: str = "UNASSESSED"

    confidence: int = 0

    reasoning: list = field(
        default_factory=list
    )

    signals: dict = field(
        default_factory=dict
    )

