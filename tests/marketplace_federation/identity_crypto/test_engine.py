from aletheus.marketplace_federation.identity_crypto.engine import Engine


def test_engine_constructs() -> None:
    assert Engine() is not None
