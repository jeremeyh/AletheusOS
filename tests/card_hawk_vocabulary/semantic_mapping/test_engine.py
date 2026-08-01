from aletheus.card_hawk_vocabulary.semantic_mapping.engine import Engine


def test_mapping() -> None:
    assert "Field Vision" in Engine().experience_for("Gathering Mesh")
