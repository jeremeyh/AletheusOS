from __future__ import annotations

from typing import ClassVar

from .base import VocabularyEngineBase
from .models import VocabularyTerm


class Engine(VocabularyEngineBase):
    FAMILY: ClassVar[str] = "ARCHIVE_MUSEUM_PROVENANCE"

    TERMS: ClassVar[tuple[VocabularyTerm, ...]] = (
        VocabularyTerm(
            name="Archive",
            meaning="Preserved historical and documentary record.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Gallery",
            meaning="Curated visual collection view.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Exhibit",
            meaning="Focused presentation around a theme, creator, event, franchise, or period.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Collection Hall",
            meaning="Broad organized view of owned assets.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Registry",
            meaning="Canonical identification and classification system.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Ledger",
            meaning="Ownership, valuation, transaction, and audit history.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Provenance",
            meaning="Authenticity, origin, ownership, and evidence lineage.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Chronicle",
            meaning="Timeline of asset and collection history.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Catalog",
            meaning="Structured searchable inventory of collectible assets.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Cabinet",
            meaning="Specialized private grouping of high-value or thematic assets.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Curator",
            meaning="Guided organization, interpretation, and presentation intelligence.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Conservation",
            meaning="Condition, preservation, and long-term stewardship workspace.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Restoration",
            meaning="Documented repair, recovery, or condition-improvement history.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Heritage",
            meaning="Historical, cultural, and generational significance of an asset or collection.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Legacy",
            meaning="Long-term impact, narrative, and enduring collection value.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
    )

    def list_terms(self) -> tuple[VocabularyTerm, ...]:
        return self.TERMS
