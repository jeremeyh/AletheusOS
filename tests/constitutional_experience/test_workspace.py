from aletheus.constitutional_experience.workspace_composer.engine import (
    Engine,
    Instrument,
)


def test_compose():
    assert Engine().compose([Instrument("a", 0.2), Instrument("b", 0.9)], 1) == ["b"]
