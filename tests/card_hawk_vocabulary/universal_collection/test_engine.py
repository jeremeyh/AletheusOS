from aletheus.card_hawk_vocabulary.universal_collection.engine import Engine


def test_terms() -> None:
    assert Engine().resolve("Vault").meaning.startswith("Secure")
