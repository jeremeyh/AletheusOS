from aletheus.autonomous_collector.collector_orchestrator.engine import Engine
from aletheus.autonomous_collector.collector_orchestrator.models import (
    CollectorPolicy,
    Mission,
    Opportunity,
)


def test_human_authority_is_preserved() -> None:
    result = Engine().evaluate(
        Mission("m-1", "Acquire scarce asset", 300.0),
        Opportunity(
            "o-1",
            "a-1",
            "CARD_HAWK",
            180.0,
            240.0,
            0.93,
        ),
        CollectorPolicy(),
    )

    assert result["immutableDecisionContract"] is True
    assert result["requiresHumanApproval"] is True
    assert result["executionAuthorized"] is False
    assert result["directives"]["executionAuthorized"] is False
    assert result["humanAuthority"]["status"] == "PRESERVED"
    assert len(result["digest"]) == 64
