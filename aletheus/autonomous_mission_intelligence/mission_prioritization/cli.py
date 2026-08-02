from __future__ import annotations

from json import dumps

from .engine import Engine
from .models import (
    MissionCandidate,
    StrategicObjective,
)


def main() -> None:
    objective = StrategicObjective(
        "objective-demo", "Demonstrate Mission Prioritization Engine"
    )
    mission = MissionCandidate(
        "mission-demo", objective.objective_id, 0.8, 0.7, 1.0, 0.2, 0.9
    )
    result = Engine().rank([mission])
    print(dumps(result, indent=2, sort_keys=True))
