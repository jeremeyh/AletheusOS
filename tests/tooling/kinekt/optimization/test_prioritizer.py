from aletheus.tooling.kinekt.optimization.prioritizer import score


def test_priority_score() -> None:
    assert score("high", "low", "low", 0.9, 5.0) > 50
