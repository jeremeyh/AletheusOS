from aletheus.marketplace_federation.federation_api.engine import Engine


def test_engine_constructs() -> None:
    assert Engine() is not None
