from __future__ import annotations

from typing import ClassVar

from .base import VocabularyEngineBase
from .models import VocabularyTerm


class Engine(VocabularyEngineBase):
    FAMILY: ClassVar[str] = "SIGNAL_OBSERVATION_INTELLIGENCE"

    TERMS: ClassVar[tuple[VocabularyTerm, ...]] = (
        VocabularyTerm(
            name="Observatory",
            meaning="High-level market and collection observation environment.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Radar",
            meaning="Continuous monitoring across marketplaces and categories.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Signal",
            meaning="Meaningful indicator extracted from data and events.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Pulse",
            meaning="Current activity, momentum, and health.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Spectrum",
            meaning="Multi-dimensional distribution of value, risk, scarcity, and momentum.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Telemetry",
            meaning="Live operational and market measurements.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Field Vision",
            meaning="Connected, contextual awareness across the entire collectible landscape.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Panorama",
            meaning="Broad visual synthesis across domains.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Lens",
            meaning="Focused analytical perspective or filter.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Aperture",
            meaning="Controlled scope of observation and evidence intake.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Beacon",
            meaning="High-confidence priority signal.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Constellation",
            meaning="Network of related assets, creators, franchises, and evidence.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Watchtower",
            meaning="Persistent high-level monitoring for risk, opportunity, and change.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Spotlight",
            meaning="Focused attention on a high-priority asset, creator, or event.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Echo",
            meaning="Recurring pattern, repeated signal, or historical resonance.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Insight",
            meaning="Interpreted understanding derived from governed evidence.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
    )

    def list_terms(self) -> tuple[VocabularyTerm, ...]:
        return self.TERMS
