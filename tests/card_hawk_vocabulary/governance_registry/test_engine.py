from aletheus.card_hawk_vocabulary.governance_registry.engine import Engine
from aletheus.card_hawk_vocabulary.governance_registry.models import VocabularyTerm


def test_registry() -> None:
    terms = (
        VocabularyTerm(
            "Vault",
            "x",
            "HUMAN_EXPERIENCE_LANGUAGE",
            "UNIVERSAL",
        ),
    )
    assert Engine().validate(terms)["valid"] is True
