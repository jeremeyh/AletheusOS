"""
AletheusOS
Genesis 48.0

Proof 001

Double Hedron Session Memory™

Constitutional Memory Proof
"""

from __future__ import annotations

from pprint import pprint

from aletheus.double_hedron import (
    MemoryLifecycle,
    MemoryType,
    double_hedron,
)


def header(title: str) -> None:

    print()
    print(title)
    print("=" * len(title))


def main() -> None:

    memory = double_hedron.remember(
        identity="identity.founder.master_lord_6ixth",
        capability="foundation.appraiserx",
        execution="EXEC-0001",
        session="SESSION-0001",
        memory_type=MemoryType.OBSERVATION,
        observation="Caleb Williams Bowman valuation requested.",
        evidence=[
            "Marketplace Intelligence",
            "Portfolio Analysis",
        ],
        reasoning=[
            "Intent resolved",
            "Marketplace evidence gathered",
            "Portfolio context applied",
        ],
        confidence=0.94,
        provenance={
            "application": "CardHawk",
            "genesis": "48.0",
        },
    )

    header("CREATED MEMORY")

    pprint(memory.to_dict())

    header("RECALL BY IDENTITY")

    memories = double_hedron.recall(identity="identity.founder.master_lord_6ixth")

    pprint([m.to_dict() for m in memories])

    header("PROMOTION")

    double_hedron.consolidate(
        memory,
        MemoryLifecycle.VALIDATED,
    )

    pprint(memory.to_dict())

    header("HEALTH")

    pprint(double_hedron.health())

    header("STATISTICS")

    pprint(double_hedron.statistics())


if __name__ == "__main__":
    main()
