"""
AletheusOS
Genesis 46.1

Proof 001

Cognitive Kernel™

Constitutional Execution Proof
"""

from __future__ import annotations

from pprint import pprint

from aletheus.cognitive_kernel import (
    cognitive_kernel,
)


def print_header(title: str) -> None:

    print()
    print(title)
    print("=" * len(title))


def main() -> None:

    print_header(
        "COGNITIVE KERNEL v1.0 PROOF"
    )

    queries = [

        (
            "identity.founder.master_lord_6ixth",
            "CardHawk",
            "What is my Caleb Williams Bowman worth?",
        ),

        (
            "identity.founder.master_lord_6ixth",
            "CardHawk",
            "Should I sell my Matas Buzelis collection?",
        ),

        (
            "identity.founder.master_lord_6ixth",
            "CardHawk",
            "Find recent Rome Odunze auto comps.",
        ),

    ]

    for identity, application, query in queries:

        print()

        print(f"QUERY: {query}")

        record = cognitive_kernel.process(

            identity=identity,

            application=application,

            query=query,

        )

        pprint(record.to_dict())

    print_header("KERNEL HEALTH")

    pprint(
        cognitive_kernel.health()
    )

    print_header("KERNEL STATISTICS")

    pprint(
        cognitive_kernel.statistics()
    )

    print_header("EXECUTION HISTORY")

    pprint(
        cognitive_kernel.records()
    )


if __name__ == "__main__":

    main()
