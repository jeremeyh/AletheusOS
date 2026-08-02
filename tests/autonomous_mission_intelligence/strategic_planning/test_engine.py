from __future__ import annotations

from aletheus.autonomous_mission_intelligence.strategic_planning.engine import Engine
from aletheus.autonomous_mission_intelligence.strategic_planning.models import (
    StrategicObjective,
)


def test_strategic_planning_is_bounded_and_deterministic() -> None:
    objective = StrategicObjective("objective-1", "Build a constitutional strategy")
    result = Engine().plan(objective)
    assert isinstance(result, dict)
    assert len(result["digest"]) == 64
