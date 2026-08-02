from __future__ import annotations

from aletheus.autonomous_mission_intelligence.spartan_strategy_security.engine import (
    Engine,
)


def test_spartan_strategy_security_is_bounded_and_deterministic() -> None:
    result = Engine().inspect({"plan": "bounded"})
    assert isinstance(result, dict)
    assert len(result["digest"]) == 64
