from aletheus.marketplace_federation.orchestrator.engine import Engine


def test_engine_constructs() -> None:
    assert Engine() is not None
