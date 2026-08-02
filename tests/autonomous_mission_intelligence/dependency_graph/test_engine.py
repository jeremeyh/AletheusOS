from __future__ import annotations

from aletheus.autonomous_mission_intelligence.dependency_graph.engine import Engine
from aletheus.autonomous_mission_intelligence.dependency_graph.models import (
    MissionCandidate,
    StrategicObjective,
)


def test_dependency_graph_is_bounded_and_deterministic() -> None:
    objective = StrategicObjective("objective-1", "Build a constitutional strategy")
    mission = MissionCandidate(
        "mission-1", objective.objective_id, 0.8, 0.7, 1.0, 0.2, 0.9
    )
    result = Engine().compile([mission])
    assert isinstance(result, dict)
    assert len(result["digest"]) == 64
