from __future__ import annotations

from typing import ClassVar

from .base import VocabularyEngineBase
from .models import VocabularyTerm


class Engine(VocabularyEngineBase):
    FAMILY: ClassVar[str] = "UNIVERSAL_COLLECTION"

    TERMS: ClassVar[tuple[VocabularyTerm, ...]] = (
        VocabularyTerm(
            name="Vault",
            meaning="Secure ownership, storage, and private asset stewardship.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Gallery",
            meaning="Curated visual presentation of assets and collections.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Archive",
            meaning="Historical record, documentation, and preserved collection knowledge.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Observatory",
            meaning="Whole-landscape monitoring, analysis, and discovery.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Showcase",
            meaning="Public or presentation-focused display of selected assets.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Discovery",
            meaning="Opportunity finding, category exploration, and emerging asset identification.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Expedition",
            meaning="Purposeful research journey through a market, collection, or category.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Horizon",
            meaning="Forward-looking market outlook and projected opportunity space.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Compass",
            meaning="Guidance, orientation, and strategic next-step assistance.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Atlas",
            meaning="Comprehensive map of collections, categories, players, creators, and markets.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Beacon",
            meaning="High-priority signal, alert, or emerging opportunity.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Pulse",
            meaning="Current state, movement, momentum, or activity level.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Signal",
            meaning="Meaningful event, condition, anomaly, or intelligence indicator.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Panorama",
            meaning="Broad, connected view across multiple assets and markets.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Nexus",
            meaning="Central point where assets, markets, evidence, and intelligence converge.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Foundry",
            meaning="Place where collection strategies, reports, and structured outputs are formed.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Registry",
            meaning="Canonical index of assets, identities, provenance, and classification.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Chronicle",
            meaning="Narrative timeline of asset, collection, and market history.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Ledger",
            meaning="Transaction, ownership, valuation, and audit record.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Provenance",
            meaning="Chain of origin, ownership, authenticity, and evidentiary support.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Cabinet",
            meaning="Private thematic grouping of carefully selected collectibles.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Exhibit",
            meaning="Focused presentation around a theme, creator, franchise, event, or era.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Treasury",
            meaning="Concentrated view of prized, rare, or strategically important assets.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Collection Hall",
            meaning="Broad organized presentation of owned assets.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
    )

    def list_terms(self) -> tuple[VocabularyTerm, ...]:
        return self.TERMS
