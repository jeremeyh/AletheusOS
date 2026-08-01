from aletheus.card_hawk_experience.locker_room.engine import Engine


def test_x():
    assert Engine().surface().display_name == "Locker Room™"
