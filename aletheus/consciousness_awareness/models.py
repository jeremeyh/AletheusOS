"""
Awareness Models

Genesis 13.53
"""

from dataclasses import dataclass, field


@dataclass
class AwarenessState:
    system_status: str

    mission: str

    alignment_score: int

    observations: list = field(default_factory=list)
