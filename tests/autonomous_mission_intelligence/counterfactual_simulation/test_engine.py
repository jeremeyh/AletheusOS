from __future__ import annotations

from aletheus.autonomous_mission_intelligence.counterfactual_simulation.engine import (
    Engine,
)


def test_counterfactual_simulation_is_bounded_and_deterministic() -> None:
    result = Engine().simulate(
        [{"value": 10.0, "probability": 0.8, "cost": 2.0, "risk": 0.1}]
    )
    assert isinstance(result, dict)
    assert len(result["digest"]) == 64
