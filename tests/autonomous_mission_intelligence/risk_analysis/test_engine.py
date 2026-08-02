from __future__ import annotations

from aletheus.autonomous_mission_intelligence.risk_analysis.engine import Engine


def test_risk_analysis_is_bounded_and_deterministic() -> None:
    result = Engine().analyze({"operational": 0.2, "security": 0.1})
    assert isinstance(result, dict)
    assert len(result["digest"]) == 64
