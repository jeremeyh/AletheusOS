from aletheus.a3ye.balance_engine.engine import Engine


def test_x() -> None:
    result = Engine().score(
        veracity=0.9,
        governance=1,
        predictive_stability=0.8,
        principle_x=0.95,
        entropy=0.1,
    )
    assert result.overall_strength > 0.8
