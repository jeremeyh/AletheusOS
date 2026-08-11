from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Mapping, Tuple


class MammothIdentityStrategy(str, Enum):
    LOGICAL = "LOGICAL"
    CONTENT_ADDRESSED = "CONTENT_ADDRESSED"


class MammothRetentionClass(str, Enum):
    TRANSIENT = "TRANSIENT"
    STANDARD = "STANDARD"
    ARCHIVAL = "ARCHIVAL"
    IMMUTABLE = "IMMUTABLE"


@dataclass(frozen=True, slots=True)
class MammothObjectMetadata:
    """Canonical metadata envelope for one persistent object version.

    Identity layers are deliberately separate:
    * object_id: stable logical object identity
    * version_id: immutable identity of one version
    * content_digest: exact bytes identity
    """

    object_id: str
    version_id: str
    lineage_id: str
    version_sequence: int
    parent_version_id: str | None
    namespace: str
    object_type: str
    content_type: str
    size_bytes: int
    content_digest: str
    owner_capability: str
    producer_capability: str
    lifecycle_policy_id: str
    retention_class: MammothRetentionClass
    schema_version: str
    created_at_iso: str
    updated_at_iso: str
    tags: Tuple[str, ...] = field(default_factory=tuple)
    attributes: Mapping[str, str] = field(default_factory=dict)

    def to_canonical_dict(self) -> dict[str, object]:
        return {
            "attributes": dict(sorted(self.attributes.items())),
            "content_digest": self.content_digest,
            "content_type": self.content_type,
            "created_at_iso": self.created_at_iso,
            "lifecycle_policy_id": self.lifecycle_policy_id,
            "lineage_id": self.lineage_id,
            "namespace": self.namespace,
            "object_id": self.object_id,
            "object_type": self.object_type,
            "owner_capability": self.owner_capability,
            "parent_version_id": self.parent_version_id,
            "producer_capability": self.producer_capability,
            "retention_class": self.retention_class.value,
            "schema_version": self.schema_version,
            "size_bytes": self.size_bytes,
            "tags": list(self.tags),
            "updated_at_iso": self.updated_at_iso,
            "version_id": self.version_id,
            "version_sequence": self.version_sequence,
        }
