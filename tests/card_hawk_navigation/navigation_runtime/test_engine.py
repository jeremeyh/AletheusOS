from aletheus.card_hawk_navigation.navigation_runtime.engine import Engine
from aletheus.card_hawk_navigation.navigation_runtime.models import NavigationContext


def test_navigation():
    c = NavigationContext("s", "locker_room")
    assert Engine().navigate(c, "vault").current_node == "vault"
