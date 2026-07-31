"""
AletheusOS
Genesis 47.0

Proof 001

Canonical Identity Framework™

Constitutional Identity Proof
"""

from __future__ import annotations

from pprint import pprint

from aletheus.canonical_identity import (
    IdentityType,
    TrustLevel,
    canonical_identity_framework,
)


def print_header(title: str) -> None:

    print()
    print(title)
    print("=" * len(title))


def main() -> None:

    print_header("CANONICAL IDENTITY FRAMEWORK v1.0 PROOF")

    founder = canonical_identity_framework.create_identity(
        canonical_name="identity.founder.master_lord_6ixth",
        display_name="Jeremey Harvey",
        identity_type=IdentityType.PERSON,
        trust_level=TrustLevel.FOUNDATION,
        organizations=["6th Dimension Multimedia"],
        roles=["Founder", "Chief Architect"],
        applications=["CardHawk"],
    )

    organization = canonical_identity_framework.create_identity(
        canonical_name="organization.6dm",
        display_name="6th Dimension Multimedia",
        identity_type=IdentityType.ORGANIZATION,
        trust_level=TrustLevel.FOUNDATION,
    )

    application = canonical_identity_framework.create_identity(
        canonical_name="application.cardhawk",
        display_name="CardHawk",
        identity_type=IdentityType.APPLICATION,
        trust_level=TrustLevel.APPLICATION,
    )

    founder.add_relationship(
        relationship_type="FOUNDED",
        target_identity=organization.identity_id,
    )

    founder.add_relationship(
        relationship_type="CREATED",
        target_identity=application.identity_id,
    )

    print_header("FOUNDER")

    pprint(founder.to_dict())

    print_header("ORGANIZATION")

    pprint(organization.to_dict())

    print_header("APPLICATION")

    pprint(application.to_dict())

    print_header("ALL IDENTITIES")

    for identity in canonical_identity_framework.identities():
        pprint(identity.to_dict())

    print_header("HEALTH")

    pprint(canonical_identity_framework.health())

    print_header("STATISTICS")

    pprint(canonical_identity_framework.statistics())


if __name__ == "__main__":
    main()
