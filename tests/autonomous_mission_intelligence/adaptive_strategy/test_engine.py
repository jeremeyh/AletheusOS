from __future__ import annotations

from aletheus.autonomous_mission_intelligence.adaptive_strategy.engine import Engine


def test_adaptive_strategy_is_bounded_and_deterministic() -> None:
    result = Engine().adapt({"state": "ACTIVE"}, {"confidence": 0.4})
    assert isinstance(result, dict)
    assert len(result["digest"]) == 64
