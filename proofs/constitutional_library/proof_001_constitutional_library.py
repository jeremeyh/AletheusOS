"""
AletheusOS
Genesis 51.0

Proof 001

Constitutional Library™

Institutional Knowledge Proof
"""

from __future__ import annotations

from pprint import pprint

from aletheus.constitutional_library import (
    KnowledgeType,
    constitutional_library,
)


def header(title: str) -> None:

    print()
    print(title)
    print("=" * len(title))


def main() -> None:

    #
    # Create institutional knowledge.
    #

    knowledge = constitutional_library.create(

        title="Marketplace Appraisal Principle",

        statement=(
            "Marketplace appraisals should combine "
            "market evidence, portfolio context, and "
            "constitutional reasoning."
        ),

        knowledge_type=KnowledgeType.PRINCIPLE,

        confidence=0.95,

        constitutional_articles=[
            "Principle X",
            "Evidence Before Conclusion",
            "Knowledge Stewardship Principle",
        ],

        supporting_evidence=[
            "Marketplace Intelligence",
            "Portfolio Analysis",
        ],

        related_identities=[
            "identity.founder.master_lord_6ixth",
        ],

        related_memories=[
            "MEM-EXAMPLE-0001",
        ],

        related_reasons=[
            "REASON-EXAMPLE-0001",
        ],

        execution_graph_nodes=[
            "NODE-EXAMPLE-0001",
        ],

        provenance={
            "application": "CardHawk",
            "genesis": "51.0",
        },
    )

    header("CREATED KNOWLEDGE")

    pprint(
        knowledge.to_dict()
    )

    #
    # Governance
    #

    constitutional_library.validate(
        knowledge
    )

    constitutional_library.promote(
        knowledge
    )

    header("CANONICAL KNOWLEDGE")

    pprint(
        knowledge.to_dict()
    )

    #
    # Retrieval
    #

    header("SEARCH")

    pprint(
        [
            k.to_dict()
            for k in constitutional_library.search(
                "Marketplace"
            )
        ]
    )

    header("CANONICAL")

    pprint(
        [
            k.to_dict()
            for k in constitutional_library.canonical()
        ]
    )

    #
    # Diagnostics
    #

    header("HEALTH")

    pprint(
        constitutional_library.health()
    )

    header("STATISTICS")

    pprint(
        constitutional_library.statistics()
    )


if __name__ == "__main__":

    main()
