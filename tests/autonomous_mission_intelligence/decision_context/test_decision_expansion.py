from aletheus.autonomous_mission_intelligence.decision_context.engine import Engine


def test_engine_preserves_human_authority() -> None:
    result = Engine().execute({"objective": "test"})
    assert result["humanAuthority"] == "PRESERVED"
    assert result["executionAuthorized"] is False
    assert result["requiresHumanAuthorization"] is True
    assert "Decision Context Engine" in result["decisionStages"]
