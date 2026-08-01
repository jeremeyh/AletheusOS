from aletheus.uxr.interaction.engine import Engine, Event


def test_x():
    assert Engine().dispatch(Event("onSelect", "n", {}))["accepted"]
