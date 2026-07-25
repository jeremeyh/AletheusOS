"""
Learning Optimization Models

Genesis 13.48
"""

from dataclasses import dataclass


@dataclass
class LearningEvent:

    event_type: str

    input_data: dict

    outcome: dict

    confidence: int = 0



@dataclass
class ImprovementProposal:

    target: str

    recommendation: str

    confidence: int

    status: str = "pending"

