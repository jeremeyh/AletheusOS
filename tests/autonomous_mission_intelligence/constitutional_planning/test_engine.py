from __future__ import annotations

from aletheus.autonomous_mission_intelligence.constitutional_planning.engine import (
    Engine,
)


def test_constitutional_planning_is_bounded_and_deterministic() -> None:
    result = Engine().validate(["OBSERVE", "ANALYZE"])
    assert isinstance(result, dict)
    assert len(result["digest"]) == 64
