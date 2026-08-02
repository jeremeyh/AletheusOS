from aletheus.marketplace_federation.connector_runtime.engine import Engine


def test_engine_constructs() -> None:
    assert Engine() is not None
