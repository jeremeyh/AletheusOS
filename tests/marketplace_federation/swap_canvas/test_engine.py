from aletheus.marketplace_federation.swap_canvas.engine import Engine


def test_engine_constructs() -> None:
    assert Engine() is not None
