from aletheus.tooling.intelligent_regression.engine import Engine, Regression


def test_regression_engine() -> None:
    report = Engine().analyze((Regression("latency", 95, 96),))
    assert report["regression_count"] == 0
