from aletheus.marketplace_federation.spartan_security.engine import Engine


def test_engine_constructs() -> None:
    assert Engine() is not None
