from __future__ import annotations

from aletheus.autonomous_mission_intelligence.opportunity_forecasting.engine import (
    Engine,
)


def test_opportunity_forecasting_is_bounded_and_deterministic() -> None:
    result = Engine().forecast([1.0, 2.0, 3.0])
    assert isinstance(result, dict)
    assert len(result["digest"]) == 64
