from __future__ import annotations

from typing import ClassVar

from .base import VocabularyEngineBase
from .models import VocabularyTerm


class Engine(VocabularyEngineBase):
    FAMILY: ClassVar[str] = "COMPETITIVE_DOMAIN"

    TERMS: ClassVar[tuple[VocabularyTerm, ...]] = (
        VocabularyTerm(
            name="Locker Room",
            meaning="Private collector workspace for preparation, organization, planning, and collection building.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Field Vision",
            meaning="Ability to perceive the broader collectible landscape beyond the asset immediately in view.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Scoreboard",
            meaning="At-a-glance portfolio, market, and acquisition performance state.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Draft Board",
            meaning="Ranked acquisition candidates and future collection targets.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Playbook",
            meaning="Saved strategies, rules, acquisition plans, and portfolio tactics.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Scouting Report",
            meaning="Deep intelligence report on a player, creator, franchise, asset, or category.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Game Film",
            meaning="Historical review of prior sales, market behavior, and decision outcomes.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Starting Lineup",
            meaning="Highest-priority or core assets within a portfolio.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Bench",
            meaning="Secondary holdings, developmental assets, or reserve opportunities.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Sideline",
            meaning="Watchlist, monitoring queue, and non-active opportunities.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="War Room",
            meaning="High-stakes evaluation and acquisition decision environment.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Matchup",
            meaning="Direct comparison between assets, opportunities, or market paths.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Strike Zone",
            meaning="Acceptable acquisition-value range under THOR\u1d61 governance.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Final Score",
            meaning="Concluded decision outcome after evidence and governance review.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Power Rankings",
            meaning="Ordered view of assets, categories, or opportunities by governed strength.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Rookie Watch",
            meaning="Focused monitoring of emerging creators, players, releases, or properties.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Dynasty",
            meaning="Long-horizon strategy centered on enduring portfolio strength.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Overtime",
            meaning="Extended review when evidence or negotiation remains unresolved.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
        VocabularyTerm(
            name="Championship",
            meaning="Milestone collection, portfolio, or acquisition achievement.",
            tier="HUMAN_EXPERIENCE_LANGUAGE",
            domain_family=FAMILY,
        ),
    )

    def list_terms(self) -> tuple[VocabularyTerm, ...]:
        return self.TERMS
