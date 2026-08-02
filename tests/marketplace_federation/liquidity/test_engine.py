from aletheus.marketplace_federation.liquidity.engine import Engine


def test_engine_constructs() -> None:
    assert Engine() is not None
