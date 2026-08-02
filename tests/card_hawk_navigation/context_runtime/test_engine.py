from aletheus.card_hawk_navigation.context_runtime.engine import Engine
from aletheus.card_hawk_navigation.context_runtime.models import NavigationContext


def test_context():
    c = NavigationContext("s", "scouting_report", asset_id="a")
    assert Engine().propagate(c, "war_room").asset_id == "a"
