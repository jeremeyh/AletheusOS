"""Models for Kinekt™ runtime topology."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class ModuleTopology:
    module: str
    package: str
    incoming: tuple[str, ...]
    outgoing: tuple[str, ...]
    fan_in: int
    fan_out: int


@dataclass(frozen=True, slots=True)
class PackageTopology:
    package: str
    modules: int
    internal_edges: int
    inbound_packages: tuple[str, ...]
    outbound_packages: tuple[str, ...]
    cycle_groups: int
    isolated_modules: int


@dataclass(slots=True)
class TopologyReport:
    generated_at: str
    source_report: str
    modules: list[ModuleTopology] = field(default_factory=list)
    packages: list[PackageTopology] = field(default_factory=list)
    entry_points: list[str] = field(default_factory=list)
    sinks: list[str] = field(default_factory=list)
    isolated: list[str] = field(default_factory=list)
    strongly_connected_components: list[list[str]] = field(default_factory=list)
    cycles: list[list[str]] = field(default_factory=list)
    longest_chains: list[list[str]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
