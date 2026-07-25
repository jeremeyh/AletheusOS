"""Immutable Constitutional Graph statistics."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ConstitutionalGraphStatistics:
    """Immutable topology statistics."""

    nodes: int
    relationships: int
    roots: int
    leaves: int
    orphans: int
    cycles: int
    connected_components: int
    maximum_depth: int
    average_out_degree: float
    average_in_degree: float
    nodes_by_kind: Mapping[str, int]
    relationships_by_kind: Mapping[str, int]

    def to_dict(self) -> dict[str, object]:
        return {
            "nodes": self.nodes,
            "relationships": self.relationships,
            "roots": self.roots,
            "leaves": self.leaves,
            "orphans": self.orphans,
            "cycles": self.cycles,
            "connected_components": (
                self.connected_components
            ),
            "maximum_depth": self.maximum_depth,
            "average_out_degree": (
                self.average_out_degree
            ),
            "average_in_degree": (
                self.average_in_degree
            ),
            "nodes_by_kind": dict(
                self.nodes_by_kind
            ),
            "relationships_by_kind": dict(
                self.relationships_by_kind
            ),
        }
