from aletheus.card_hawk_navigation.intelligence_dock.engine import Engine


def test_dock():
    assert "THORᵡ" in Engine().items_for("war_room")
