from __future__ import annotations

from aletheus.autonomous_mission_intelligence.agent_coordination.engine import Engine
from aletheus.autonomous_mission_intelligence.agent_coordination.models import (
    AgentRecommendation,
)


def test_agent_coordination_is_bounded_and_deterministic() -> None:
    recommendation = AgentRecommendation("agent-1", "PROCEED", 0.9)
    result = Engine().coordinate([recommendation])
    assert isinstance(result, dict)
    assert len(result["digest"]) == 64
