"""
AletheusOS
Genesis 49.0

Proof 001

Reason Engine™

Constitutional Reasoning Proof
"""

from __future__ import annotations

from pprint import pprint

from aletheus.reason_engine import (
    reason_engine,
)


def header(title: str) -> None:

    print()
    print(title)
    print("=" * len(title))


def main() -> None:

    reason = reason_engine.reason(

        intent="APPRAISE",

        identity="identity.founder.master_lord_6ixth",

        query="What is my Caleb Williams Bowman worth?",

        conclusion="Marketplace appraisal should be performed.",

        evidence=[
            "Marketplace Intelligence",
            "Portfolio Analysis",
        ],

        memories_used=[
            "MEM-EXAMPLE-0001",
        ],

        constitutional_articles=[
            "Principle X",
            "Evidence Before Conclusion",
            "Reason Transparency Principle",
        ],

        confidence=0.93,

        provenance={
            "application": "CardHawk",
            "genesis": "49.0",
        },
    )

    header("REASON OBJECT")

    pprint(
        reason.to_dict()
    )

    header("HEALTH")

    pprint(
        reason_engine.health()
    )

    header("STATISTICS")

    pprint(
        reason_engine.statistics()
    )


if __name__ == "__main__":

    main()
