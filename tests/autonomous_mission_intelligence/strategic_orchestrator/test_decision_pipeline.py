from aletheus.autonomous_mission_intelligence.strategic_orchestrator.decision_pipeline import (
    DecisionPipeline,
)


def test_decision_pipeline_runs_all_expansion_stages() -> None:
    result = DecisionPipeline().run({"strategy": "bounded"})
    assert result["genesis34DecisionExpansion"] is True
    assert result["humanAuthority"] == "PRESERVED"
    assert result["executionAuthorized"] is False
    assert len(result["decisionStages"]) == 12
