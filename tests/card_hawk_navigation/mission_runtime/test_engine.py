from aletheus.card_hawk_navigation.mission_runtime.engine import Engine
from aletheus.card_hawk_navigation.mission_runtime.models import (
    MissionContext,
    NavigationContext,
)


def test_mission():
    assert (
        Engine()
        .activate(
            NavigationContext("s", "field_vision"),
            MissionContext("m", "Acquire", "Gold /10", {"maxPrice": 500}),
        )
        .mission_id
        == "m"
    )
