from aletheus.autonomous_mission_intelligence.predictive_validation.engine import Engine


def test_engine_preserves_human_authority() -> None:
    result = Engine().execute({"objective": "test"})
    assert result["humanAuthority"] == "PRESERVED"
    assert result["executionAuthorized"] is False
    assert result["requiresHumanAuthorization"] is True
    assert "Predictive Validation Engine" in result["decisionStages"]
