from __future__ import annotations

from typing import ClassVar

from .base import VocabularyEngineBase
from .models import VocabularyTerm


class Engine(VocabularyEngineBase):
    FAMILY: ClassVar[str] = "COMMAND_OPERATIONS"

    TERMS: ClassVar[tuple[VocabularyTerm, ...]] = (
        VocabularyTerm(
            name="Operations",
            meaning="Day-to-day activity and workflow coordination.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Mission Control",
            meaning="Active mission orchestration and status management.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Command Center",
            meaning="Unified intelligence and decision environment.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Situation Room",
            meaning="Focused response space for major market, portfolio, or asset events.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Control Tower",
            meaning="Oversight of concurrent acquisitions, listings, alerts, and portfolio flows.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Workshop",
            meaning="Hands-on asset preparation, metadata refinement, and collection maintenance.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Foundry",
            meaning="Creation of reports, strategies, valuation models, and collection outputs.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Forge",
            meaning="Construction and refinement of advanced collection intelligence artifacts.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Queue",
            meaning="Ordered work, review, and decision pipeline.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Dispatch",
            meaning="Routing of actions, alerts, reports, and acquisition tasks.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Blueprint",
            meaning="Structured plan for a collection, acquisition campaign, or portfolio objective.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Studio",
            meaning="Creative environment for curation, storytelling, and presentation.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Laboratory",
            meaning="Controlled analytical environment for experimentation and validation.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Refinery",
            meaning="Process for improving metadata, evidence quality, valuation, or collection strategy.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
    )

    def list_terms(self) -> tuple[VocabularyTerm, ...]:
        return self.TERMS
