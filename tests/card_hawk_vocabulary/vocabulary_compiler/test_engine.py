from aletheus.card_hawk_vocabulary.vocabulary_compiler.engine import Engine
from aletheus.card_hawk_vocabulary.vocabulary_compiler.models import (
    CapabilityMapping,
    VocabularyTerm,
)


def test_compile() -> None:
    terms = (
        VocabularyTerm(
            "Field Vision",
            "Broad collectible landscape awareness.",
            "HUMAN_EXPERIENCE_LANGUAGE",
            "COMPETITIVE_DOMAIN",
        ),
        VocabularyTerm(
            "Scoreboard",
            "At-a-glance portfolio and market state.",
            "HUMAN_EXPERIENCE_LANGUAGE",
            "COMPETITIVE_DOMAIN",
        ),
    )
    mappings = (
        CapabilityMapping(
            "Gathering Mesh",
            "Market Intelligence",
            "Field Vision",
            "Perceive the broader collectible landscape.",
        ),
        CapabilityMapping(
            "Balance Engine",
            "Portfolio Performance",
            "Scoreboard",
            "Summarize current standing.",
        ),
    )
    result = Engine().compile(
        application="CARD_HAWK",
        terms=terms,
        mappings=mappings,
    )
    assert result["valid"] is True
