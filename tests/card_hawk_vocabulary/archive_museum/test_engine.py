from aletheus.card_hawk_vocabulary.archive_museum.engine import Engine


def test_provenance() -> None:
    assert "Authenticity" in Engine().resolve("Provenance").meaning
