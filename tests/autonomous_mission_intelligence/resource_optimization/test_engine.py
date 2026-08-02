from __future__ import annotations

from aletheus.autonomous_mission_intelligence.resource_optimization.engine import Engine
from aletheus.autonomous_mission_intelligence.resource_optimization.models import (
    MissionCandidate,
    ResourceCapacity,
    StrategicObjective,
)


def test_resource_optimization_is_bounded_and_deterministic() -> None:
    objective = StrategicObjective("objective-1", "Build a constitutional strategy")
    mission = MissionCandidate(
        "mission-1", objective.objective_id, 0.8, 0.7, 1.0, 0.2, 0.9
    )
    resource = ResourceCapacity("resource-1", 10.0)
    result = Engine().allocate([mission], [resource])
    assert isinstance(result, dict)
    assert len(result["digest"]) == 64
