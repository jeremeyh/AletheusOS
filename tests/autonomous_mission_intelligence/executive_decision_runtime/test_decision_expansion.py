from aletheus.autonomous_mission_intelligence.executive_decision_runtime.engine import (
    Engine,
)


def test_engine_preserves_human_authority() -> None:
    result = Engine().execute({"objective": "test"})
    assert result["humanAuthority"] == "PRESERVED"
    assert result["executionAuthorized"] is False
    assert result["requiresHumanAuthorization"] is True
    assert "Executive Decision Runtime" in result["decisionStages"]
