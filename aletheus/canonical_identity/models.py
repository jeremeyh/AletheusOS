"""
AletheusOS
Genesis 47.0

Canonical Identity Framework™

Canonical Models
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


def new_identity_id() -> str:
    return f"ID-{uuid4().hex[:12].upper()}"


class IdentityType(StrEnum):

    PERSON = "PERSON"

    ORGANIZATION = "ORGANIZATION"

    APPLICATION = "APPLICATION"

    SERVICE = "SERVICE"

    CONNECTOR = "CONNECTOR"

    AGENT = "AGENT"

    COUNCIL_MEMBER = "COUNCIL_MEMBER"

    SYSTEM = "SYSTEM"

    DEVICE = "DEVICE"


class TrustLevel(StrEnum):

    UNKNOWN = "UNKNOWN"

    EXTERNAL = "EXTERNAL"

    USER = "USER"

    APPLICATION = "APPLICATION"

    ENTERPRISE = "ENTERPRISE"

    FOUNDATION = "FOUNDATION"

    SYSTEM = "SYSTEM"


class IdentityStatus(StrEnum):

    ACTIVE = "ACTIVE"

    DISABLED = "DISABLED"

    ARCHIVED = "ARCHIVED"


@dataclass(slots=True)
class IdentityRelationship:

    relationship_type: str

    target_identity: str

    metadata: dict[str, Any] = field(default_factory=dict)

    created_at: str = field(default_factory=utc_now)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class CanonicalIdentity:

    identity_id: str

    canonical_name: str

    display_name: str

    identity_type: IdentityType

    trust_level: TrustLevel

    status: IdentityStatus = IdentityStatus.ACTIVE

    organizations: list[str] = field(default_factory=list)

    roles: list[str] = field(default_factory=list)

    applications: list[str] = field(default_factory=list)

    permissions: list[str] = field(default_factory=list)

    relationships: list[IdentityRelationship] = field(default_factory=list)

    memory_references: list[str] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)

    created_at: str = field(default_factory=utc_now)

    updated_at: str = field(default_factory=utc_now)

    def add_relationship(
        self,
        relationship_type: str,
        target_identity: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:

        self.relationships.append(
            IdentityRelationship(
                relationship_type=relationship_type,
                target_identity=target_identity,
                metadata=metadata or {},
            )
        )

        self.updated_at = utc_now()

    def to_dict(self) -> dict[str, Any]:

        return {
            "identity_id": self.identity_id,
            "canonical_name": self.canonical_name,
            "display_name": self.display_name,
            "identity_type": self.identity_type.value,
            "trust_level": self.trust_level.value,
            "status": self.status.value,
            "organizations": self.organizations,
            "roles": self.roles,
            "applications": self.applications,
            "permissions": self.permissions,
            "relationships": [
                relationship.to_dict()
                for relationship in self.relationships
            ],
            "memory_references": self.memory_references,
            "metadata": self.metadata,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
