from aletheus.card_hawk_experience.field_vision_scoreboard.engine import Engine


def test_x():
    e = Engine()
    assert (
        e.field_vision().surface_id == "field_vision"
        and e.scoreboard().surface_id == "scoreboard"
    )
