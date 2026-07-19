import pytest

from aletheus.platform_intelligence.constitutional import (
    ConstitutionalRelationship,
    RelationshipKind,
)


def test_relationship_creation() -> None:
    relationship = ConstitutionalRelationship.create(
        source="service.workspace",
        target="runtime.core",
        kind=RelationshipKind.DEPENDS_ON,
    )

    assert str(relationship.source) == "service.workspace"
    assert str(relationship.target) == "runtime.core"
    assert relationship.kind is RelationshipKind.DEPENDS_ON


def test_self_relationship_is_rejected() -> None:
    with pytest.raises(ValueError):
        ConstitutionalRelationship.create(
            source="runtime.core",
            target="runtime.core",
            kind=RelationshipKind.DEPENDS_ON,
        )
