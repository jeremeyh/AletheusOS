from __future__ import annotations

import hashlib
import uuid
from datetime import datetime, timezone
from typing import Mapping, Sequence

from aletheus.mammoth.contracts.objects import (
    MammothIdentityStrategy,
    MammothObjectMetadata,
    MammothRetentionClass,
)
from aletheus.mammoth.serialization.canonical import canonical_json_bytes
from aletheus.mammoth.validation.invariants import MammothInvariants


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


class MammothObjectIdFactory:
    SCHEMA_VERSION = "1.0.0"

    @staticmethod
    def create(
        *,
        namespace: str,
        object_type: str,
        content_type: str,
        data: bytes,
        strategy: MammothIdentityStrategy,
        owner_capability: str,
        producer_capability: str,
        retention_class: MammothRetentionClass,
        tags: Sequence[str] = (),
        attributes: Mapping[str, str] | None = None,
        logical_object_id: str | None = None,
        lineage_id: str | None = None,
        parent_version_id: str | None = None,
        parent_version_sequence: int | None = None,
        now_iso: str | None = None,
    ) -> MammothObjectMetadata:
        if not isinstance(data, (bytes, bytearray, memoryview)):
            raise TypeError("data must be bytes-like")
        payload = bytes(data)
        namespace = MammothInvariants.validate_namespace(namespace)
        object_type = MammothInvariants.require_nonblank(object_type, "object_type")
        content_type = MammothInvariants.require_nonblank(content_type, "content_type")
        owner_capability = MammothInvariants.require_nonblank(owner_capability, "owner_capability")
        producer_capability = MammothInvariants.require_nonblank(producer_capability, "producer_capability")

        raw_digest = _sha256(payload)
        content_digest = f"sha256:{raw_digest}"
        timestamp = now_iso or _utc_now()
        MammothInvariants.validate_iso8601(timestamp)

        if logical_object_id is not None:
            object_id = MammothInvariants.validate_object_id(logical_object_id)
        elif strategy is MammothIdentityStrategy.CONTENT_ADDRESSED:
            object_id = f"mobj-{raw_digest[:32]}"
        else:
            object_id = f"mobj-{uuid.uuid4().hex}"

        if lineage_id is None:
            if strategy is MammothIdentityStrategy.CONTENT_ADDRESSED:
                seed = canonical_json_bytes({"namespace": namespace, "object_id": object_id})
                lineage_id = f"mlin-{_sha256(seed)[:32]}"
            else:
                lineage_id = f"mlin-{uuid.uuid4().hex}"
        MammothInvariants.validate_lineage_id(lineage_id)

        if parent_version_id is None:
            version_sequence = 1
        else:
            MammothInvariants.validate_version_id(parent_version_id)
            if parent_version_sequence is None or parent_version_sequence < 1:
                raise ValueError("parent_version_sequence >= 1 is required when parent_version_id is supplied")
            version_sequence = parent_version_sequence + 1

        version_material = canonical_json_bytes({
            "content_digest": content_digest,
            "lineage_id": lineage_id,
            "object_id": object_id,
            "parent_version_id": parent_version_id,
            "version_sequence": version_sequence,
        })
        version_id = f"mver-{_sha256(version_material)[:32]}"

        unique_tags = tuple(sorted({MammothInvariants.require_nonblank(t, "tag") for t in tags}))
        attrs = dict(sorted((attributes or {}).items()))

        return MammothObjectMetadata(
            object_id=object_id,
            version_id=version_id,
            lineage_id=lineage_id,
            version_sequence=version_sequence,
            parent_version_id=parent_version_id,
            namespace=namespace,
            object_type=object_type,
            content_type=content_type,
            size_bytes=len(payload),
            content_digest=content_digest,
            owner_capability=owner_capability,
            producer_capability=producer_capability,
            lifecycle_policy_id=f"policy-{retention_class.value.lower()}",
            retention_class=retention_class,
            schema_version=MammothObjectIdFactory.SCHEMA_VERSION,
            created_at_iso=timestamp,
            updated_at_iso=timestamp,
            tags=unique_tags,
            attributes=attrs,
        )
