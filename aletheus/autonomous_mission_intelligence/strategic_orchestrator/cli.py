from __future__ import annotations

from json import dumps

from .engine import Engine
from .models import (
    AgentRecommendation,
    MissionCandidate,
    StrategicObjective,
)


def main() -> None:
    objective = StrategicObjective(
        "objective-demo", "Demonstrate Autonomous Strategic Orchestrator"
    )
    mission = MissionCandidate(
        "mission-demo", objective.objective_id, 0.8, 0.7, 1.0, 0.2, 0.9
    )
    recommendation = AgentRecommendation("agent-demo", "PROCEED", 0.9)
    result = Engine().orchestrate(objective, [mission], [recommendation])
    print(dumps(result, indent=2, sort_keys=True))
