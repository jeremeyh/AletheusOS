"""
THORᵡ Decision Models

Genesis 13.7
"""

from dataclasses import dataclass, field



@dataclass
class THORDecision:


    asset_id: str

    quality_score: int = 0

    scarcity_score: int = 0

    demand_score: int = 0

    growth_score: int = 0

    risk_score: int = 0

    confidence: int = 0

    recommendation: str = "UNASSESSED"

    upside_classification: str = "UNKNOWN"

    reasoning: dict = field(
        default_factory=dict
    )

