from aletheus.card_hawk_vocabulary.competitive_domain.engine import Engine


def test_field_vision() -> None:
    assert "broader collectible landscape" in Engine().resolve("Field Vision").meaning
