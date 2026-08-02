from __future__ import annotations

from json import dumps

from .engine import Engine
from .models import (
    MissionCandidate,
    ResourceCapacity,
    StrategicObjective,
)


def main() -> None:
    objective = StrategicObjective(
        "objective-demo", "Demonstrate Resource Optimization Intelligence"
    )
    mission = MissionCandidate(
        "mission-demo", objective.objective_id, 0.8, 0.7, 1.0, 0.2, 0.9
    )
    resource = ResourceCapacity("resource-demo", 10.0)
    result = Engine().allocate([mission], [resource])
    print(dumps(result, indent=2, sort_keys=True))
