"""Models for the Platform Service Registry."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any

from aletheus.platform_intelligence.constitutional import (
    ConstitutionalAddress,
    ConstitutionalHealth,
    ConstitutionalKind,
    ConstitutionalObject,
    ConstitutionalState,
)


@dataclass(frozen=True, slots=True)
class PlatformServiceDefinition:
    """Declarative definition used to register a platform service."""

    address: ConstitutionalAddress
    canonical_name: str
    version: str
    authority: str
    owner: str
    description: str
    dependencies: frozenset[ConstitutionalAddress]
    attributes: Mapping[str, Any]

    @classmethod
    def create(
        cls,
        *,
        address: str | ConstitutionalAddress,
        canonical_name: str,
        version: str,
        authority: str,
        owner: str,
        description: str = "",
        dependencies: (
            set[str | ConstitutionalAddress]
            | frozenset[str | ConstitutionalAddress]
            | tuple[str | ConstitutionalAddress, ...]
            | list[str | ConstitutionalAddress]
            | None
        ) = None,
        attributes: Mapping[str, Any] | None = None,
    ) -> PlatformServiceDefinition:
        service_address = (
            address
            if isinstance(address, ConstitutionalAddress)
            else ConstitutionalAddress(address)
        )

        dependency_addresses = frozenset(
            dependency
            if isinstance(
                dependency,
                ConstitutionalAddress,
            )
            else ConstitutionalAddress(dependency)
            for dependency in (dependencies or ())
        )

        if service_address in dependency_addresses:
            raise ValueError(
                "A platform service cannot depend on itself."
            )

        return cls(
            address=service_address,
            canonical_name=canonical_name.strip(),
            version=version.strip(),
            authority=authority.strip(),
            owner=owner.strip(),
            description=description.strip(),
            dependencies=dependency_addresses,
            attributes=MappingProxyType(
                dict(attributes or {})
            ),
        )

    def to_constitutional_object(
        self,
    ) -> ConstitutionalObject:
        """Create the canonical constitutional representation."""

        attributes = dict(self.attributes)
        attributes["dependencies"] = sorted(
            str(dependency)
            for dependency in self.dependencies
        )

        return ConstitutionalObject.create(
            address=str(self.address),
            kind=ConstitutionalKind.PLATFORM_SERVICE,
            canonical_name=self.canonical_name,
            version=self.version,
            authority=self.authority,
            owner=self.owner,
            description=self.description,
            state=ConstitutionalState.REGISTERED,
            health=ConstitutionalHealth.UNKNOWN,
            attributes=attributes,
        )


@dataclass(frozen=True, slots=True)
class PlatformServiceRegistryStatistics:
    """Immutable Platform Service Registry statistics."""

    registered: int
    running: int
    degraded: int
    unhealthy: int
    dependency_edges: int
    services_by_state: Mapping[str, int]
    services_by_health: Mapping[str, int]

    def to_dict(self) -> dict[str, object]:
        return {
            "registered": self.registered,
            "running": self.running,
            "degraded": self.degraded,
            "unhealthy": self.unhealthy,
            "dependency_edges": self.dependency_edges,
            "services_by_state": dict(
                self.services_by_state
            ),
            "services_by_health": dict(
                self.services_by_health
            ),
        }
