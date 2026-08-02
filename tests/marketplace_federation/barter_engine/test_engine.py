from aletheus.marketplace_federation.barter_engine.engine import Engine


def test_engine_constructs() -> None:
    assert Engine() is not None
