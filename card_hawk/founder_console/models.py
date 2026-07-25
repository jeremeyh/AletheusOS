"""
Founder Console Models

Genesis 14.8
"""

from dataclasses import dataclass, field


@dataclass
class ConsoleWidget:


    name: str

    data: dict = field(
        default_factory=dict
    )



@dataclass
class DecisionItem:


    action: str

    recommendation: str

    confidence: int

