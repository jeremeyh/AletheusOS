"""
Strategic Planning Models

Genesis 13.50
"""

from dataclasses import dataclass, field


@dataclass
class StrategicGoal:
    goal_id: str

    description: str

    constraints: dict = field(default_factory=dict)


@dataclass
class MissionPlan:
    mission_id: str

    objective: str

    steps: list = field(default_factory=list)

    status: str = "created"
