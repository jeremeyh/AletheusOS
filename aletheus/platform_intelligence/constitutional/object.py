"""Canonical ConstitutionalObject model."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field, replace
from datetime import UTC, datetime
from types import MappingProxyType
from typing import Any, Mapping

from .enums import (
    ConstitutionalHealth,
    ConstitutionalKind,
    ConstitutionalState,
)
from .identity import ConstitutionalIdentity
from .transitions import (
    CANONICAL_TRANSITION_POLICY,
    ConstitutionalTransitionPolicy,
)


def _utc_now() -> datetime:
    return datetime.now(UTC)


def _freeze_mapping(
    value: Mapping[str, Any] | None,
) -> Mapping[str, Any]:
    return MappingProxyType(dict(value or {}))


@dataclass(frozen=True, slots=True)
class ConstitutionalObject:
    """
    Canonical representation of an entity recognized by AletheusOS.

    This model is intentionally independent of runtime implementation details.
    Operational components may project themselves into this representation,
    but the representation does not execute those components.
    """

    identity: ConstitutionalIdentity
    canonical_name: str
    version: str
    authority: str
    owner: str
    description: str = ""

    state: ConstitutionalState = ConstitutionalState.REGISTERED
    health: ConstitutionalHealth = ConstitutionalHealth.UNKNOWN

    created_at: datetime = field(default_factory=_utc_now)
    modified_at: datetime = field(default_factory=_utc_now)

    attributes: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )
    metrics: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        if not self.canonical_name.strip():
            raise ValueError("Canonical name cannot be empty.")

        if not self.version.strip():
            raise ValueError("Version cannot be empty.")

        if not self.authority.strip():
            raise ValueError("Constitutional authority cannot be empty.")

        if not self.owner.strip():
            raise ValueError("Constitutional owner cannot be empty.")

        if self.modified_at < self.created_at:
            raise ValueError(
                "modified_at cannot precede created_at."
            )

        object.__setattr__(
            self,
            "canonical_name",
            self.canonical_name.strip(),
        )
        object.__setattr__(self, "version", self.version.strip())
        object.__setattr__(self, "authority", self.authority.strip())
        object.__setattr__(self, "owner", self.owner.strip())
        object.__setattr__(
            self,
            "description",
            self.description.strip(),
        )
        object.__setattr__(
            self,
            "attributes",
            _freeze_mapping(self.attributes),
        )
        object.__setattr__(
            self,
            "metrics",
            _freeze_mapping(self.metrics),
        )

    @classmethod
    def create(
        cls,
        *,
        address: str,
        kind: ConstitutionalKind,
        canonical_name: str,
        version: str,
        authority: str,
        owner: str,
        description: str = "",
        state: ConstitutionalState = ConstitutionalState.REGISTERED,
        health: ConstitutionalHealth = ConstitutionalHealth.UNKNOWN,
        attributes: Mapping[str, Any] | None = None,
        metrics: Mapping[str, Any] | None = None,
    ) -> "ConstitutionalObject":
        return cls(
            identity=ConstitutionalIdentity.create(
                address=address,
                kind=kind,
            ),
            canonical_name=canonical_name,
            version=version,
            authority=authority,
            owner=owner,
            description=description,
            state=state,
            health=health,
            attributes=_freeze_mapping(attributes),
            metrics=_freeze_mapping(metrics),
        )

    @property
    def address(self) -> str:
        return str(self.identity.address)

    @property
    def kind(self) -> ConstitutionalKind:
        return self.identity.kind

    def transition_to(
        self,
        state: ConstitutionalState,
        *,
        health: ConstitutionalHealth | None = None,
        policy: ConstitutionalTransitionPolicy = (
            CANONICAL_TRANSITION_POLICY
        ),
    ) -> "ConstitutionalObject":
        """
        Return a new representation after validating lifecycle policy.

        The original object remains unchanged.
        """

        policy.require(self.state, state)

        return replace(
            self,
            state=state,
            health=health if health is not None else self.health,
            modified_at=_utc_now(),
        )

    def report_health(
        self,
        health: ConstitutionalHealth,
        *,
        metrics: Mapping[str, Any] | None = None,
    ) -> "ConstitutionalObject":
        """Return a new representation with updated health information."""

        return replace(
            self,
            health=health,
            metrics=(
                _freeze_mapping(metrics)
                if metrics is not None
                else self.metrics
            ),
            modified_at=_utc_now(),
        )

    def with_attributes(
        self,
        **attributes: Any,
    ) -> "ConstitutionalObject":
        """Return a new object with merged constitutional attributes."""

        merged = dict(self.attributes)
        merged.update(attributes)

        return replace(
            self,
            attributes=_freeze_mapping(merged),
            modified_at=_utc_now(),
        )

    def integrity_hash(self) -> str:
        """
        Produce a deterministic digest of constitutionally meaningful fields.

        Runtime timestamps are excluded so equivalent representations produce
        the same integrity hash.
        """

        payload = {
            "object_id": str(self.identity.object_id),
            "address": self.address,
            "kind": self.kind.value,
            "canonical_name": self.canonical_name,
            "version": self.version,
            "authority": self.authority,
            "owner": self.owner,
            "description": self.description,
            "state": self.state.value,
            "health": self.health.value,
            "attributes": dict(self.attributes),
            "metrics": dict(self.metrics),
        }

        encoded = json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            default=str,
        ).encode("utf-8")

        return hashlib.sha256(encoded).hexdigest()

    def to_snapshot(self) -> dict[str, Any]:
        """Serialize the object into a Digital Twin-compatible snapshot."""

        return {
            "identity": {
                "object_id": str(self.identity.object_id),
                "address": self.address,
                "kind": self.kind.value,
            },
            "canonical_name": self.canonical_name,
            "version": self.version,
            "authority": self.authority,
            "owner": self.owner,
            "description": self.description,
            "state": self.state.value,
            "health": self.health.value,
            "created_at": self.created_at.isoformat(),
            "modified_at": self.modified_at.isoformat(),
            "attributes": dict(self.attributes),
            "metrics": dict(self.metrics),
            "integrity_hash": self.integrity_hash(),
        }
