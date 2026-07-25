"""Immutable CDM planning models."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from types import MappingProxyType
from typing import Any
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class DependencyLevel:
    """One dependency-safe execution level."""

    index: int
    services: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.index < 0:
            raise ValueError(
                "Dependency level index cannot be negative."
            )

        object.__setattr__(
            self,
            "services",
            tuple(sorted(self.services)),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "index": self.index,
            "services": list(self.services),
        }


@dataclass(frozen=True, slots=True)
class DependencyValidation:
    """Immutable dependency validation result."""

    valid: bool
    registered_services: int
    dependency_edges: int
    missing_dependencies: Mapping[
        str,
        tuple[str, ...],
    ]
    cycles: tuple[tuple[str, ...], ...]
    self_dependencies: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "missing_dependencies",
            MappingProxyType(
                {
                    address: tuple(
                        sorted(dependencies)
                    )
                    for address, dependencies
                    in self.missing_dependencies.items()
                }
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "valid": self.valid,
            "registered_services": (
                self.registered_services
            ),
            "dependency_edges": (
                self.dependency_edges
            ),
            "missing_dependencies": {
                address: list(dependencies)
                for address, dependencies
                in self.missing_dependencies.items()
            },
            "cycles": [
                list(cycle)
                for cycle in self.cycles
            ],
            "self_dependencies": list(
                self.self_dependencies
            ),
        }


@dataclass(frozen=True, slots=True)
class ConstitutionalDependencyPlan:
    """Immutable boot or shutdown plan."""

    plan_id: UUID
    generated_at: datetime
    direction: str
    levels: tuple[DependencyLevel, ...]
    service_count: int
    dependency_edges: int
    maximum_depth: int
    parallel_groups: int

    @classmethod
    def create(
        cls,
        *,
        direction: str,
        levels: tuple[DependencyLevel, ...],
        dependency_edges: int,
    ) -> ConstitutionalDependencyPlan:
        if direction not in {
            "boot",
            "shutdown",
            "restart",
        }:
            raise ValueError(
                f"Unsupported dependency plan direction: "
                f"{direction}"
            )

        return cls(
            plan_id=uuid4(),
            generated_at=datetime.now(UTC),
            direction=direction,
            levels=levels,
            service_count=sum(
                len(level.services)
                for level in levels
            ),
            dependency_edges=dependency_edges,
            maximum_depth=max(
                (
                    level.index
                    for level in levels
                ),
                default=0,
            ),
            parallel_groups=sum(
                len(level.services) > 1
                for level in levels
            ),
        )

    @property
    def ordered_services(
        self,
    ) -> tuple[str, ...]:
        return tuple(
            service
            for level in self.levels
            for service in level.services
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "plan_id": str(self.plan_id),
            "generated_at": (
                self.generated_at.isoformat()
            ),
            "direction": self.direction,
            "levels": [
                level.to_dict()
                for level in self.levels
            ],
            "ordered_services": list(
                self.ordered_services
            ),
            "service_count": self.service_count,
            "dependency_edges": (
                self.dependency_edges
            ),
            "maximum_depth": (
                self.maximum_depth
            ),
            "parallel_groups": (
                self.parallel_groups
            ),
        }


@dataclass(frozen=True, slots=True)
class DependencyManagerStatistics:
    """Immutable CDM statistics."""

    services: int
    dependency_edges: int
    boot_levels: int
    maximum_depth: int
    parallel_groups: int
    root_services: int
    leaf_services: int

    def to_dict(self) -> dict[str, int]:
        return {
            "services": self.services,
            "dependency_edges": (
                self.dependency_edges
            ),
            "boot_levels": self.boot_levels,
            "maximum_depth": self.maximum_depth,
            "parallel_groups": self.parallel_groups,
            "root_services": self.root_services,
            "leaf_services": self.leaf_services,
        }
