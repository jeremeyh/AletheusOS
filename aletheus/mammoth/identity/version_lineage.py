from __future__ import annotations

from dataclasses import dataclass

from aletheus.mammoth.contracts.objects import MammothObjectMetadata
from aletheus.mammoth.validation.invariants import MammothInvariantViolation, MammothInvariants


@dataclass(frozen=True, slots=True)
class MammothVersionLineage:
    object_id: str
    lineage_id: str
    latest_version_id: str
    latest_sequence: int

    @classmethod
    def from_metadata(cls, metadata: MammothObjectMetadata) -> "MammothVersionLineage":
        MammothInvariants.validate_object_id(metadata.object_id)
        MammothInvariants.validate_lineage_id(metadata.lineage_id)
        MammothInvariants.validate_version_id(metadata.version_id)
        if metadata.version_sequence < 1:
            raise MammothInvariantViolation("version_sequence must be >= 1")
        if metadata.version_sequence == 1 and metadata.parent_version_id is not None:
            raise MammothInvariantViolation("version 1 cannot have a parent_version_id")
        if metadata.version_sequence > 1 and metadata.parent_version_id is None:
            raise MammothInvariantViolation("version >1 requires parent_version_id")
        return cls(metadata.object_id, metadata.lineage_id, metadata.version_id, metadata.version_sequence)

    def assert_can_parent(self, child: MammothObjectMetadata) -> None:
        if child.object_id != self.object_id:
            raise MammothInvariantViolation("child object_id differs from lineage object_id")
        if child.lineage_id != self.lineage_id:
            raise MammothInvariantViolation("child lineage_id differs from lineage_id")
        if child.parent_version_id != self.latest_version_id:
            raise MammothInvariantViolation("child parent_version_id is not current lineage head")
        if child.version_sequence != self.latest_sequence + 1:
            raise MammothInvariantViolation("child version_sequence is not contiguous")
