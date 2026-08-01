from aletheus.card_hawk_vocabulary.core.engine import Engine
from aletheus.card_hawk_vocabulary.core.models import VocabularyLibrary


def test_core() -> None:
    result = Engine().describe(VocabularyLibrary("card-hawk", "27.0.0", ()))
    assert "signature" in result
