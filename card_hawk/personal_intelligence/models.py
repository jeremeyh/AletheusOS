"""
Personal Intelligence Models

Genesis 14.24
"""

from dataclasses import dataclass, field



@dataclass
class CollectorProfile:


    user_id: str

    preferences: dict = field(
        default_factory=dict
    )

    goals: list = field(
        default_factory=list
    )

