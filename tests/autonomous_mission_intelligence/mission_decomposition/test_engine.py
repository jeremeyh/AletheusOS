from __future__ import annotations

from aletheus.autonomous_mission_intelligence.mission_decomposition.engine import Engine
from aletheus.autonomous_mission_intelligence.mission_decomposition.models import (
    StrategicObjective,
)


def test_mission_decomposition_is_bounded_and_deterministic() -> None:
    objective = StrategicObjective("objective-1", "Build a constitutional strategy")
    result = Engine().decompose(objective)
    assert isinstance(result, dict)
    assert len(result["digest"]) == 64
