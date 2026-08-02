from aletheus.card_hawk_navigation.overlay_manager.engine import Engine
from aletheus.card_hawk_navigation.overlay_manager.models import NavigationContext


def test_overlay():
    assert (
        "A•3ye" in Engine().open(NavigationContext("s", "war_room"), "A•3ye").overlays
    )
