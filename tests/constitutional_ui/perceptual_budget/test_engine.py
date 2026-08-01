from aletheus.constitutional_ui.perceptual_budget.engine import Cost, Engine


def test_x():
    assert "a" in Engine().allocate((Cost("a", 1, 2, 1, 1, 1, 0, 0),), 7)["selected"]
