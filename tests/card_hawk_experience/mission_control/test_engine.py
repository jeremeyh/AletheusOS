from aletheus.card_hawk_experience.mission_control.engine import Engine


def test_x():
    assert Engine().surface().surface_id == "mission_control"
