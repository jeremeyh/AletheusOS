from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4


def _timestamp():
    return datetime.now(UTC).isoformat()


def new_identity_id(prefix: str = "identity"):
    return f"{prefix}.{uuid4().hex[:12]}"


@dataclass(slots=True)
class Identity:
    identity_id: str
    identity_type: str
    display_name: str
    profile_id: str = "consumer"
    organization: str = ""
    application: str = ""
    aliases: list[str] = field(default_factory=list)
    status: str = "active"
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=_timestamp)

    def to_dict(self):
        return {
            "identity_id": self.identity_id,
            "identity_type": self.identity_type,
            "display_name": self.display_name,
            "profile_id": self.profile_id,
            "organization": self.organization,
            "application": self.application,
            "aliases": self.aliases,
            "status": self.status,
            "metadata": self.metadata,
            "created_at": self.created_at,
        }


@dataclass(slots=True)
class IdentitySession:
    session_id: str
    identity_id: str
    authenticated: bool = False
    issued_at: str = field(default_factory=_timestamp)
    expires_at: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self):
        return {
            "session_id": self.session_id,
            "identity_id": self.identity_id,
            "authenticated": self.authenticated,
            "issued_at": self.issued_at,
            "expires_at": self.expires_at,
            "metadata": self.metadata,
        }
