"""Snapshot comparison for the Platform Digital Twin."""

from __future__ import annotations

from dataclasses import dataclass

from .snapshot import TwinSnapshot


def _addresses(
    records: tuple[object, ...],
) -> set[str]:
    addresses: set[str] = set()

    for record in records:
        if not isinstance(record, dict):
            record = dict(record)  # type: ignore[arg-type]

        identity = record.get("identity", {})

        if isinstance(identity, dict):
            address = identity.get("address")

            if isinstance(address, str):
                addresses.add(address)

    return addresses


@dataclass(frozen=True, slots=True)
class TwinSnapshotDiff:
    """Structural difference between two Twin snapshots."""

    from_revision: int
    to_revision: int
    added_services: tuple[str, ...]
    removed_services: tuple[str, ...]
    added_nodes: tuple[str, ...]
    removed_nodes: tuple[str, ...]
    relationship_delta: int
    health_changed: bool
    topology_changed: bool

    @classmethod
    def between(
        cls,
        previous: TwinSnapshot,
        current: TwinSnapshot,
    ) -> TwinSnapshotDiff:
        previous_services = _addresses(previous.services)
        current_services = _addresses(current.services)

        previous_nodes = _addresses(previous.nodes)
        current_nodes = _addresses(current.nodes)

        return cls(
            from_revision=previous.revision,
            to_revision=current.revision,
            added_services=tuple(sorted(current_services - previous_services)),
            removed_services=tuple(sorted(previous_services - current_services)),
            added_nodes=tuple(sorted(current_nodes - previous_nodes)),
            removed_nodes=tuple(sorted(previous_nodes - current_nodes)),
            relationship_delta=(
                len(current.relationships) - len(previous.relationships)
            ),
            health_changed=(dict(previous.health) != dict(current.health)),
            topology_changed=(dict(previous.topology) != dict(current.topology)),
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "from_revision": self.from_revision,
            "to_revision": self.to_revision,
            "added_services": list(self.added_services),
            "removed_services": list(self.removed_services),
            "added_nodes": list(self.added_nodes),
            "removed_nodes": list(self.removed_nodes),
            "relationship_delta": (self.relationship_delta),
            "health_changed": self.health_changed,
            "topology_changed": (self.topology_changed),
        }
