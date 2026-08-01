from aletheus.a3ye.peg.engine import Engine, Invariant


def test_x() -> None:
    result = Engine().evaluate(
        {"mode": "simulation"}, (Invariant("i", "mode", "equals", "simulation"),)
    )
    assert result["executionAllowed"] is True
