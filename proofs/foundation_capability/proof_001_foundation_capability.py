"""
AletheusOS
Genesis 47.5

Proof 001

Foundation Capability Base™

Constitutional Engineering Proof
"""

from __future__ import annotations

from pprint import pprint

from aletheus.foundation.capability import (
    CapabilityMetadata,
    FoundationCapability,
    FoundationCapabilityContract,
    health,
    statistics,
)


class ExampleCapability(FoundationCapability):
    """
    Example capability used to certify
    the Foundation Capability Base.
    """

    def __init__(self) -> None:

        metadata = CapabilityMetadata(
            name="Example Capability",
            genesis="47.5",
            version="1.0.0",
            description="Foundation engineering proof capability.",
            certification="prototype",
            constitutional_articles=[
                "Principle X",
                "Proof Before Promotion",
                "Elegant Sufficiency",
            ],
            dependencies=[
                "Foundation Capability Base",
            ],
            proofs=[
                "proof_001_foundation_capability",
            ],
        )

        super().__init__(metadata)

    def statistics(self) -> dict:

        stats = super().statistics()

        stats["example_counter"] = 1

        return stats


def print_header(title: str) -> None:

    print()
    print(title)
    print("=" * len(title))


def main() -> None:

    capability = ExampleCapability()

    contract = FoundationCapabilityContract(
        capability_name=capability.name,
        purpose="Demonstrate Foundation engineering.",
        responsibilities=[
            "Publish metadata",
            "Publish health",
            "Publish statistics",
        ],
        non_responsibilities=[
            "Business logic",
            "Workflow execution",
        ],
        constitutional_articles=[
            "Principle X",
            "Proof Before Promotion",
        ],
    )

    print_header("METADATA")

    pprint(
        capability.capability_metadata()
    )

    print_header("HEALTH")

    pprint(
        health(capability)
    )

    print_header("STATISTICS")

    pprint(
        statistics(capability)
    )

    print_header("FOUNDATION CONTRACT")

    pprint(
        contract.to_dict()
    )


if __name__ == "__main__":

    main()
