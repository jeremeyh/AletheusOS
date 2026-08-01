from aletheus.card_hawk_experience.war_room.engine import Engine


def test_x():
    assert Engine().analyze("offer", 75.0)["marketplaceCommitAllowed"] is False
