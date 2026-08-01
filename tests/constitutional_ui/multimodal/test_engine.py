from aletheus.constitutional_ui.multimodal.engine import Engine


def test_x():
    assert Engine().plan("NEBULAR", 0.2, 0.3).textual_equivalent
