from aletheus.a3ye.council_bridge.engine import Engine, Thesis


def test_x() -> None:
    result = Engine().deliberate(
        (Thesis("e1", "approve", 0.9, "strong"), Thesis("e2", "qualify", 0.7, "risk"))
    )
    assert result["thorxReady"] is True
