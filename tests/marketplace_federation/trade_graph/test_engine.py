from aletheus.marketplace_federation.trade_graph.engine import Engine


def test_engine_constructs() -> None:
    assert Engine() is not None
