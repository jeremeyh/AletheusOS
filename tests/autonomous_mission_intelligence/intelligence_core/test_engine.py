from __future__ import annotations

from aletheus.autonomous_mission_intelligence.intelligence_core.engine import Engine
from aletheus.autonomous_mission_intelligence.intelligence_core.models import (
    MissionCandidate,
    StrategicObjective,
)


def test_intelligence_core_is_bounded_and_deterministic() -> None:
    objective = StrategicObjective("objective-1", "Build a constitutional strategy")
    mission = MissionCandidate(
        "mission-1", objective.objective_id, 0.8, 0.7, 1.0, 0.2, 0.9
    )
    result = Engine().evaluate(objective, [mission])
    assert isinstance(result, dict)
    assert len(result["digest"]) == 64
