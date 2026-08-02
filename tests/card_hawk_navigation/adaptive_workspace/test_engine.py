from aletheus.card_hawk_navigation.adaptive_workspace.engine import Engine


def test_layout():
    assert Engine().layout_for("buying")[0].surface_id == "war_room"
