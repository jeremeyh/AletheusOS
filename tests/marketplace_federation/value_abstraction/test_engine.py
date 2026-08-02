from aletheus.marketplace_federation.value_abstraction.engine import Engine


def test_engine_constructs() -> None:
    assert Engine() is not None
