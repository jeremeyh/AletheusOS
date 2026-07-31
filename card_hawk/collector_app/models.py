"""
Collector Platform Models

Genesis 14.9
"""

from dataclasses import dataclass, field


@dataclass
class CollectorProfile:
    user_id: str

    preferences: dict = field(default_factory=dict)


@dataclass
class CollectionGoal:
    name: str

    progress: int = 0
