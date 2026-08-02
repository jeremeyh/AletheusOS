from __future__ import annotations

from aletheus.autonomous_mission_intelligence.strategic_learning.engine import Engine


def test_strategic_learning_is_bounded_and_deterministic() -> None:
    result = Engine().learn(0.5, 0.4, 0.8)
    assert isinstance(result, dict)
    assert len(result["digest"]) == 64
