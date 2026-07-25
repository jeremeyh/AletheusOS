"""
Agent Council Models

Genesis 13.29
"""

from dataclasses import dataclass, field


@dataclass
class AgentOpinion:


    agent: str

    recommendation: str

    confidence: int

    reasoning: list = field(
        default_factory=list
    )



@dataclass
class CouncilDecision:


    decision: str

    confidence: int

    opinions: list = field(
        default_factory=list
    )

