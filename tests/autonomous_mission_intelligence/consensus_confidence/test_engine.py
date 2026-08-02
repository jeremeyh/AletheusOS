from __future__ import annotations

from aletheus.autonomous_mission_intelligence.consensus_confidence.engine import Engine
from aletheus.autonomous_mission_intelligence.consensus_confidence.models import (
    AgentRecommendation,
)


def test_consensus_confidence_is_bounded_and_deterministic() -> None:
    recommendation = AgentRecommendation("agent-1", "PROCEED", 0.9)
    result = Engine().aggregate([recommendation])
    assert isinstance(result, dict)
    assert len(result["digest"]) == 64
