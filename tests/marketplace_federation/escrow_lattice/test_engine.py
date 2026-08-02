from aletheus.marketplace_federation.escrow_lattice.engine import Engine


def test_engine_constructs() -> None:
    assert Engine() is not None
