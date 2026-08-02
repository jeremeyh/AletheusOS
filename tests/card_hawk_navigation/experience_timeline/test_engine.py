from aletheus.card_hawk_navigation.experience_timeline.engine import Engine
from aletheus.card_hawk_navigation.experience_timeline.models import TimelineEvent


def test_timeline():
    assert (
        len(
            Engine().append(
                (),
                TimelineEvent("e", "OBSERVED", "2026-08-02T00:00:00Z", "field_vision"),
            )
        )
        == 1
    )
