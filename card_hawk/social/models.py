"""
Social Collector Models

Genesis 14.25
"""

from dataclasses import dataclass, field



@dataclass
class CollectorProfile:


    user_id: str

    interests: list = field(
        default_factory=list
    )

    reputation: int = 0



@dataclass
class Community:


    name: str

    members: list = field(
        default_factory=list
    )

