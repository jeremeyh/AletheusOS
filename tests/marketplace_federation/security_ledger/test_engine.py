from aletheus.marketplace_federation.security_ledger.engine import Engine


def test_engine_constructs() -> None:
    assert Engine() is not None
