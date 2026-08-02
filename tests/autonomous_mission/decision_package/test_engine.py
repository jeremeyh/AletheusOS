from __future__ import annotations

from aletheus.autonomous_mission.decision_package.engine import Engine
from aletheus.autonomous_mission.decision_package.models import MissionSpec


def test_engine_preserves_mission_contract() -> None:
    mission = MissionSpec(
        mission_id="mission-demo",
        objective="Find and evaluate a bounded opportunity",
        domain="CARD_HAWK",
        budget=1500.0,
        priority=80,
    )
    result = Engine().evaluate(mission)
    assert isinstance(result, dict)
    assert result
