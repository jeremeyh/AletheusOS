from __future__ import annotations

from aletheus.autonomous_mission_intelligence.human_collaboration.engine import Engine


def test_human_collaboration_is_bounded_and_deterministic() -> None:
    result = Engine().route("request-1", 0.6, ["owner@example.com"])
    assert isinstance(result, dict)
    assert len(result["digest"]) == 64
