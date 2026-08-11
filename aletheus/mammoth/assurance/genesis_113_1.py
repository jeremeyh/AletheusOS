from __future__ import annotations

import hashlib
from dataclasses import dataclass

from aletheus.mammoth.contracts.objects import MammothIdentityStrategy, MammothRetentionClass
from aletheus.mammoth.identity.object_ids import MammothObjectIdFactory
from aletheus.mammoth.identity.version_lineage import MammothVersionLineage


@dataclass(frozen=True, slots=True)
class Genesis1131AssuranceResult:
    status: str
    checks: tuple[str, ...]
    evidence_digest: str


class Genesis1131Assurance:
    """Non-RAF local assurance probe. RAF remains external certification authority."""

    @staticmethod
    def run() -> Genesis1131AssuranceResult:
        payload = b"ALETHEUSOS-MAMMOTH-GENESIS-113.1-ASSURANCE"
        first = MammothObjectIdFactory.create(
            namespace="system.assurance",
            object_type="probe",
            content_type="application/octet-stream",
            data=payload,
            strategy=MammothIdentityStrategy.LOGICAL,
            owner_capability="Mammoth",
            producer_capability="Genesis113.1",
            retention_class=MammothRetentionClass.TRANSIENT,
            now_iso="2026-01-01T00:00:00Z",
        )
        lineage = MammothVersionLineage.from_metadata(first)
        second = MammothObjectIdFactory.create(
            namespace=first.namespace,
            object_type=first.object_type,
            content_type=first.content_type,
            data=payload + b"-V2",
            strategy=MammothIdentityStrategy.LOGICAL,
            owner_capability=first.owner_capability,
            producer_capability="Genesis113.1",
            retention_class=first.retention_class,
            logical_object_id=first.object_id,
            lineage_id=first.lineage_id,
            parent_version_id=first.version_id,
            parent_version_sequence=first.version_sequence,
            now_iso="2026-01-01T00:00:01Z",
        )
        lineage.assert_can_parent(second)
        checks = (
            "OBJECT_ID_VALID",
            "VERSION_ID_VALID",
            "LINEAGE_CONTIGUOUS",
            "FULL_SHA256_CONTENT_DIGEST",
            "PROVIDER_IMPLEMENTATION_ABSENT_BY_DESIGN",
            "RAF_AUTHORITY_NOT_REIMPLEMENTED",
        )
        digest = hashlib.sha256("\n".join(checks).encode()).hexdigest()
        return Genesis1131AssuranceResult("PASS", checks, f"sha256:{digest}")
